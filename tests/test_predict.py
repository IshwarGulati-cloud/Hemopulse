import unittest
from unittest.mock import patch

import cv2
import numpy as np

from app.schemas.facility import HealthcareFacilitySchema
from app.schemas.predict import ScreeningInputSchema
from app.services.ml_service import ml_service


class FacilitySchemaTests(unittest.TestCase):
    def test_accepts_catalog_record(self):
        facility = HealthcareFacilitySchema.model_validate(
            {
                "id": "0d8b6c9e-b3a2-4c2f-9e9b-a14e643506f8",
                "name": "Village PHC",
                "facility_type": "PHC",
                "referral_level": 2,
                "address": "Bengaluru Rural",
                "phone": None,
                "latitude": 13.1,
                "longitude": 77.5,
                "google_maps_url": None,
            }
        )

        self.assertEqual(facility.referral_level, 2)


class AppStartupTests(unittest.TestCase):
    def test_import_does_not_create_supabase_client(self):
        with patch("supabase.create_client") as create_client:
            import app.main  # noqa: F401

        create_client.assert_not_called()


class PredictionTests(unittest.TestCase):
    def test_returns_demo_only_four_tier_result(self):
        result = ml_service.predict(
            ScreeningInputSchema(red_ratio=34, green_ratio=33, blue_ratio=33)
        )

        self.assertIn(result.risk_level, {"Normal", "Mild", "Moderate", "Severe"})
        self.assertTrue(result.demo_only)

    def test_predict_image_accepts_centered_closeup(self):
        image = np.full((64, 64, 3), (80, 100, 140), dtype=np.uint8)
        ok, encoded = cv2.imencode(".png", image)

        self.assertTrue(ok)
        result = ml_service.predict_image(encoded.tobytes())
        self.assertTrue(result.demo_only)

    def test_predict_image_rejects_invalid_bytes(self):
        with self.assertRaises(ValueError):
            ml_service.predict_image(b"not an image")

    def test_photo_upload_is_documented_in_openapi(self):
        from app.main import app

        body = app.openapi()["paths"]["/api/v1/predict/eyelid/image"]["post"]["requestBody"]
        self.assertIn("multipart/form-data", body["content"])
