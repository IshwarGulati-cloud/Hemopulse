from pathlib import Path

import joblib
import cv2
import numpy as np
import pandas as pd
from app.schemas.predict import ScreeningInputSchema, ScreeningOutputSchema

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "hemopulse_model.pkl"
FEATURES = ["%Red Pixel", "%Green pixel", "%Blue pixel"]


class MLInferenceService:
    def __init__(self):
        artifact = joblib.load(MODEL_PATH)
        self.model = artifact["model"]

    def predict(self, payload: ScreeningInputSchema) -> ScreeningOutputSchema:
        features = pd.DataFrame(
            [[payload.red_ratio, payload.green_ratio, payload.blue_ratio]],
            columns=FEATURES,
        )
        risk_level = str(self.model.predict(features)[0])
        confidence = float(max(self.model.predict_proba(features)[0]))

        return ScreeningOutputSchema(
            anemic_status="Not clinically assessed",
            risk_level=risk_level,
            confidence_score=round(confidence, 2),
            recommended_action="Demo only. Confirm hemoglobin with a laboratory test; do not use this result for care decisions.",
            demo_only=True,
        )

    def predict_image(self, image_bytes: bytes) -> ScreeningOutputSchema:
        image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Could not decode image; upload a JPEG or PNG photo.")

        height, width = image.shape[:2]
        if height < 4 or width < 4:
            raise ValueError("Image is too small to process.")
        # Demo assumption: the lower conjunctiva is centered; this is not segmentation.
        crop = image[height // 4 : 3 * height // 4, width // 4 : 3 * width // 4]
        rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        channel_means = rgb.mean(axis=(0, 1))
        if channel_means.sum() == 0:
            raise ValueError("Image crop contains no usable color information.")
        ratios = channel_means / channel_means.sum() * 100
        return self.predict(
            ScreeningInputSchema(
                red_ratio=ratios[0],
                green_ratio=ratios[1],
                blue_ratio=ratios[2],
            )
        )

ml_service = MLInferenceService()
