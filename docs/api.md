# API Reference

Base URL for local development:

```text
http://127.0.0.1:8000
```

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

## Transaction Risk Facts

```http
GET /transactions/{transaction_id}
```

Example:

```http
GET /transactions/T1002
```

Returns the transaction profile, model prediction, historical entity evidence, matched rules, risk score, and risk level.

Key fields:

- `transaction`: basic transaction attributes.
- `model_prediction`: local model fraud probability, predicted label, and threshold.
- `entity_evidence`: user, device, IP, and merchant history features.
- `rule_hits`: deterministic fraud rule matches.
- `risk_score`: integer score from 0 to 100.
- `risk_level`: `low`, `medium`, or `high`.

## Investigation Report

```http
GET /investigations/{transaction_id}
```

Example:

```http
GET /investigations/T1002
```

Returns the same risk facts plus retrieved rule context and a mock Agent report.

Example report shape:

```json
{
  "transaction_id": "T1002",
  "retrieved_rules": [
    {
      "rule_id": "KB002",
      "title": "High-Risk Signals",
      "source": "data/rules.md",
      "content": "New device or new IP shortly before a high-value transaction.",
      "relevance_score": 5.0,
      "matched_terms": ["device", "high-value", "ip", "new", "transaction"]
    }
  ],
  "report": {
    "risk_level": "high",
    "risk_score": 100,
    "evidence": [
      "Model fraud probability is 0.9998 against threshold 0.50.",
      "Amount 1299.00 exceeds the large-amount threshold against no prior user amount history.",
      "High-value transaction uses new device D902 and IP 198.51.100.21 for user U002."
    ],
    "possible_fraud_pattern": "High-value transaction from a new access context.",
    "suggested_action": "Hold or step-up the transaction and route it to manual review.",
    "review_caveats": [
      "This mock Agent is deterministic and does not call an external LLM.",
      "Retrieved rules are used as local RAG context before report generation."
    ]
  }
}
```

## Sample Transaction IDs

- `T1001`: low-risk normal transaction.
- `T1002`: high-value transaction from a new device/IP.
- `T1003`: repeat low-risk transaction.
- `T1004`: high-risk transaction with fraud-like model features and limited history.
