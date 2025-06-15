from kafka import KafkaProducer

try:
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    print("✅ Kafka broker is reachable.")
except Exception as e:
    print("❌ Kafka broker unreachable:", e)
