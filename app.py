import streamlit as st
import smtplib
from email.mime.text import MIMEText
import re
from datetime import datetime

# =============================
# إعداد الصفحة
# =============================
st.set_page_config(page_title="Cyber AI", layout="wide")

# =============================
# CSS احترافي جداً
# =============================
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
    font-family: 'Segoe UI';
}

/* عنوان */
.title {
    font-size: 36px;
    font-weight: bold;
    background: linear-gradient(90deg, #00f5ff, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.03);
    border-radius: 18px;
    padding: 20px;
    margin-top: 15px;
    border: 1px solid rgba(0,255,255,0.1);
    box-shadow: 0 0 25px rgba(0,255,255,0.08);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.02);
    box-shadow: 0 0 35px rgba(0,255,255,0.2);
}

/* زر */
.stButton>button {
    background: linear-gradient(90deg, #00f5ff, #6366f1);
    border: none;
    border-radius: 12px;
    height: 45px;
    color: white;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
}

/* input */
textarea {
    border-radius: 10px !important;
}

/* Metrics */
.metric {
    font-size: 28px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =============================
# Sidebar
# =============================
st.sidebar.markdown("## 🛡️ Cyber AI")
menu = st.sidebar.radio("", ["Dashboard", "Analyzer"])

# =============================
# Session
# =============================
if "history" not in st.session_state:
    st.session_state.history = []

# =============================
# تحليل
# =============================
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

# =============================
# إيميل
# =============================
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

# =============================
# Dashboard
# =============================
if menu == "Dashboard":

    st.markdown('<div class="title">⚡ Cyber Security Dashboard</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    total = len(st.session_state.history)
    attacks = len([x for x in st.session_state.history if x["threat"] != "Normal"])
    high = len([x for x in st.session_state.history if x["risk"] > 50])

    col1.markdown(f'<div class="card">📄 Total Logs<br><div class="metric">{total}</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="card">⚠️ Attacks<br><div class="metric">{attacks}</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="card">🔥 High Risk<br><div class="metric">{high}</div></div>', unsafe_allow_html=True)

    for item in reversed(st.session_state.history):
        st.markdown(f"""
        <div class="card">
        ⏰ {item['time']}<br>
        🌐 IP: {item['ip']}<br>
        ⚠️ Threat: {item['threat']}<br>
        🔥 Risk: {item['risk']}%
        </div>
        """, unsafe_allow_html=True)

# =============================
# Analyzer
# =============================
if menu == "Analyzer":

    st.markdown('<div class="title">🧠 AI Analyzer</div>', unsafe_allow_html=True)

    user_input = st.text_area("Paste logs or attack data...")

    if st.button("🚀 Analyze"):

        if user_input.strip() == "":
            st.warning("Enter data")
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
