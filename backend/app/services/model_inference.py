import csv
import json
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from app.schemas import ModelPrediction

MODEL_DIR_NAME = "credit_card_fraud"
MODEL_FILE_NAME = "fraud_detection_pipeline.joblib"
METADATA_FILE_NAME = "model_metadata.json"
FEATURES_FILE_NAME = "model_features.csv"


@lru_cache(maxsize=1)
def _load_model_bundle():
    model_dir = _resolve_model_dir()
    metadata = json.loads((model_dir / METADATA_FILE_NAME).read_text(encoding="utf-8"))
    pipeline = joblib.load(model_dir / MODEL_FILE_NAME)
    return pipeline, metadata


@lru_cache(maxsize=1)
def _load_feature_rows() -> dict[str, dict[str, float]]:
    feature_path = _resolve_data_path(FEATURES_FILE_NAME)
    with feature_path.open(newline="", encoding="utf-8-sig") as csv_file:
        rows = {}
        for row in csv.DictReader(csv_file):
            transaction_id = row.pop("transaction_id")
            rows[transaction_id] = {key: float(value) for key, value in row.items()}
        return rows


def predict_transaction(transaction_id: str) -> ModelPrediction | None:
    feature_rows = _load_feature_rows()
    model_features = feature_rows.get(transaction_id)
    if model_features is None:
        return None

    pipeline, metadata = _load_model_bundle()
    feature_names = metadata["features"]
    input_df = pd.DataFrame([model_features], columns=feature_names)
    fraud_probability = float(pipeline.predict_proba(input_df)[0, 1])
    threshold = float(metadata["threshold"])

    return ModelPrediction(
        model_name=metadata["model_type"],
        fraud_probability=fraud_probability,
        predicted_label=int(fraud_probability >= threshold),
        threshold=threshold,
        risk_level=_risk_level(fraud_probability),
        features_available=True,
    )


def score_from_prediction(prediction: ModelPrediction) -> tuple[int, str]:
    score = round(prediction.fraud_probability * 100)
    return score, prediction.risk_level


def _risk_level(probability: float) -> str:
    if probability >= 0.8:
        return "high"
    if probability >= 0.5:
        return "medium"
    return "low"


def _resolve_model_dir() -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "models" / MODEL_DIR_NAME
        if (candidate / MODEL_FILE_NAME).exists() and (candidate / METADATA_FILE_NAME).exists():
            return candidate
    raise FileNotFoundError(f"Could not locate models/{MODEL_DIR_NAME}.")


def _resolve_data_path(file_name: str) -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "data" / file_name
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Could not locate data/{file_name}.")
