import json
import os
from kafka import KafkaConsumer
from app.model import FraudScorer
from app.schemas import Transaction
from app.storage import save

consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers=os.getenv("KAFKA_BROKER", "localhost:19092"),
    group_id="fraud-scorers",
    auto_offset_reset="earliest",
    value_deserializer=lambda value: json.loads(value.decode()),
)
scorer = FraudScorer()
for message in consumer:
    transaction = Transaction(**message.value)
    decision = scorer.score(transaction)
    save(transaction, decision)
    print(decision.model_dump_json())
