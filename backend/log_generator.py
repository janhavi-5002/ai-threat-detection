import random
import time
import json
from datetime import datetime

NORMAL_IPS = ["192.168.1.10", "192.168.1.11", "10.0.0.5", "10.0.0.8"]
ATTACK_IPS = ["203.45.67.89", "185.220.101.5", "45.142.212.100"]
ENDPOINTS = ["/login", "/api/users", "/dashboard", "/api/data", "/logout"]

def generate_normal_log():
    return {
        "ip": random.choice(NORMAL_IPS),
        "endpoint": random.choice(ENDPOINTS),
        "method": "GET",
        "status_code": 200,
        "response_time": random.randint(50, 300),
        "timestamp": datetime.now().isoformat(),
        "is_attack": False
    }

def generate_brute_force_log():
    return {
        "ip": random.choice(ATTACK_IPS),
        "endpoint": "/login",
        "method": "POST",
        "status_code": 401,
        "response_time": random.randint(5, 15),
        "timestamp": datetime.now().isoformat(),
        "is_attack": True
    }

def generate_log():
    if random.random() < 0.05:
        return generate_brute_force_log()
    else:
        return generate_normal_log()

if __name__ == "__main__":
    print("Log generator chalu hai... (Ctrl+C se band karo)")
    while True:
        log = generate_log()
        print(json.dumps(log, indent=2))
        time.sleep(0.5)