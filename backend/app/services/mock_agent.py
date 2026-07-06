from app.schemas import InvestigationReport, TransactionRiskFacts


def build_investigation_report(risk_facts: TransactionRiskFacts) -> InvestigationReport:
    transaction = risk_facts.transaction
    evidence = [hit.evidence for hit in risk_facts.rule_hits]
    if risk_facts.model_prediction is not None:
        evidence.insert(
            0,
            (
                "Model fraud probability is "
                f"{risk_facts.model_prediction.fraud_probability:.4f} "
                f"against threshold {risk_facts.model_prediction.threshold:.2f}."
            ),
        )

    if not evidence:
        evidence = [
            "No high-risk rule was triggered by the current transaction profile.",
            (
                f"Transaction amount {transaction.amount:.2f} is within the observed "
                "behavioral range for available sample data."
            ),
        ]

    return InvestigationReport(
        risk_level=risk_facts.risk_level,
        risk_score=risk_facts.risk_score,
        evidence=evidence,
        possible_fraud_pattern=_infer_pattern(risk_facts),
        suggested_action=_suggest_action(risk_facts.risk_level),
        review_caveats=[
            "This mock Agent is deterministic and does not call an external LLM.",
            "Sample data is small, so entity history should be treated as demo evidence.",
            "Ground-truth labels are kept separate from the suggested analyst action.",
        ],
    )


def _infer_pattern(risk_facts: TransactionRiskFacts) -> str:
    rule_ids = {hit.rule_id for hit in risk_facts.rule_hits}

    if (
        risk_facts.model_prediction is not None
        and risk_facts.model_prediction.predicted_label == 1
        and {"R001", "R002"} <= rule_ids
    ):
        return "Model-confirmed high-risk transaction with new access context."
    if {"R001", "R002"} <= rule_ids:
        return "High-value transaction from a new access context."
    if "R004" in rule_ids:
        return "Entity-linked fraud exposure through merchant, device, or IP history."
    if "R001" in rule_ids:
        return "Amount anomaly compared with available user history."
    if "R002" in rule_ids or "R003" in rule_ids:
        return "Account access anomaly requiring identity and device review."
    return "No clear fraud pattern detected from current mock rules."


def _suggest_action(risk_level: str) -> str:
    if risk_level == "high":
        return "Hold or step-up the transaction and route it to manual review."
    if risk_level == "medium":
        return "Allow with additional verification or queue for analyst sampling."
    return "Allow, while keeping the event available for monitoring and feedback."
