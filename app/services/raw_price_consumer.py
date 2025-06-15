import os
import json
from kafka import KafkaConsumer
from app.core.database import SessionLocal
from app.models.price import Price

def consume_prices():
    kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = "market.prices"

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='price-consumers',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("Kafka consumer started and waiting for messages...")

    db = SessionLocal()

    try:
        for message in consumer:
            data = message.value
            print(f"Received message: {data}")

            try:
                price = Price(
                    symbol=data["symbol"],
                    value=float(data["value"]),
                    timestamp=data["timestamp"]
                )
                db.add(price)
                db.commit()
                print(f"Stored price for {data['symbol']}")
            except Exception as e:
                db.rollback()
                print(f"Error processing message: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    consume_prices()
