from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from app.model import FraudScorer
from app.schemas import Decision, Transaction
from app.storage import alerts, save

app = FastAPI(title="Real-Time Fraud Detection API", version="1.0.0")
scorer = FraudScorer()
SCORED = Counter("transactions_scored_total", "Transactions scored", ["decision"])
LATENCY = Histogram("fraud_scoring_seconds", "Fraud scoring latency")


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}


@app.post("/score", response_model=Decision)
def score(transaction: Transaction):
    with LATENCY.time():
        decision = scorer.score(transaction)
        save(transaction, decision)
        SCORED.labels(decision.decision).inc()
        return decision


@app.get("/alerts")
def recent_alerts(limit: int = 50):
    return alerts(min(limit, 200))


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
