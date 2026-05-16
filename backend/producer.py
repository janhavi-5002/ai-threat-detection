import json
import time
from kafka import KafkaProducer
from log_generator import generate_log

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def start_producing():
    print("Kafka producer chalu... logs stream ho rahe hain")
    while True:
        log = generate_log()
        producer.send('security-logs', value=log)
        if log['is_attack']:
            print(f"🚨 ATTACK LOG: {log['ip']} → {log['endpoint']}")
        else:
            print(f"✅ Normal: {log['ip']} → {log['endpoint']}")
        time.sleep(0.3)

if __name__ == "__main__":
    start_producing()