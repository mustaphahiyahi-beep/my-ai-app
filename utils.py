import hashlib
import requests
import streamlit as st
import smtplib
from email.mime.text import MIMEText

# 🦠 Malware Scanner
def scan_file(file):
    content = file.read()
    file_hash = hashlib.md5(content).hexdigest()

    if b"virus" in content:
        return "Malicious"
    return "Safe"

# 📩 Telegram
def send_telegram_alert(message):
    try:
        token = st.secrets["TELEGRAM_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]

        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": chat_id, "text": message}
        )
    except:
        pass

# 📧 Email
def send_email_alert(message):
    try:
        sender = st.secrets["EMAIL"]
        password = st.secrets["EMAIL_PASSWORD"]

        msg = MIMEText(message)
        msg["Subject"] = "🚨 Security Alert"
        msg["From"] = sender
        msg["To"] = sender

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
    except:
        pass

# 🚫 Firewall (محاكاة)
def block_ip(ip):
    print(f"[BLOCKED] {ip}")
