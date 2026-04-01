import streamlit as st
import requests

# 🔥 ضع API KEY ديالك هنا
API_KEY = "AIzaSyAkpimXjXJlmK9jg8peVugH4r4Zpz3szis"

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= FUNCTIONS =================
def signup(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    return requests.post(url, json=payload).json()

def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    return requests.post(url, json=payload).json()

# ================= UI =================
st.title("🚀 Cyber AI SaaS")

# ================= IF NOT LOGGED =================
if st.session_state.user is None:

    tab1, tab2 = st.tabs(["Signup", "Login"])

    # -------- SIGNUP --------
    with tab1:
        st.subheader("Create Account")

        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Signup"):
            if email.strip() and password.strip():

                res = signup(email, password)

                if "error" in res:
                    st.error(res["error"]["message"])
                else:
                    st.success("Account created 🎉")

            else:
                st.warning("Please enter email and password")

    # -------- LOGIN --------
    with tab2:
        st.subheader("Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if email.strip() and password.strip():

                res = login(email, password)

                if "error" in res:
                    st.error(res["error"]["message"])
                else:
                    st.session_state.user = res
                    st.success("Logged in 🚀")
                    st.rerun()

            else:
                st.warning("Please enter email and password")

# ================= DASHBOARD =================
else:
    st.success(f"Welcome {st.session_state.user['email']} 👋")

    st.header("📊 Dashboard")

    st.write("Your user info:")
    st.json(st.session_state.user)

    # 🔑 API KEY وهمي لكل مستخدم (نطورها لاحقاً)
    st.subheader("🔑 Your API Key")
    st.code(f"API-{st.session_state.user['localId']}")

    # 💳 Placeholder للدفع (Stripe لاحقاً)
    st.subheader("💳 Subscription")
    st.info("Upgrade to Pro (Stripe integration next step)")

    # 🔴 LOGOUT
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
