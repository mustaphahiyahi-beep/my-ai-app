import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText
import re
import firebase_admin


st.title("🛡️ Cyber AI SaaS")

def login_page():
    st.subheader("Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):
        st.success("Welcome 🚀")


def signup_page():
    st.subheader("Create Account")

    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_pass")

    if st.button("Create Account", key="signup_btn"):
        st.success("Account created ✅")


menu = st.selectbox("Choose", ["Login", "Sign Up"])

if menu == "Login":
    login_page()
else:
    signup_page()


# ----------- NAVIGATION -----------

menu = st.selectbox("Choose", ["Login", "Sign Up"])

# ⚠️ هذا هو المهم
if menu == "Login":
    login_page()

elif menu == "Sign Up":
    signup_page()
        
# ===============================
# Firebase Setup
# ===============================
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ===============================
# Email Alert Function
# ===============================
def send_email(ip, threat, risk):
    sender = "YOUR_EMAIL@gmail.com"
    password = "YOUR_APP_PASSWORD"
    receiver = sender

    msg = MIMEText(f"""
🚨 Cyber Security Alert

IP: {ip}
Threat: {threat}
Risk: {risk}%
""")

    msg['Subject'] = "🚨 Security Alert"
    msg['From'] = sender
    msg['To'] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
    except:
        pass

# ===============================
# AI Threat Detection
# ===============================
def analyze(text):
    threats = []
    risk = 0

    if re.search(r"(UNION|SELECT|DROP|OR 1=1)", text, re.I):
        threats.append("SQL Injection")
        risk += 40

    if "<script>" in text:
        threats.append("XSS Attack")
        risk += 30

    if "Failed login" in text:
        threats.append("Brute Force")
        risk += 20

    if risk == 0:
        threats.append("Safe")

    return ", ".join(threats), min(risk, 100)

# ===============================
# Auth UI
# ===============================
st.title("🛡️ Cyber AI SaaS")

menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

# ===============================
# SIGNUP
# ===============================
if choice == "Signup":
    st.subheader("Create Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        try:
            user = auth.create_user(email=email, password=password)
            st.success("Account created!")
        except:
            st.error("Error creating account")

# ===============================
# LOGIN
# ===============================
if choice == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state["user"] = email
        st.success("Logged in!")

# ===============================
# MAIN APP
# ===============================
if "user" in st.session_state:

    st.sidebar.success(f"👤 {st.session_state['user']}")

    st.header("📡 Send Log")

    log = st.text_area("Paste Log")

    if st.button("Analyze"):
        ip = "Unknown"

        threat, risk = analyze(log)

        data = {
            "user": st.session_state["user"],
            "log": log,
            "threat": threat,
            "risk": risk,
            "time": datetime.datetime.now()
        }

        db.collection("logs").add(data)

        if risk > 20:
            send_email(ip, threat, risk)

        st.success("Analyzed!")
        st.write(f"Threat: {threat}")
        st.write(f"Risk: {risk}%")

    # ===============================
    # Dashboard
    # ===============================
    st.header("📊 Dashboard")

    logs = db.collection("logs").stream()

    data_list = []
    for doc in logs:
        data_list.append(doc.to_dict())

    if data_list:
        df = pd.DataFrame(data_list)

        st.metric("Total Logs", len(df))
        st.metric("Detected Attacks", len(df[df["risk"] > 0]))

        st.line_chart(df["risk"])

        st.dataframe(df)

    else:
        st.info("No logs yet")

    # ===============================
    # Logout
    # ===============================
    if st.sidebar.button("Logout"):
        del st.session_state["user"]
