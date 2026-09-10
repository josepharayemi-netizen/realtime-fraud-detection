from app.schemas import Transaction

FEATURE_NAMES = ["log_amount", "unusual_hour", "country_mismatch", "merchant_risk", "velocity_1h", "new_account"]


def vectorize(t: Transaction) -> list[float]:
    import math
    return [
        math.log1p(t.amount),
        float(t.hour <= 4),
        float(t.country.upper() != t.customer_country.upper()),
        t.merchant_risk,
        float(t.velocity_1h),
        float(t.account_age_days < 30),
    ]


def reasons(t: Transaction) -> list[str]:
    found = []
    if t.amount >= 5000:
        found.append("HIGH_AMOUNT")
    if t.hour <= 4:
        found.append("UNUSUAL_HOUR")
    if t.country.upper() != t.customer_country.upper():
        found.append("COUNTRY_MISMATCH")
    if t.merchant_risk >= 0.75:
        found.append("HIGH_RISK_MERCHANT")
    if t.velocity_1h >= 6:
        found.append("HIGH_VELOCITY")
    if t.account_age_days < 30:
        found.append("NEW_ACCOUNT")
    return found or ["NO_MAJOR_RULE_TRIGGER"]
