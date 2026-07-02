# FraudGuard Agent

FraudGuard Agent is an AI risk investigation system for real-time transaction fraud analysis. It combines rule retrieval, transaction profiling, tool calling, and automated evidence-based risk reports.

## Project Positioning

This project focuses on in-transaction fraud investigation rather than offline toy classification. It is designed to show practical AI algorithm thinking: imbalanced fraud data, PR-AUC-oriented evaluation, risk threshold trade-offs, evidence chains, and human-in-the-loop review.

## Core Features

- Transaction risk investigation from a transaction ID or user ID
- Tool calling for transaction profile, device history, IP risk, merchant behavior, and rule hits
- RAG-based retrieval over fraud rules, case notes, and review guidelines
- Automated risk report generation with evidence, risk level, and suggested action
- Dashboard for transaction timeline, risk factors, and investigation summary
- Docker-based local deployment plan

## Planned Tech Stack

- Backend: FastAPI, Pydantic, SQLite/PostgreSQL
- Agent: LangGraph or lightweight custom workflow, tool calling, RAG retrieval
- Model layer: baseline risk scoring with LightGBM/XGBoost or simulated model output
- Frontend: React, TypeScript, Vite
- Deployment: Docker Compose

## Initial MVP

1. Load sample transaction, user, device, IP, merchant, and rule data.
2. Query one transaction and aggregate risk evidence.
3. Generate a structured investigation report.
4. Expose backend API for the frontend dashboard.
5. Add Docker Compose for reproducible local startup.

## Backend MVP API

Run the backend locally:

```bash
cd backend
uvicorn app.main:app --reload
```

Available endpoints:

- `GET /health`: service health check.
- `GET /transactions/{transaction_id}`: returns the transaction, entity evidence, matched rule hits, risk score, and risk level.
- `GET /investigations/{transaction_id}`: returns the same risk facts plus a deterministic mock Agent investigation report.

Example transaction IDs in `data/sample_transactions.csv`: `T1001`, `T1002`, `T1003`, `T1004`.

## Frontend Dashboard

Run the dashboard locally:

```bash
cd frontend
pnpm install
pnpm run dev
```

The dashboard calls `http://127.0.0.1:8000` by default. Set `VITE_API_BASE_URL` if the backend runs elsewhere.

## Resume Angle

Built a real-time fraud investigation Agent that integrates transaction profiling, rule retrieval, tool calling, and evidence-based risk report generation. The system targets highly imbalanced fraud scenarios and emphasizes PR-AUC-style evaluation, threshold trade-offs, and human review workflows.
