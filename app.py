import streamlit as st
import requests
import uuid
import google.generativeai as genai

# ==============================
# CONFIG
# ==============================

FIREBASE_API_KEY = st.secrets["FIREBASE_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ==============================
# SESSION STATE
# ==============================

if "user" not in st.session_state:
    st.session_state.user = None

if "token" not in st.session_state:
    st.session_state.token = None

# ==============================
# FUNCTIONS
# ==============================

def signup(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    res = requests.post(url, json=data)
    return res.json()

def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    res = requests.post(url, json=data)
    return res.json()

def generate_api_key():
    return "sk-" + str(uuid.uuid4())

# ==============================
# UI
# ==============================

st.title("🚀 Cyber AI SaaS")

menu = ["Signup", "Login"]
choice = st.tabs(menu)

# ==============================
# SIGNUP
# ==============================

with choice[0]:
    st.subheader("Create Account")

    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_pass")

    if st.button("Signup"):
        result = signup(email, password)

        if "error" in result:
            st.error(result["error"]["message"])
        else:
            st.success("Account created 🎉")

# ==============================
# LOGIN
# ==============================

if st.button("Login"):
    result = login(email, password)

    if "error" in result:
        st.error(result["error"]["message"])
    else:
        st.session_state.user = result["email"]
        st.session_state.token = result["idToken"]
        st.session_state.api_key = generate_api_key()

        st.success("Logged in 🎉")
        st.rerun()

# ==============================
# DASHBOARD
# ==============================

if st.session_state.user:

    st.success(f"Welcome {st.session_state.user} 👋")

    st.header("📊 Dashboard")

    st.subheader("🔑 Your API Key")
    st.code(st.session_state.api_key)

    st.subheader("🤖 AI Tool")

    prompt = st.text_area("Ask AI something")

    # Usage Limit
    LIMIT = 5

    if st.session_state.usage >= LIMIT:
        st.error("Free limit reached 🚫 Upgrade to Pro")
    else:
        if st.button("Generate"):
            if prompt:
                with st.spinner("Thinking..."):
                    try:
                        response = model.generate_content(prompt)
                        st.success(response.text)
                        st.session_state.usage += 1
                        st.info(f"Usage: {st.session_state.usage}/{LIMIT}")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Enter a prompt")

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.api_key = None
        st.session_state.usage = 0
        st.rerun()
