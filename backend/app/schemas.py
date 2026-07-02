from pydantic import BaseModel, Field


class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    merchant_id: str
    device_id: str
    ip: str
    country: str
    amount: float
    event_time: str
    label: int


class EntityEvidence(BaseModel):
    user_transaction_count: int
    user_average_amount: float | None
    user_max_amount: float | None
    user_known_countries: list[str]
    device_transaction_count: int
    device_user_count: int
    ip_transaction_count: int
    ip_user_count: int
    merchant_transaction_count: int
    merchant_confirmed_fraud_count: int


class RuleHit(BaseModel):
    rule_id: str
    name: str
    severity: str
    description: str
    evidence: str
    score_impact: int = Field(ge=0, le=100)


class TransactionRiskFacts(BaseModel):
    transaction: Transaction
    entity_evidence: EntityEvidence
    rule_hits: list[RuleHit]
    risk_score: int = Field(ge=0, le=100)
    risk_level: str


class InvestigationReport(BaseModel):
    risk_level: str
    risk_score: int = Field(ge=0, le=100)
    evidence: list[str]
    possible_fraud_pattern: str
    suggested_action: str
    review_caveats: list[str]


class InvestigationResponse(BaseModel):
    transaction_id: str
    risk_facts: TransactionRiskFacts
    report: InvestigationReport
