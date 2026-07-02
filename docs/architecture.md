# Architecture

## High-Level Flow

1. User submits a transaction ID in the dashboard.
2. Backend retrieves transaction profile and related entities.
3. Agent calls tools for rule hits, historical behavior, device/IP risk, and merchant context.
4. RAG retrieves relevant fraud rules and review guidelines.
5. Agent generates a structured investigation report.
6. Frontend displays risk score, evidence chain, timeline, and suggested action.

## Main Modules

- `backend/`: API service and data access layer.
- `agent/`: tool definitions, prompts, and investigation workflow.
- `frontend/`: risk investigation dashboard.
- `data/`: synthetic sample data and rule documents.
- `docs/`: architecture, resume notes, and design decisions.
