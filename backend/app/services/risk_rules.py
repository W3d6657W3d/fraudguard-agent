from app.schemas import EntityEvidence, RuleHit, Transaction


def match_rule_hits(
    transaction: Transaction,
    evidence: EntityEvidence,
    user_prior_devices: set[str],
    user_prior_ips: set[str],
    user_prior_countries: set[str],
) -> list[RuleHit]:
    hits: list[RuleHit] = []

    if _is_large_amount(transaction.amount, evidence.user_average_amount):
        baseline = (
            f"user average {evidence.user_average_amount:.2f}"
            if evidence.user_average_amount is not None
            else "no prior user amount history"
        )
        hits.append(
            RuleHit(
                rule_id="R001",
                name="Sudden large transaction amount",
                severity="high",
                description="Transaction amount is unusually large compared with user history.",
                evidence=f"Amount {transaction.amount:.2f} exceeds the large-amount threshold against {baseline}.",
                score_impact=45,
            )
        )

    has_new_device = transaction.device_id not in user_prior_devices
    has_new_ip = transaction.ip not in user_prior_ips
    if transaction.amount >= 500 and (has_new_device or has_new_ip):
        new_parts = []
        if has_new_device:
            new_parts.append(f"device {transaction.device_id}")
        if has_new_ip:
            new_parts.append(f"IP {transaction.ip}")
        hits.append(
            RuleHit(
                rule_id="R002",
                name="New device or IP on high-value transaction",
                severity="medium",
                description="A high-value transaction uses an access context not seen in prior user history.",
                evidence=f"High-value transaction uses new {' and '.join(new_parts)} for user {transaction.user_id}.",
                score_impact=30,
            )
        )

    if transaction.amount >= 500 and user_prior_countries and transaction.country not in user_prior_countries:
        hits.append(
            RuleHit(
                rule_id="R003",
                name="Country shift on high-value transaction",
                severity="medium",
                description="Transaction country differs from the user's previously observed countries.",
                evidence=(
                    f"Country {transaction.country} is not in prior countries "
                    f"{sorted(user_prior_countries)} for user {transaction.user_id}."
                ),
                score_impact=25,
            )
        )

    if evidence.merchant_confirmed_fraud_count > 0:
        hits.append(
            RuleHit(
                rule_id="R004",
                name="Merchant linked to confirmed fraud",
                severity="high",
                description="Merchant appears in transactions previously labeled as confirmed fraud.",
                evidence=(
                    f"Merchant {transaction.merchant_id} is linked to "
                    f"{evidence.merchant_confirmed_fraud_count} confirmed fraud sample(s)."
                ),
                score_impact=35,
            )
        )

    return hits


def score_risk(rule_hits: list[RuleHit]) -> tuple[int, str]:
    score = min(100, sum(hit.score_impact for hit in rule_hits))

    if score >= 70:
        return score, "high"
    if score >= 30:
        return score, "medium"
    return score, "low"


def _is_large_amount(amount: float, user_average_amount: float | None) -> bool:
    if user_average_amount is None:
        return amount >= 1000
    return amount >= 500 and amount >= user_average_amount * 2.5
