import json
import psycopg2
from kafka import KafkaConsumer
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

consumer = KafkaConsumer(
    'security-logs',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

def save_to_db(log):
    cursor.execute("""
        INSERT INTO logs (ip, endpoint, method, status_code, response_time)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        log['ip'],
        log['endpoint'],
        log['method'],
        log['status_code'],
        log['response_time']
    ))
    conn.commit()

print("Consumer chalu... logs sun raha hoon")
for message in consumer:
    log = message.value
    save_to_db(log)
    print(f"💾 Saved: {log['ip']} - {log['endpoint']} - {log['status_code']}")