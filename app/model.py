from pathlib import Path
import joblib

from app.features import reasons, vectorize
from app.schemas import Decision, Transaction

MODEL_PATH = Path("models/fraud_model.joblib")


class FraudScorer:
    def __init__(self, model_path: Path = MODEL_PATH):
        if not model_path.exists():
            from app.train import train
            train(model_path)
        self.model = joblib.load(model_path)

    def score(self, transaction: Transaction) -> Decision:
        probability = float(self.model.predict_proba([vectorize(transaction)])[0][1])
        rule_reasons = reasons(transaction)
        triggers = sum(reason != "NO_MAJOR_RULE_TRIGGER" for reason in rule_reasons)
        risk = round(min(1.0, probability + min(0.18, 0.03 * triggers)), 4)
        decision = "BLOCK" if risk >= 0.80 else "REVIEW" if risk >= 0.55 else "APPROVE"
        return Decision(transaction_id=transaction.transaction_id, risk_score=risk, decision=decision, reasons=rule_reasons)
