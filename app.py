import streamlit as st
import smtplib
from email.mime.text import MIMEText
import re
from datetime import datetime

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(page_title="Cyber AI", layout="centered")

# =========================
# CSS (تصميم ChatGPT)
# =========================
st.markdown("""
<style>

html, body {
    background-color: #0f172a;
    color: white;
}

/* الرسائل */
.user-msg {
    background-color: #1e293b;
    padding: 12px;
    border-radius: 10px;
    margin: 5px 0;
    text-align: right;
}

.bot-msg {
    background-color: #020617;
    padding: 12px;
    border-radius: 10px;
    margin: 5px 0;
    border-left: 3px solid #22c55e;
}

/* زر */
.stButton>button {
    background-color: #22c55e;
    color: white;
    border-radius: 10px;
}

/* input */
textarea {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# لوجو
# =========================
st.markdown("<h2 style='text-align:center;'>🛡️ Cyber AI Assistant</h2>", unsafe_allow_html=True)

# =========================
# session
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = []

# =========================
# تحليل
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

    return ip, threat, risk

# =========================
# ايميل
# =========================
def send_email(message):
    sender = st.secrets["EMAIL"]
    password = st.secrets["EMAIL_PASSWORD"]

    msg = MIMEText(message)
    msg["Subject"] = "🚨 Alert"
    msg["From"] = sender
    msg["To"] = sender

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, sender, msg.as_string())
    server.quit()

# =========================
# عرض الشات
# =========================
for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

# =========================
# إدخال المستخدم
# =========================
user_input = st.text_area("Type your message...")

if st.button("Send"):

    if user_input.strip() != "":
        # رسالة المستخدم
        st.session_state.chat.append({"role": "user", "content": user_input})

        ip, threat, risk = analyze_input(user_input)

        # رد AI
        response = f"""
🔍 Analysis Result:

IP: {ip}  
Threat: {threat}  
Risk: {risk}%
"""

        if risk > 50:
            send_email(f"Attack detected: {ip} - {threat}")
            response += "\n🚨 Alert sent to email!"

        st.session_state.chat.append({"role": "bot", "content": response})

        st.rerun()
