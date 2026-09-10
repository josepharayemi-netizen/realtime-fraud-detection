import json
import os
import random
import time
import uuid
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BROKER", "localhost:19092"),
    value_serializer=lambda value: json.dumps(value).encode(),
)
countries = ["NG", "GB", "US", "ZA", "KE"]
while True:
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "amount": round(random.lognormvariate(6, 1.5), 2),
        "hour": random.randrange(24),
        "country": random.choice(countries),
        "customer_country": random.choice(countries),
        "merchant_risk": round(random.random(), 2),
        "velocity_1h": random.randrange(12),
        "account_age_days": random.randrange(1500),
    }
    producer.send("transactions", transaction)
    producer.flush()
    print("published", transaction["transaction_id"])
    time.sleep(2)
