import re
from functools import lru_cache
from pathlib import Path

from app.schemas import RetrievedRule, TransactionRiskFacts

RULES_FILE_NAME = "rules.md"

RULE_QUERY_TERMS = {
    "R001": {"large", "amount", "high-value", "history", "sudden"},
    "R002": {"new", "device", "ip", "high-value", "transaction"},
    "R003": {"country", "new", "transaction", "review"},
    "R004": {"merchant", "ip", "device", "confirmed", "fraud"},
}

GENERAL_TERMS = {
    "fraud",
    "risk",
    "review",
    "precision-recall",
    "pr-auc",
    "model",
    "score",
    "rule",
    "auditability",
}

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "before",
    "for",
    "from",
    "in",
    "is",
    "of",
    "or",
    "over",
    "the",
    "to",
    "use",
    "when",
    "with",
}


@lru_cache(maxsize=1)
def load_rule_chunks() -> list[RetrievedRule]:
    rules_path = _resolve_data_path(RULES_FILE_NAME)
    lines = rules_path.read_text(encoding="utf-8-sig").splitlines()
    chunks: list[RetrievedRule] = []
    current_heading = "Fraud Review Rules"
    chunk_index = 1

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            current_heading = stripped.lstrip("#").strip()
            continue
        if stripped.startswith("-"):
            content = stripped.lstrip("-").strip()
            chunks.append(
                RetrievedRule(
                    rule_id=f"KB{chunk_index:03d}",
                    title=current_heading,
                    source=f"data/{RULES_FILE_NAME}",
                    content=content,
                    relevance_score=0,
                    matched_terms=[],
                )
            )
            chunk_index += 1

    return chunks


def retrieve_relevant_rules(risk_facts: TransactionRiskFacts, limit: int = 4) -> list[RetrievedRule]:
    query_terms = _build_query_terms(risk_facts)
    scored_rules: list[RetrievedRule] = []

    for chunk in load_rule_chunks():
        chunk_terms = _tokenize(f"{chunk.title} {chunk.content}")
        matched_terms = sorted(query_terms & chunk_terms)
        if not matched_terms:
            continue

        title_bonus = 0.5 if risk_facts.risk_level in {"high", "medium"} and "risk" in chunk_terms else 0
        score = len(matched_terms) + title_bonus
        scored_rules.append(
            RetrievedRule(
                rule_id=chunk.rule_id,
                title=chunk.title,
                source=chunk.source,
                content=chunk.content,
                relevance_score=score,
                matched_terms=matched_terms,
            )
        )

    return sorted(
        scored_rules,
        key=lambda item: (item.relevance_score, len(item.matched_terms), item.rule_id),
        reverse=True,
    )[:limit]


def _build_query_terms(risk_facts: TransactionRiskFacts) -> set[str]:
    terms = set(GENERAL_TERMS)
    terms.update(_tokenize(risk_facts.risk_level))

    for rule_hit in risk_facts.rule_hits:
        terms.update(RULE_QUERY_TERMS.get(rule_hit.rule_id, set()))
        terms.update(_tokenize(f"{rule_hit.name} {rule_hit.description} {rule_hit.evidence}"))

    if risk_facts.model_prediction is not None:
        terms.update({"model", "score", "fraud", "threshold"})
        if risk_facts.model_prediction.predicted_label == 1:
            terms.update({"high", "risk", "fraud"})

    transaction = risk_facts.transaction
    if transaction.amount >= 500:
        terms.update({"large", "amount", "high-value"})

    return terms


def _tokenize(text: str) -> set[str]:
    normalized = text.lower().replace("high value", "high-value")
    return {
        token
        for token in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", normalized)
        if token not in STOP_WORDS
    }


def _resolve_data_path(file_name: str) -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "data" / file_name
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Could not locate data/{file_name}.")
