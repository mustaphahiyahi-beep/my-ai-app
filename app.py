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
# CSS تصميم احترافي
# =============================
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    color: white;
}
.title {
    font-size: 30px;
    font-weight: bold;
    color: #38bdf8;
}
.metric {
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =============================
# Sidebar
# =============================
st.sidebar.title("🛡️ Cyber AI")
st.sidebar.write("Security Dashboard")

menu = st.sidebar.radio("Navigation", ["Dashboard", "Analyzer"])

# =============================
# Session
# =============================
if "history" not in st.session_state:
    st.session_state.history = []

# =============================
# تحليل الهجوم
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

    elif "drop table" in text.lower():
        threat = "Database Attack"
        risk = 90

    return ip, threat, risk

# =============================
# إرسال إيميل
# =============================
def send_email(message):
    sender = st.secrets["EMAIL"]
    password = st.secrets["EMAIL_PASSWORD"]

    msg = MIMEText(message)
    msg["Subject"] = "🚨 Security Alert"
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

    st.markdown('<div class="title">📊 Cyber Security Dashboard</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    total = len(st.session_state.history)
    high_risk = len([x for x in st.session_state.history if x["risk"] > 50])
    attacks = len([x for x in st.session_state.history if x["threat"] != "Normal"])

    col1.metric("Total Logs", total)
    col2.metric("High Risk", high_risk)
    col3.metric("Attacks", attacks)

    st.write("")

    for item in reversed(st.session_state.history):
        st.markdown(f"""
        <div class="card">
        ⏰ {item['time']} <br>
        🌐 IP: {item['ip']} <br>
        ⚠️ Threat: {item['threat']} <br>
        🔥 Risk: {item['risk']}%
        </div>
        """, unsafe_allow_html=True)

# =============================
# Analyzer
# =============================
if menu == "Analyzer":

    st.markdown('<div class="title">🧠 AI Analyzer</div>', unsafe_allow_html=True)

    user_input = st.text_area("Enter logs or request:")

    if st.button("🚀 Analyze"):

        if user_input.strip() == "":
            st.warning("⚠️ Please enter data")
        else:
            ip, threat, risk = analyze_input(user_input)

            st.markdown(f"""
            <div class="card">
            🌐 IP: {ip} <br>
            ⚠️ Threat: {threat} <br>
            🔥 Risk: {risk}%
            </div>
            """, unsafe_allow_html=True)

            # حفظ
            st.session_state.history.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip": ip,
                "threat": threat,
                "risk": risk
            })

            # إرسال إيميل تلقائي
            if risk >= 50:
                send_email(f"""
🚨 Attack Detected!

IP: {ip}
Threat: {threat}
Risk: {risk}%
Time: {datetime.now()}
""")
                st.success("📩 Email Sent!")
