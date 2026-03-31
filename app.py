import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# ================================
# Firebase Setup (مرة واحدة فقط)
# ================================
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")  # تأكد الملف موجود
    firebase_admin.initialize_app(cred)

# ================================
# إعداد الصفحة
# ================================
st.set_page_config(page_title="Cyber AI SaaS", layout="centered")

st.title("🛡️ Cyber AI SaaS")

# ================================
# Menu
# ================================
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu, key="main_menu")

# ================================
# SIGNUP
# ================================
if choice == "Signup":
    st.subheader("Create Account")

    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_pass")

    if st.button("Signup", key="signup_btn"):
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            st.success("Account created successfully ✅")
        except Exception as e:
            st.error(f"Error: {e}")

# ================================
# LOGIN
# ================================
elif choice == "Login":
    st.subheader("Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):
        # ملاحظة: Firebase Admin لا يدعم login مباشر
        # هذا تسجيل وهمي مؤقت
        st.session_state["user"] = email
        st.success("Logged in successfully 🚀")

# ================================
# Dashboard (بعد تسجيل الدخول)
# ================================
if "user" in st.session_state:
    st.write("---")
    st.subheader(f"Welcome {st.session_state['user']} 👋")

    st.write("🚀 Dashboard will be here")

    if st.button("Logout"):
        del st.session_state["user"]
        st.rerun()
