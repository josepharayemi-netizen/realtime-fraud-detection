from pathlib import Path
from app.model import FraudScorer
from app.schemas import Transaction
from app.storage import alerts, save


def risky():
    return Transaction(transaction_id="RISK-1", amount=20000, hour=2, country="US",
        customer_country="NG", merchant_risk=.95, velocity_1h=12, account_age_days=2)


def test_risky_transaction_has_explanations(tmp_path: Path):
    decision = FraudScorer(tmp_path / "model.joblib").score(risky())
    assert decision.decision in {"REVIEW", "BLOCK"}
    assert "COUNTRY_MISMATCH" in decision.reasons
    assert "HIGH_VELOCITY" in decision.reasons


def test_alert_is_persisted(tmp_path: Path):
    transaction = risky()
    decision = FraudScorer(tmp_path / "model.joblib").score(transaction)
    db = tmp_path / "fraud.db"
    save(transaction, decision, db)
    assert alerts(path=db)[0]["transaction_id"] == "RISK-1"
