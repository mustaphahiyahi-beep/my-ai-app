import streamlit as st
from groq import Groq

# API Key
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🤖 AI Cyber Assistant")

user_input = st.text_input("💬 اسأل:")

if st.button("إرسال"):
    if user_input:
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            answer = response.choices[0].message.content
            st.success(answer)

        except Exception as e:
            st.error(f"❌ خطأ: {e}")
