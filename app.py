import streamlit as st
import requests

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

if st.session_state.user is None:

    tab1, tab2 = st.tabs(["Signup", "Login"])

    # -------- SIGNUP --------
    with tab1:
        st.subheader("Create Account")

        with st.form("signup_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            submit = st.form_submit_button("Signup")

            if submit:
                if email.strip() != "" and password.strip() != "":
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

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            submit = st.form_submit_button("Login")

            if submit:
                if email.strip() != "" and password.strip() != "":
                    res = login(email, password)

                    if "error" in res:
                        st.error(res["error"]["message"])
                    else:
                        st.session_state.user = res
                        st.success("Logged in 🚀")
                        st.rerun()
                else:
                    st.warning("Please enter email and password")

import random
import string

def generate_api_key():
    return "sk-" + "".join(random.choices(string.ascii_letters + string.digits, k=32))


# ================= DASHBOARD =================
else:
    st.success(f"Welcome {st.session_state.user['email']} 👋")

    st.title("📊 Dashboard")

    # إنشاء API KEY إذا لم يكن موجود
    if "api_key" not in st.session_state:
        st.session_state.api_key = generate_api_key()

    st.subheader("🔑 Your API Key")
    st.code(st.session_state.api_key)

    st.info("Use this API key to access AI services")

    # مثال AI بسيط
    st.subheader("🤖 AI Tool")

    prompt = st.text_area("Ask AI something")

    if st.button("Generate"):
        if prompt:
            st.success(f"AI Response: (demo) → {prompt[::-1]}")
        else:
            st.warning("Enter a prompt")

    # Logout
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
