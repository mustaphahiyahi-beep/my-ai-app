import streamlit as st
from google import genai

st.title("🤖 AI Assistant (Gemini New API)")

# API KEY
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

user_input = st.text_input("💬 اسأل:")

if st.button("اسأل"):
    if user_input:
        with st.spinner("⏳ جاري التفكير..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=user_input
                )

                st.success(response.text)

            except Exception as e:
                st.error(f"خطأ: {e}")
    else:
        st.warning("اكتب سؤال أولاً")
