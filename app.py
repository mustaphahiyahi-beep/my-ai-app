import streamlit as st
import requests
import json
import uuid

# =========================
# 🔐 CONFIG (عدلهم)
# =========================
FIREBASE_API_KEY = "AIzaSyAkpimXjXJlmK9jg8peVugH4r4Zpz3szis"
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/test_xxx"  # ضع رابط الدفع

st.set_page_config(page_title="Cyber AI SaaS", layout="centered")

st.title("🛡️ Cyber AI SaaS")

# =========================
# SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

# =========================
# MENU
# =========================
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu, key="menu")

import streamlit as st
import requests

API_KEY = "AIzaSyAkpimXjXJlmK9jg8peVugH4r4Zpz3szis"

st.title("Cyber AI SaaS")

# ================= SIGNUP =================
st.header("Create Account")

signup_email = st.text_input("Email", key="signup_email")
signup_password = st.text_input("Password", type="password", key="signup_password")

if st.button("Signup"):
    if signup_email.strip() != "" and signup_password.strip() != "":
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"

        payload = {
            "email": signup_email,
            "password": signup_password,
            "returnSecureToken": True
        }

        res = requests.post(url, json=payload)
        data = res.json()

        if "error" in data:
            st.error(data["error"]["message"])
        else:
            st.success("Account created successfully 🎉")

    else:
        st.warning("Please enter email and password")

# ================= LOGIN =================
st.header("Login")

login_email = st.text_input("Email", key="login_email")
login_password = st.text_input("Password", type="password", key="login_password")

if st.button("Login"):
    if login_email.strip() != "" and login_password.strip() != "":
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

        payload = {
            "email": login_email,
            "password": login_password,
            "returnSecureToken": True
        }

        res = requests.post(url, json=payload)
        data = res.json()

        if "error" in data:
            st.error(data["error"]["message"])
        else:
            st.success("Logged in successfully 🚀")

    else:
        st.warning("Please enter email and password")

# =========================
# 📊 DASHBOARD
# =========================
if st.session_state.user:

    st.write("---")
    st.subheader(f"Welcome {st.session_state.user['email']} 👋")

    # 🔑 API KEY
    if "api_key" not in st.session_state:
        st.session_state.api_key = str(uuid.uuid4())

    st.write("### 🔑 Your API Key")
    st.code(st.session_state.api_key)

    # 📊 Fake Analytics
    st.write("### 📊 Usage")
    st.metric("Requests Today", "23")
    st.metric("Threats Blocked", "5")

    # 💳 Stripe Payment
    st.write("### 💳 Upgrade Plan")
    st.link_button("Upgrade to Pro 🚀", STRIPE_PAYMENT_LINK)

    # 🚪 Logout
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
