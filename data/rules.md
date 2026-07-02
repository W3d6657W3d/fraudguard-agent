# Fraud Review Rules

## High-Risk Signals

- Sudden large transaction amount compared with user history.
- New device or new IP shortly before a high-value transaction.
- Multiple failed attempts followed by a successful transaction.
- Merchant, IP, or device connected to previously confirmed fraud.

## Review Guidance

- Prioritize precision-recall trade-offs over accuracy in imbalanced fraud datasets.
- Use PR-AUC as a core offline metric when positive fraud samples are rare.
- Separate model score, rule hits, and analyst decision for auditability.
