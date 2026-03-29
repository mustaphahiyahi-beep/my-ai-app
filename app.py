import streamlit as st
import google.generativeai as genai

st.title("🤖 AI Assistant")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-pro")

user_input = st.text_input("💬 اسأل:")

if st.button("اسأل"):
    if user_input:
        with st.spinner("⏳ جاري التفكير..."):
            try:
                response = model.generate_content(
                    user_input,
                    request_options={"timeout": 10}
                )

                if response.text:
                    st.success(response.text)
                else:
                    st.warning("لا يوجد رد 😅")

            except Exception as e:
                st.error(f"خطأ: {e}")
    else:
        st.warning("اكتب سؤال")
