import csv
from functools import lru_cache
from pathlib import Path

from app.schemas import EntityEvidence, Transaction, TransactionRiskFacts
from app.services.model_inference import predict_transaction, score_from_prediction
from app.services.risk_rules import match_rule_hits, score_risk

DATA_FILE_NAME = "sample_transactions.csv"


class TransactionNotFoundError(ValueError):
    pass


@lru_cache(maxsize=1)
def load_transactions() -> list[Transaction]:
    with _resolve_data_path().open(newline="", encoding="utf-8-sig") as csv_file:
        return [
            Transaction(
                transaction_id=row["transaction_id"],
                user_id=row["user_id"],
                merchant_id=row["merchant_id"],
                device_id=row["device_id"],
                ip=row["ip"],
                country=row["country"],
                amount=float(row["amount"]),
                event_time=row["event_time"],
                label=int(row["label"]),
            )
            for row in csv.DictReader(csv_file)
        ]


def get_transaction_risk_facts(transaction_id: str) -> TransactionRiskFacts:
    transactions = load_transactions()
    transaction = next(
        (item for item in transactions if item.transaction_id == transaction_id),
        None,
    )
    if transaction is None:
        raise TransactionNotFoundError(f"Transaction {transaction_id} was not found.")

    prior_transactions = [
        item for item in transactions if item.event_time < transaction.event_time
    ]
    user_prior = [
        item for item in prior_transactions if item.user_id == transaction.user_id
    ]

    entity_evidence = _build_entity_evidence(transaction, transactions, user_prior)
    rule_hits = match_rule_hits(
        transaction=transaction,
        evidence=entity_evidence,
        user_prior_devices={item.device_id for item in user_prior},
        user_prior_ips={item.ip for item in user_prior},
        user_prior_countries={item.country for item in user_prior},
    )
    model_prediction = predict_transaction(transaction.transaction_id)
    if model_prediction is not None:
        risk_score, risk_level = score_from_prediction(model_prediction)
    else:
        risk_score, risk_level = score_risk(rule_hits)

    return TransactionRiskFacts(
        transaction=transaction,
        entity_evidence=entity_evidence,
        model_prediction=model_prediction,
        rule_hits=rule_hits,
        risk_score=risk_score,
        risk_level=risk_level,
    )


def _build_entity_evidence(
    transaction: Transaction,
    transactions: list[Transaction],
    user_prior: list[Transaction],
) -> EntityEvidence:
    device_transactions = [
        item for item in transactions if item.device_id == transaction.device_id
    ]
    ip_transactions = [item for item in transactions if item.ip == transaction.ip]
    merchant_transactions = [
        item for item in transactions if item.merchant_id == transaction.merchant_id
    ]

    user_amounts = [item.amount for item in user_prior]

    return EntityEvidence(
        user_transaction_count=len(user_prior),
        user_average_amount=round(sum(user_amounts) / len(user_amounts), 2)
        if user_amounts
        else None,
        user_max_amount=max(user_amounts) if user_amounts else None,
        user_known_countries=sorted({item.country for item in user_prior}),
        device_transaction_count=len(device_transactions),
        device_user_count=len({item.user_id for item in device_transactions}),
        ip_transaction_count=len(ip_transactions),
        ip_user_count=len({item.user_id for item in ip_transactions}),
        merchant_transaction_count=len(merchant_transactions),
        merchant_confirmed_fraud_count=sum(
            1
            for item in merchant_transactions
            if item.label == 1 and item.transaction_id != transaction.transaction_id
        ),
    )


def _resolve_data_path() -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "data" / DATA_FILE_NAME
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Could not locate data/{DATA_FILE_NAME}.")
