from pathlib import Path
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression


def training_data(samples: int = 5000, seed: int = 42):
    rng = np.random.default_rng(seed)
    log_amount = rng.normal(6.2, 1.4, samples)
    unusual_hour = rng.binomial(1, 0.17, samples)
    mismatch = rng.binomial(1, 0.12, samples)
    merchant_risk = rng.beta(2, 5, samples)
    velocity = rng.poisson(2.0, samples)
    new_account = rng.binomial(1, 0.20, samples)
    x = np.column_stack([log_amount, unusual_hour, mismatch, merchant_risk, velocity, new_account])
    logits = -8.5 + 0.55 * log_amount + unusual_hour + 1.8 * mismatch + 3.2 * merchant_risk + 0.35 * velocity + 0.9 * new_account
    probabilities = 1 / (1 + np.exp(-logits))
    y = rng.binomial(1, probabilities)
    return x, y


def train(output: Path = Path("models/fraud_model.joblib")) -> Path:
    x, y = training_data()
    model = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    model.fit(x, y)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output)
    print(f"Model saved to {output}; fraud samples={int(y.sum())}/{len(y)}")
    return output


if __name__ == "__main__":
    train()
