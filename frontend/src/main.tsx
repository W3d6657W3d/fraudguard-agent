import React from "react";
import ReactDOM from "react-dom/client";
import { AlertTriangle, FileSearch, Loader2, Search, ShieldCheck } from "lucide-react";

import "./styles.css";

type Transaction = {
  transaction_id: string;
  user_id: string;
  merchant_id: string;
  device_id: string;
  ip: string;
  country: string;
  amount: number;
  event_time: string;
  label: number;
};

type EntityEvidence = {
  user_transaction_count: number;
  user_average_amount: number | null;
  user_max_amount: number | null;
  user_known_countries: string[];
  device_transaction_count: number;
  device_user_count: number;
  ip_transaction_count: number;
  ip_user_count: number;
  merchant_transaction_count: number;
  merchant_confirmed_fraud_count: number;
};

type RuleHit = {
  rule_id: string;
  name: string;
  severity: string;
  description: string;
  evidence: string;
  score_impact: number;
};

type InvestigationReport = {
  risk_level: string;
  risk_score: number;
  evidence: string[];
  possible_fraud_pattern: string;
  suggested_action: string;
  review_caveats: string[];
};

type TransactionRiskFacts = {
  transaction: Transaction;
  entity_evidence: EntityEvidence;
  rule_hits: RuleHit[];
  risk_score: number;
  risk_level: string;
};

type InvestigationResponse = {
  transaction_id: string;
  risk_facts: TransactionRiskFacts;
  report: InvestigationReport;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

function App() {
  const [transactionId, setTransactionId] = React.useState("T1002");
  const [result, setResult] = React.useState<InvestigationResponse | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [isLoading, setIsLoading] = React.useState(false);

  async function analyzeTransaction(event?: React.FormEvent) {
    event?.preventDefault();
    const normalizedId = transactionId.trim();
    if (!normalizedId) {
      setError("Enter a transaction ID to analyze.");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/investigations/${encodeURIComponent(normalizedId)}`);
      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail ?? `Request failed with status ${response.status}`);
      }
      setResult(await response.json());
    } catch (requestError) {
      setResult(null);
      setError(requestError instanceof Error ? requestError.message : "Unable to analyze transaction.");
    } finally {
      setIsLoading(false);
    }
  }

  React.useEffect(() => {
    void analyzeTransaction();
  }, []);

  const facts = result?.risk_facts;
  const report = result?.report;

  return (
    <main className="app-shell">
      <section className="topbar">
        <div>
          <p className="eyebrow">FraudGuard Agent</p>
          <h1>Real-time transaction investigation</h1>
        </div>
        <div className="status-pill">
          <ShieldCheck size={18} />
          Mock Agent mode
        </div>
      </section>

      <section className="query-band">
        <form className="query-form" onSubmit={analyzeTransaction}>
          <label htmlFor="transaction-id">Transaction ID</label>
          <div className="query-controls">
            <input
              id="transaction-id"
              value={transactionId}
              onChange={(event) => setTransactionId(event.target.value.toUpperCase())}
              placeholder="T1002"
            />
            <button type="submit" disabled={isLoading}>
              {isLoading ? <Loader2 className="spin" size={18} /> : <Search size={18} />}
              Analyze
            </button>
          </div>
        </form>
        <div className="sample-ids" aria-label="Sample transaction IDs">
          {["T1001", "T1002", "T1003", "T1004"].map((id) => (
            <button key={id} type="button" onClick={() => setTransactionId(id)}>
              {id}
            </button>
          ))}
        </div>
      </section>

      {error && (
        <section className="error-banner">
          <AlertTriangle size={18} />
          {error}
        </section>
      )}

      {facts && report && (
        <section className="dashboard-grid">
          <RiskSummary facts={facts} report={report} />
          <TransactionDetails transaction={facts.transaction} />
          <EvidencePanel facts={facts} report={report} />
          <AgentReport report={report} />
        </section>
      )}
    </main>
  );
}

function RiskSummary({ facts, report }: { facts: TransactionRiskFacts; report: InvestigationReport }) {
  return (
    <section className="panel risk-panel">
      <div>
        <p className="panel-kicker">Risk decision</p>
        <h2 className={`risk-label ${facts.risk_level}`}>{facts.risk_level}</h2>
      </div>
      <div className="score-block">
        <span>{facts.risk_score}</span>
        <p>risk score</p>
      </div>
      <div className="pattern-line">
        <FileSearch size={18} />
        {report.possible_fraud_pattern}
      </div>
    </section>
  );
}

function TransactionDetails({ transaction }: { transaction: Transaction }) {
  const rows = [
    ["Transaction", transaction.transaction_id],
    ["User", transaction.user_id],
    ["Merchant", transaction.merchant_id],
    ["Device", transaction.device_id],
    ["IP", transaction.ip],
    ["Country", transaction.country],
    ["Amount", formatAmount(transaction.amount)],
    ["Event time", transaction.event_time],
  ];

  return (
    <section className="panel">
      <p className="panel-kicker">Transaction details</p>
      <div className="detail-grid">
        {rows.map(([label, value]) => (
          <div className="detail-row" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

function EvidencePanel({ facts, report }: { facts: TransactionRiskFacts; report: InvestigationReport }) {
  const evidence = facts.entity_evidence;

  return (
    <section className="panel evidence-panel">
      <p className="panel-kicker">Evidence chain</p>
      <div className="metric-row">
        <Metric label="User history" value={String(evidence.user_transaction_count)} />
        <Metric label="Device txns" value={String(evidence.device_transaction_count)} />
        <Metric label="IP users" value={String(evidence.ip_user_count)} />
        <Metric label="Merchant fraud" value={String(evidence.merchant_confirmed_fraud_count)} />
      </div>

      <div className="rule-list">
        {facts.rule_hits.length > 0 ? (
          facts.rule_hits.map((rule) => (
            <article className="rule-card" key={rule.rule_id}>
              <div>
                <span className={`severity ${rule.severity}`}>{rule.severity}</span>
                <h3>{rule.rule_id}: {rule.name}</h3>
              </div>
              <p>{rule.evidence}</p>
            </article>
          ))
        ) : (
          <article className="rule-card">
            <h3>No rule hit</h3>
            <p>No high-risk rule was triggered for this transaction.</p>
          </article>
        )}
      </div>

      <ol className="evidence-list">
        {report.evidence.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ol>
    </section>
  );
}

function AgentReport({ report }: { report: InvestigationReport }) {
  return (
    <section className="panel agent-panel">
      <p className="panel-kicker">Mock Agent report</p>
      <div className="action-box">
        <span>Suggested action</span>
        <strong>{report.suggested_action}</strong>
      </div>
      <div>
        <h3>Review caveats</h3>
        <ul>
          {report.review_caveats.map((caveat) => (
            <li key={caveat}>{caveat}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function formatAmount(amount: number) {
  return new Intl.NumberFormat("en-AU", {
    style: "currency",
    currency: "AUD",
  }).format(amount);
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
