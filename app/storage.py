import json
import sqlite3
from pathlib import Path
from app.schemas import Decision, Transaction

DB_PATH = Path("data/fraud.db")


def save(transaction: Transaction, decision: Decision, path: Path = DB_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS decisions (
            transaction_id TEXT PRIMARY KEY, amount REAL, risk_score REAL,
            decision TEXT, reasons TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        db.execute("""INSERT OR REPLACE INTO decisions
            (transaction_id, amount, risk_score, decision, reasons)
            VALUES (?, ?, ?, ?, ?)""",
            (transaction.transaction_id, transaction.amount, decision.risk_score,
             decision.decision, json.dumps(decision.reasons)))


def alerts(limit: int = 50, path: Path = DB_PATH) -> list[dict]:
    if not path.exists():
        return []
    with sqlite3.connect(path) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute("""SELECT * FROM decisions WHERE decision != 'APPROVE'
            ORDER BY created_at DESC LIMIT ?""", (limit,)).fetchall()
    return [dict(row) | {"reasons": json.loads(row["reasons"])} for row in rows]
