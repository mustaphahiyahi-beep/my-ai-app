import streamlit as st
import smtplib
from email.mime.text import MIMEText
import re
from datetime import datetime

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(page_title="Cyber AI", layout="wide")

# =========================
# CSS احترافي
# =========================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #0a0f1c;
    color: white;
}

/* Title */
.main-title {
    font-size: 40px;
    font-weight: bold;
    background: linear-gradient(90deg, #00f5ff, #9b5cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Card */
.card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 20px;
    margin-top: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0px 0px 20px rgba(0,255,255,0.1);
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #00f5ff, #9b5cff);
    color: white;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
    border: none;
}

/* Input */
textarea {
    border-radius: 10px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

</style>
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
st.sidebar.title("🛡️ Cyber AI")
menu = st.sidebar.radio("", ["Dashboard", "Analyzer"])

# =========================
# Session
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

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
        threat = "XSS"
        risk = 70

    return ip, threat, risk

# =========================
# إيميل
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
# Dashboard
# =========================
if menu == "Dashboard":

    st.markdown('<div class="main-title">⚡ Cyber Dashboard</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    total = len(st.session_state.history)
    attacks = len([x for x in st.session_state.history if x["threat"] != "Normal"])
    high = len([x for x in st.session_state.history if x["risk"] > 50])

    col1.markdown(f'<div class="card">📄 Total Logs<br><b>{total}</b></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card">⚠️ Attacks<br><b>{attacks}</b></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card">🔥 High Risk<br><b>{high}</b></div>', unsafe_allow_html=True)

    for item in reversed(st.session_state.history):
        st.markdown(f"""
        <div class="card">
        ⏰ {item['time']} <br>
        🌐 {item['ip']} <br>
        ⚠️ {item['threat']} <br>
        🔥 {item['risk']}%
        </div>
        """, unsafe_allow_html=True)

# =========================
# Analyzer
# =========================
if menu == "Analyzer":

    st.markdown('<div class="main-title">🧠 AI Analyzer</div>', unsafe_allow_html=True)

    user_input = st.text_area("Paste logs or attack data...")

    if st.button("🚀 Analyze Now"):

        if user_input.strip() == "":
            st.warning("Enter something")
        else:
            ip, threat, risk = analyze_input(user_input)

            st.markdown(f"""
            <div class="card">
            🌐 IP: {ip}<br>
            ⚠️ Threat: {threat}<br>
            🔥 Risk: {risk}%
            </div>
            """, unsafe_allow_html=True)

            st.session_state.history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "ip": ip,
                "threat": threat,
                "risk": risk
            })

            if risk > 50:
                send_email(f"Attack detected: {ip} - {threat}")
                st.success("📩 Alert Sent!")
