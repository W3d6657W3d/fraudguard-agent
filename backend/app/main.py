from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import InvestigationResponse, TransactionRiskFacts
from app.services.mock_agent import build_investigation_report
from app.services.transactions import TransactionNotFoundError, get_transaction_risk_facts

app = FastAPI(title="FraudGuard Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/transactions/{transaction_id}", response_model=TransactionRiskFacts)
def read_transaction(transaction_id: str) -> TransactionRiskFacts:
    try:
        return get_transaction_risk_facts(transaction_id)
    except TransactionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/investigations/{transaction_id}", response_model=InvestigationResponse)
def read_investigation(transaction_id: str) -> InvestigationResponse:
    try:
        risk_facts = get_transaction_risk_facts(transaction_id)
    except TransactionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return InvestigationResponse(
        transaction_id=risk_facts.transaction.transaction_id,
        risk_facts=risk_facts,
        report=build_investigation_report(risk_facts),
    )
