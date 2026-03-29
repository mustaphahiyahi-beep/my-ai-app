import streamlit as st
import google.generativeai as genai

st.title("🤖 AI Cyber Assistant (Gemini)")

# ✅ جلب API Key
genai.configure(api_key="ضع المفتاح هنا")

# ✅ اختيار النموذج
model = genai.GenerativeModel("gemini-pro")

# واجهة المستخدم
user_input = st.text_input("💬 اسأل:")

if st.button("اسأل"):
    if user_input:
        with st.spinner("جاري التفكير..."):
            try:
                response = model.generate_content(user_input)
                st.success(response.text)
            except Exception as e:
                st.error(f"خطأ: {e}")
    else:
        st.warning("اكتب سؤال أولاً")
