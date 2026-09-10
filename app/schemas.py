from pydantic import BaseModel, Field


class Transaction(BaseModel):
    transaction_id: str = Field(min_length=1)
    amount: float = Field(gt=0)
    hour: int = Field(ge=0, le=23)
    country: str = Field(min_length=2, max_length=2)
    customer_country: str = Field(min_length=2, max_length=2)
    merchant_risk: float = Field(ge=0, le=1)
    velocity_1h: int = Field(ge=0)
    account_age_days: int = Field(ge=0)


class Decision(BaseModel):
    transaction_id: str
    risk_score: float
    decision: str
    reasons: list[str]
