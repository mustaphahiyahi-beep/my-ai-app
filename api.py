from fastapi import FastAPI
import re
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

app = FastAPI()

# =========================
# تحليل الهجمات
# =========================
def analyze_input(text):
    ip_match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
    ip = ip_match.group(0) if ip_match else "Unknown"

    threat = "Normal"
    risk = 0

    if "sql" in text.lower() or "' or 1=1" in text.lower():
        threat = "SQL Injection"
        risk = 80

    elif "script" in text.lower():
        threat = "XSS Attack"
        risk = 70

    elif "drop table" in text.lower():
        threat = "Database Attack"
        risk = 90

    return ip, threat, risk

# =========================
# إرسال إيميل
# =========================
def send_email(message):
    sender = "your_email@gmail.com"
    password = "your_app_password"

    msg = MIMEText(message)
    msg["Subject"] = "🚨 Security Alert"
    msg["From"] = sender
    msg["To"] = sender

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, sender, msg.as_string())
    server.quit()

# =========================
# API Endpoint
# =========================
@app.post("/analyze")
def analyze(data: dict):
    text = data.get("text", "")

    ip, threat, risk = analyze_input(text)

    # إرسال إيميل تلقائي
    if risk >= 50:
        send_email(f"""
🚨 Attack Detected!

Time: {datetime.now()}
IP: {ip}
Threat: {threat}
Risk: {risk}%
""")

    return {
        "ip": ip,
        "threat": threat,
        "risk": risk
    }
