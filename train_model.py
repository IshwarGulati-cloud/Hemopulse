import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["%Red Pixel", "%Green pixel", "%Blue pixel"]
LEVELS = np.array(["Severe", "Moderate", "Mild", "Normal"])
MODEL_PATH = Path(__file__).parent / "app" / "models" / "hemopulse_model.pkl"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()

    data = pd.read_csv(args.csv_path)
    data = data.dropna(subset=FEATURES + ["Hb"])
    cutoffs = data["Hb"].quantile([0.25, 0.5, 0.75]).to_numpy()
    labels = LEVELS[np.digitize(data["Hb"], cutoffs)]
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, data[FEATURES], labels, cv=folds, scoring="balanced_accuracy")
    model.fit(data[FEATURES], labels)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "hb_cutoffs": cutoffs,
            "label_basis": "training CSV Hb quartiles; demo only",
            "cross_validation_balanced_accuracy": float(scores.mean()),
        },
        MODEL_PATH,
    )
    print(f"Saved demo model; 5-fold balanced accuracy: {scores.mean():.3f} ± {scores.std():.3f}")


if __name__ == "__main__":
    main()
