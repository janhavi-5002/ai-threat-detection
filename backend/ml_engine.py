import psycopg2
import numpy as np
import joblib
import os
from dotenv import load_dotenv

load_dotenv()

model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

conn = psycopg2.connect(os.getenv("DATABASE_URL"))

def get_ip_features(ip: str):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total_requests,
            SUM(CASE WHEN status_code = 401 THEN 1 ELSE 0 END) as failed_requests,
            COUNT(DISTINCT endpoint) as unique_endpoints,
            AVG(response_time) as avg_response_time
        FROM logs 
        WHERE ip = %s
        AND created_at > NOW() - INTERVAL '1 hour'
    """, (ip,))
    row = cursor.fetchone()
    return {
        'total_requests': int(row[0] or 0),
        'failed_requests': int(row[1] or 0),
        'unique_endpoints': int(row[2] or 0),
        'avg_response_time': float(row[3] or 0)
    }

def calculate_threat_score(ip: str) -> dict:
    features = get_ip_features(ip)
    
    total = features['total_requests']
    if total == 0:
        return {
            "ip": ip,
            "threat_score": 0.0,
            "severity": "LOW",
            "failed_ratio": 0.0,
            "total_requests": 0,
            "is_threat": False
        }
    
    failed_ratio = features['failed_requests'] / total
    
    X = [[
        features['total_requests'],
        failed_ratio,
        features['unique_endpoints'],
        features['avg_response_time']
    ]]
    
    X_scaled = scaler.transform(X)
    score = model.score_samples(X_scaled)[0]
    threat_score = float(min(100, max(0, (score * -1) * 50 + 50)))
    
    if threat_score >= 85 and failed_ratio > 0.5:
        severity = "CRITICAL"
    elif threat_score >= 70 and failed_ratio > 0.5:
        severity = "HIGH"
    elif threat_score >= 40 and failed_ratio > 0.3:
        severity = "MEDIUM"
    else:
        severity = "LOW"
    
    return {
        "ip": str(ip),
        "threat_score": round(threat_score, 2),
        "severity": str(severity),
        "failed_ratio": round(float(failed_ratio), 3),
        "total_requests": int(total),
        "is_threat": bool(threat_score > 70 and failed_ratio > 0.5)
    }

def get_all_threats():
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT ip FROM logs")
    ips = [row[0] for row in cursor.fetchall()]
    
    results = []
    for ip in ips:
        result = calculate_threat_score(ip)
        if result['threat_score'] > 0:
            results.append(result)
    
    results.sort(key=lambda x: x['threat_score'], reverse=True)
    return results