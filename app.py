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
model = genai.GenerativeModel("gemini-1.0-pro")

# ==============================
# SESSION
# ==============================

if "user" not in st.session_state:
    st.session_state.user = None

if "api_key" not in st.session_state:
    st.session_state.api_key = None

if "usage" not in st.session_state:
    st.session_state.usage = 0

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
    return requests.post(url, json=data).json()

def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    return requests.post(url, json=data).json()

def generate_api_key():
    return "sk-" + str(uuid.uuid4())

# ==============================
# UI
# ==============================

st.title("🚀 Cyber AI SaaS")

menu = st.radio("Choose", ["Login", "Signup"])

# ================= FORM =================
with st.form("auth_form"):

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    submit = st.form_submit_button(
        "Login" if menu == "Login" else "Signup"
    )

# ================= ACTION =================

if submit:

    if not email or not password:
        st.error("❌ Please enter email and password")

    else:

        # -------- SIGNUP --------
        if menu == "Signup":
            result = signup(email, password)

            if "error" in result:
                st.error(result["error"]["message"])
            else:
                st.success("🎉 Account created!")

        # -------- LOGIN --------
        if menu == "Login":
            result = login(email, password)

            if "error" in result:
                st.error(result["error"]["message"])
            else:
                st.session_state.user = result["email"]
                st.session_state.api_key = generate_api_key()

                st.success("🎉 Logged in!")
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

    prompt = st.text_area("Ask AI something", key="prompt_box")

    LIMIT = 5

    if st.session_state.usage >= LIMIT:
        st.error("🚫 Free limit reached")
    else:
        if st.button("Generate", key="generate_btn"):
            if not prompt:
                st.warning("⚠️ Enter a prompt")
            else:
                with st.spinner("Thinking..."):
                    try:
                        response = model.generate_content(prompt)
                        st.success(response.text)

                        st.session_state.usage += 1
                        st.info(f"Usage: {st.session_state.usage}/{LIMIT}")

                    except Exception as e:
                        st.error(f"Error: {e}")

    if st.button("Logout", key="logout_btn"):
        st.session_state.user = None
        st.session_state.api_key = None
        st.session_state.usage = 0
        st.rerun()
