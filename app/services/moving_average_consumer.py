import os
import json
from kafka import KafkaConsumer
from app.core.database import SessionLocal
from app.models.symbol_average import SymbolAverage
from app.models.price import Price
from datetime import datetime

def calculate_moving_average(prices):
    if not prices:
        return None
    return sum(prices) / len(prices)

def consume_price_events():
    kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = "market.prices"

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_servers,
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='ma-consumers',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("Moving average consumer started and listening...")

    db = SessionLocal()

    try:
        for message in consumer:
            data = message.value
            symbol = data.get("symbol")
            timestamp = data.get("timestamp")

            if not symbol:
                continue

            try:
                prices = (
                    db.query(Price)
                    .filter(Price.symbol == symbol)
                    .order_by(Price.timestamp.desc())
                    .limit(5)
                    .all()
                )

                values = [p.value for p in prices]
                moving_avg = calculate_moving_average(values)

                avg = SymbolAverage(
                    symbol=symbol,
                    moving_average=moving_avg,
                    timestamp=datetime.utcnow()  # You can use the latest price timestamp if preferred
                )
                db.add(avg)
                db.commit()
                print(f"[✓] Stored 5-pt MA for {symbol}: {moving_avg}")

            except Exception as e:
                db.rollback()
                print(f"[✗] Error: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    consume_price_events()
