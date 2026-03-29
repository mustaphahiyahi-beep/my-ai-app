import streamlit as st
import google.generativeai as genai

st.title("🤖 AI Cyber Assistant (Fast)")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 🔥 نموذج سريع
model = genai.GenerativeModel("gemini-1.5-flash")

user_input = st.text_input("💬 اسأل:")

if st.button("اسأل"):
    if user_input:
        with st.spinner("⏳ جاري التفكير..."):
            try:
                response = model.generate_content(
                    user_input,
                    request_options={"timeout": 10}  # ⏱️ يمنع التعليق
                )

                if response.text:
                    st.success(response.text)
                else:
                    st.warning("لم يتم توليد رد 😅")

            except Exception as e:
                st.error(f"خطأ: {e}")
    else:
        st.warning("اكتب سؤال أولاً")
