import streamlit as st
import smtplib
from email.mime.text import MIMEText
import re
from datetime import datetime

# ==============================
# إعداد الصفحة
# ==============================
st.set_page_config(page_title="AI Cyber Security", layout="centered")

st.title("🛡️ AI Cyber Security Agent")
st.write("Monitor & Detect Attacks Automatically")

# ==============================
# إعداد session state
# ==============================
if "history" not in st.session_state:
    st.session_state.history = []

# ==============================
# دالة تحليل الهجوم
# ==============================
def analyze_input(text):
    ip_match = re.search(r"(\\d+\\.\\d+\\.\\d+\\.\\d+)", text)
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

    return {
        "ip": ip,
        "threat": threat,
        "risk": risk
    }

# ==============================
# دالة إرسال الإيميل
# ==============================
def send_email(subject, message):
    try:
        sender = st.secrets["EMAIL"]
        password = st.secrets["EMAIL_PASSWORD"]
        receiver = sender

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        return str(e)

# ==============================
# واجهة الإدخال
# ==============================
user_input = st.text_area("Enter logs or request:")

if st.button("🚀 Analyze"):

    if user_input.strip() == "":
        st.warning("⚠️ Please enter some data")
    else:
        result = analyze_input(user_input)

        ip = result["ip"]
        threat = result["threat"]
        risk = result["risk"]

        # عرض النتائج
        st.subheader("📊 Analysis Result")
        st.write(f"IP: {ip}")
        st.write(f"Threat: {threat}")
        st.write(f"Risk: {risk}%")

        # حفظ في history
        st.session_state.history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": ip,
            "threat": threat,
            "risk": risk
        })

        # 🚨 إرسال إيميل تلقائي
        if risk >= 50:
            email_message = f"""
🚨 Cyber Attack Detected!

Time: {datetime.now()}

IP Address: {ip}
Attack Type: {threat}
Risk Level: {risk}%

Action Taken:
✔ Logged
✔ Alert Sent

Stay Safe 🔒
"""

            result_email = send_email("🚨 Security Alert", email_message)

            if result_email == True:
                st.success("📩 Email Alert Sent Successfully!")
            else:
                st.error(f"❌ Email Error: {result_email}")

# ==============================
# عرض السجل
# ==============================
st.subheader("📜 Attack History")

if st.session_state.history:
    for item in reversed(st.session_state.history):
        st.write(item)
else:
    st.write("No attacks yet.")
