from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd


MODELS_DIR = Path(__file__).resolve().parent
MODEL_PATH = MODELS_DIR / "fraud_detection_pipeline.joblib"
METADATA_PATH = MODELS_DIR / "model_metadata.json"


def risk_level(probability: float) -> str:
    if probability >= 0.8:
        return "high"
    if probability >= 0.5:
        return "medium"
    return "low"


def main() -> None:
    pipeline = joblib.load(MODEL_PATH)
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))

    sample_transaction = {
        "Time": 406.0,
        "V1": -2.3122265423263,
        "V2": 1.95199201064158,
        "V3": -1.60985073229769,
        "V4": 3.9979055875468,
        "V5": -0.522187864667764,
        "V6": -1.42654531920595,
        "V7": -2.53738730624579,
        "V8": 1.39165724829804,
        "V9": -2.77008927719433,
        "V10": -2.77227214465915,
        "V11": 3.20203320709635,
        "V12": -2.89990738849473,
        "V13": -0.595221881324605,
        "V14": -4.28925378244217,
        "V15": 0.389724120274487,
        "V16": -1.14074717980657,
        "V17": -2.83005567450437,
        "V18": -0.0168224681808257,
        "V19": 0.416955705037907,
        "V20": 0.126910559061474,
        "V21": 0.517232370861764,
        "V22": -0.0350493686052974,
        "V23": -0.465211076182388,
        "V24": 0.320198198514526,
        "V25": 0.0445191674731724,
        "V26": 0.177839798284401,
        "V27": 0.261145002567677,
        "V28": -0.143275874698919,
        "Amount": 0.0,
    }

    input_df = pd.DataFrame([sample_transaction], columns=metadata["features"])
    fraud_probability = float(pipeline.predict_proba(input_df)[0, 1])
    predicted_label = int(fraud_probability >= metadata["threshold"])

    result = {
        "fraud_probability": fraud_probability,
        "predicted_label": predicted_label,
        "risk_level": risk_level(fraud_probability),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
