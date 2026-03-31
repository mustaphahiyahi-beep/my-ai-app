import streamlit as st
import smtplib
from email.mime.text import MIMEText
import re
from datetime import datetime
import pandas as pd
import requests

# =============================
# إعداد الصفحة
# =============================
st.set_page_config(page_title="Cyber AI Pro", layout="wide")

# =============================
# تصميم احترافي (CSS)
# =============================
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}

.big-title {
    font-size: 40px;
    font-weight: bold;
    color: #00c6ff;
}

.card {
    background: #161b22;
    padding: 20px;
    border-radius: 15px;
    margin-top: 10px;
    box-shadow: 0px 0px 10px #00c6ff33;
}

button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# =============================
# Session
# =============================
if "history" not in st.session_state:
    st.session_state.history = []

# =============================
# تحليل الهجمات
# =============================
def analyze(text):
    threats = []
    risk = 0

    ip_match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
    ip = ip_match.group(0) if ip_match else "Unknown"

    if "sql" in text.lower() or "union select" in text.lower():
        threats.append("SQL Injection")
        risk += 40

    if "<script>" in text.lower():
        threats.append("XSS Attack")
        risk += 30

    if text.lower().count("failed login") >= 2:
        threats.append("Brute Force")
        risk += 30

    if risk > 50:
        send_email(ip, threats, risk)

    return ip, threats, risk

# =============================
# إرسال إيميل
# =============================
def send_email(ip, threats, risk):
    try:
        sender = st.secrets["EMAIL"]
        password = st.secrets["EMAIL_PASSWORD"]

        message = f"""
🚨 Cyber Security Alert

IP: {ip}
Threats: {', '.join(threats)}
Risk: {risk}%
"""

        msg = MIMEText(message)
        msg["Subject"] = "🚨 Alert"
        msg["From"] = sender
        msg["To"] = sender

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, sender, msg.as_string())
        server.quit()

        st.success("✅ Email sent!")

    except Exception as e:
        st.error(f"❌ Email Error: {e}")

# =============================
# IP Location
# =============================
def get_location(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return res.get("lat"), res.get("lon")
    except:
        return None, None

# =============================
# HEADER + LOGO
# =============================
st.markdown('<div class="big-title">⚡ Cyber AI Pro</div>', unsafe_allow_html=True)
st.caption("Smart Cyber Security Dashboard 🤖")

# =============================
# INPUT
# =============================
user_input = st.text_area("📥 Paste logs or attack data...", height=150)

# =============================
# ANALYZE BUTTON
# =============================
if st.button("🚀 Analyze"):

    ip, threats, risk = analyze(user_input)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if threats:
        st.error("🚨 Threat Detected!")
    else:
        st.success("✅ Safe")

    st.write(f"🌐 IP: {ip}")
    st.write(f"⚠️ Threats: {', '.join(threats) if threats else 'None'}")
    st.write(f"🔥 Risk: {risk}%")

    st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.history.append({
        "ip": ip,
        "threats": ', '.join(threats),
        "risk": risk,
        "time": datetime.now().strftime("%H:%M:%S")
    })

    if risk > 50:
        send_email(ip, threats, risk)
        st.success("📩 Email Alert Sent!")

# =============================
# DASHBOARD
# =============================
st.subheader("📊 Dashboard")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Logs", len(df))

    with col2:
        attacks = len(df[df["risk"] > 0])
        st.metric("Detected Attacks", attacks)

    # 📈 Chart
    st.subheader("📈 Risk Trend")
    st.line_chart(df["risk"])

    # 🌍 Map
    map_data = []

    for item in st.session_state.history:
        lat, lon = get_location(item["ip"])
        if lat and lon:
            map_data.append({"lat": lat, "lon": lon})

    if map_data:
        st.subheader("🌍 Attack Map")
        st.map(map_data)

    # 📜 History
    st.subheader("📜 Logs History")
    st.dataframe(df)

else:
    st.info("No data yet...")
