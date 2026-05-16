import requests
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(threat: dict, explanation: str):
    if threat['threat_score'] < 85:
        return
    
    emoji = "🚨" if threat['severity'] == "CRITICAL" else "⚠️"
    
    message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} Security Threat Detected!"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*IP Address:*\n{threat['ip']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Threat Score:*\n{threat['threat_score']}/100"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Severity:*\n{threat['severity']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Failed Requests:*\n{int(threat['failed_ratio']*100)}%"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*AI Analysis:*\n{explanation}"
                }
            }
        ]
    }
    
    if SLACK_WEBHOOK_URL and SLACK_WEBHOOK_URL != "placeholder":
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        if response.status_code == 200:
            print(f"✅ Slack alert sent for {threat['ip']}")
        else:
            print(f"❌ Slack alert failed: {response.status_code}")
    else:
        print(f"⚠️ Slack not configured — skipping alert for {threat['ip']}")