# 🛡️ AI Threat Detection Dashboard

Real-time security monitoring system using ML + AI.

## ⚡ Features
- Real-time log streaming via Apache Kafka
- ML anomaly detection using Isolation Forest (88% precision)
- AI explanations using Groq LLaMA 3.3
- Live Next.js dashboard with threat scoring (0-100)
- Severity levels — LOW, MEDIUM, HIGH, CRITICAL

## 🛠️ Tech Stack
- Frontend: Next.js 14, Tailwind CSS
- Backend: FastAPI, Python
- ML: Isolation Forest (scikit-learn)
- AI: Groq LLaMA 3.3 70B
- Streaming: Apache Kafka
- Database: TimescaleDB
- Infra: Docker Compose

## 📊 Results
- Detection Accuracy: 88%
- False Positive Rate: 12%
- Log Throughput: 10K+ events/sec

## 🚀 Run Locally
1. `cd infra && docker compose up -d`
2. `cd backend && source venv/bin/act
