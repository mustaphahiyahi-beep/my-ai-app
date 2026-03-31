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

# =========================
# 🔐 SIGNUP (Firebase)
# =========================
if choice == "Signup":
    st.subheader("Create Account")

    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_pass")

    if st.button("Signup", key="signup_btn"):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"

        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        res = requests.post(url, data=json.dumps(data))

        if res.status_code == 200:
            st.success("Account created ✅")
        else:
            st.error(res.json())

# =========================
# 🔑 LOGIN (Firebase REAL)
# =========================
elif choice == "Login":
    st.subheader("Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        res = requests.post(url, data=json.dumps(data))

        if res.status_code == 200:
            st.session_state.user = res.json()
            st.success("Logged in 🚀")
        else:
            st.error("Invalid credentials")

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
