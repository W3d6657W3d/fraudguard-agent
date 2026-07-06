# Demo Guide

## What To Show

Use transaction `T1002` for the main demo. It produces a clear high-risk investigation:

- High transaction amount.
- High XGBoost model fraud probability.
- No prior user transaction history.
- New device and IP context.
- High risk score and manual review suggestion.

## Local Demo Flow

1. Start the backend:

```bash
cd backend
uvicorn app.main:app --reload
```

2. Start the frontend:

```bash
cd frontend
pnpm install
pnpm run dev
```

3. Open the dashboard:

```text
http://127.0.0.1:5173
```

4. Enter `T1002` and click Analyze.

## Docker Demo Flow

From the repository root:

```bash
docker compose up --build
```

Then open:

```text
http://127.0.0.1:5173
```

## Screenshot Checklist

Capture the dashboard after analyzing `T1002`. A good resume or README screenshot should show:

- Transaction ID search box.
- High risk level and score.
- Model fraud probability.
- Matched rule cards.
- Evidence chain.
- Mock Agent suggested action.
