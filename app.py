import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🤖 AI Assistant")

user_input = st.text_input("💬 اسأل:")

if st.button("إرسال"):
    if user_input:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant"
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            answer = response.choices[0].message.content
            st.success(answer)

        except Exception as e:
            st.error(f"❌ خطأ: {e}")
