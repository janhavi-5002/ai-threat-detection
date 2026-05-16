from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_threat(threat: dict) -> str:
    if threat['threat_score'] < 70:
        return "Low risk activity — no action needed."
    
    prompt = f"""
    You are a cybersecurity expert. Analyze this threat in 2-3 simple sentences:
    
    IP Address: {threat['ip']}
    Threat Score: {threat['threat_score']}/100
    Failed Login Ratio: {int(threat['failed_ratio']*100)}%
    Total Requests: {threat['total_requests']}
    Severity: {threat['severity']}
    
    Explain: what attack this is, why suspicious, what action to take.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    
    return response.choices[0].message.content

def explain_all_threats(threats: list) -> list:
    results = []
    for threat in threats:
        if threat['is_threat']:
            threat['explanation'] = explain_threat(threat)
        else:
            threat['explanation'] = "Normal traffic — no suspicious activity."
        results.append(threat)
    return results