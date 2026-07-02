# Project Context: FraudGuard Agent

## Current Goal

Build a resume-worthy AI project focused on a real-time fraud investigation Agent. The project should complement prior experience in image classification deployment and Alibaba fraud transaction detection internship work.

## Positioning

FraudGuard Agent is not just another fraud classification model. It is an analyst-assist system for in-transaction fraud scenarios. It emphasizes:

- Real-time risk investigation
- Highly imbalanced fraud data
- PR-AUC-oriented evaluation thinking
- Threshold trade-offs between false positives and missed fraud
- Evidence-chain generation
- Tool calling and RAG-style rule retrieval
- Human-in-the-loop review

## Existing Background

The user already has:

- An image classification project for garbage recognition with frontend/backend deployment and Docker.
- Alibaba internship experience in fraud transaction detection.
- Fraud analysis experience involving business scenario analysis, in-transaction anti-fraud, imbalanced datasets, and PR-AUC selection.

Because of this, the project should avoid looking like a repeated fraud binary-classification task. It should highlight Agent/RAG/tool-calling capability while still using fraud domain knowledge as the differentiator.

## Recommended Project Name

FraudGuard Agent

## One-Line Description

A real-time fraud investigation Agent that uses transaction profiling, rule retrieval, tool calling, and evidence-based report generation to assist fraud analysts.

## Local Project Path

D:\Projects\fraudguard-agent

## Created Structure

- README.md
- backend/
- frontend/
- agent/
- data/
- docs/
- docker-compose.yml
- .env.example
- .gitignore

The local Git repository has already been initialized with `git init`, but no GitHub remote or commit has been created yet.

## MVP Plan

### Step 1: Backend Transaction Query

Implement FastAPI endpoints:

- `GET /health`
- `GET /transactions/{transaction_id}`
- `GET /investigations/{transaction_id}`

The backend should read `data/sample_transactions.csv`, aggregate basic entity evidence, match simple fraud rules, and return structured risk facts.

### Step 2: Mock Agent

Before connecting any paid or external LLM API, create a deterministic local mock Agent. It should transform transaction facts and rule hits into a structured investigation report:

- risk_level
- risk_score
- evidence
- possible_fraud_pattern
- suggested_action
- review_caveats

This makes the project runnable without API keys and easier to test.

### Step 3: Frontend Dashboard

Create a React dashboard where a user can enter a transaction ID and see:

- transaction details
- risk score and level
- rule hits
- evidence chain
- Agent-generated investigation report

### Step 4: LLM/RAG Upgrade

After the MVP works, add optional LLM support:

- Start with mock/local mode as default.
- Add OpenAI-compatible API support through environment variables.
- Add RAG retrieval over `data/rules.md` and future case notes.
- Keep fallback behavior so the project still runs without external API access.

## Agent Model Strategy

Do not start by depending on a free third-party API. Free APIs are often unstable, rate-limited, or hard to present professionally in a resume project.

Preferred strategy:

1. Build a deterministic mock Agent first.
2. Design a clean `LLMProvider` interface.
3. Add optional providers later:
   - OpenAI-compatible API
   - local Ollama model
   - other OpenAI-compatible hosted model
4. Keep mock mode as the default for reproducible demos.

## Future New-Chat Prompt

When opening a new Codex conversation, use this prompt:

"Please continue the FraudGuard Agent project at `D:\Projects\fraudguard-agent`. First read `docs/project_context.md`, then inspect the repo, and continue with the next MVP step. The current priority is implementing the backend transaction query and mock investigation Agent."

## Resume Direction

Chinese resume bullet draft:

构建面向事中反欺诈场景的智能风险研判 Agent，集成交易画像查询、规则检索、风险特征分析与证据链生成能力；通过工具调用和 RAG 检索自动生成风险研判报告，并结合人工复核反馈优化分析流程。

English resume bullet draft:

Built a real-time fraud investigation Agent integrating transaction profiling, rule retrieval, risk feature analysis, and evidence-chain generation. Used tool calling and RAG retrieval to produce automated risk reports and support human-in-the-loop review.
