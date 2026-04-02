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

email = st.text_input("Email", key="email_input")
password = st.text_input("Password", type="password", key="password_input")

# ==============================
# SIGNUP
# ==============================

if menu == "Signup":
    if st.button("Signup", key="signup_btn"):
        if not email or not password:
            st.error("❌ Please enter email and password")
        else:
            result = signup(email, password)

            if "error" in result:
                msg = result["error"]["message"]
                if msg == "EMAIL_EXISTS":
                    st.error("📧 هذا الإيميل مسجل بالفعل")
                else:
                    st.error(msg)
            else:
                st.success("🎉 Account created successfully!")

# ==============================
# LOGIN
# ==============================

if menu == "Login":
    if st.button("Login", key="login_btn"):
        if not email or not password:
            st.error("❌ Email and password required")
        else:
            result = login(email, password)

            if "error" in result:
                msg = result["error"]["message"]
                if msg == "INVALID_PASSWORD":
                    st.error("❌ كلمة المرور غير صحيحة")
                elif msg == "EMAIL_NOT_FOUND":
                    st.error("❌ الحساب غير موجود")
                else:
                    st.error(msg)
            else:
                st.session_state.user = result["email"]
                st.session_state.api_key = generate_api_key()
                st.success("🎉 Logged in successfully!")
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
