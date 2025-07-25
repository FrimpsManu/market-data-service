import os
import json
import logging
from datetime import datetime
from kafka import KafkaConsumer

from app.core.database import SessionLocal
from app.models.symbol_average import SymbolAverage
from app.models.price import Price
from app.utils.moving_average import calculate_moving_average

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def consume_price_events():
    kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = "market.prices"

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_servers,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="ma-consumers",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    logger.info("✅ Moving average consumer started and listening...")

    db = SessionLocal()

    try:
        for message in consumer:
            data = message.value
            symbol = data.get("symbol")

            if not symbol:
                logger.warning("✗ Skipping message with no symbol")
                continue

            try:
                prices = (
                    db.query(Price)
                    .filter(Price.symbol == symbol)
                    .order_by(Price.timestamp.desc())
                    .limit(5)
                    .all()
                )

                values = [p.value for p in prices if p.value is not None]
                if not values:
                    logger.warning(f"✗ No valid price values for {symbol}, skipping.")
                    continue

                moving_avg = calculate_moving_average(values)

                avg = SymbolAverage(
                    symbol=symbol,
                    moving_average=moving_avg,
                    timestamp=datetime.utcnow()  # Or use latest price timestamp if needed
                )
                db.add(avg)
                db.commit()
                logger.info(f"[✓] Stored 5-pt MA for {symbol}: {moving_avg}")

            except Exception as e:
                db.rollback()
                logger.error(f"[✗] Error while processing {symbol}: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    consume_price_events()
