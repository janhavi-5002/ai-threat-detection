from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from dotenv import load_dotenv
from ml_engine import calculate_threat_score, get_all_threats
from gpt_explainer import explain_threat, explain_all_threats
from slack_alerts import send_slack_alert
import os

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

@app.get("/")
def root():
    return {"message": "Threat Detection API chal raha hai! 🚀"}

@app.get("/stats")
def get_stats():
    cursor.execute("SELECT COUNT(*) FROM logs WHERE status_code = 401")
    attacks = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM logs")
    total = cursor.fetchone()[0]
    return {
        "total_logs": total,
        "suspected_attacks": attacks,
        "normal_traffic": total - attacks
    }

@app.get("/logs")
def get_logs():
    cursor.execute("SELECT * FROM logs ORDER BY created_at DESC LIMIT 50")
    rows = cursor.fetchall()
    return {"logs": rows, "count": len(rows)}

@app.get("/analyze/{ip}")
def analyze_ip(ip: str):
    result = calculate_threat_score(ip)
    if result['is_threat']:
        result['explanation'] = explain_threat(result)
        send_slack_alert(result, result['explanation'])
    else:
        result['explanation'] = "Normal traffic — no suspicious activity."
    return result

@app.get("/threats")
def get_threats():
    threats = get_all_threats()
    threats_with_explanations = explain_all_threats(threats)
    return {
        "threats": threats_with_explanations,
        "total_threats": len([t for t in threats_with_explanations if t['is_threat']])
    }