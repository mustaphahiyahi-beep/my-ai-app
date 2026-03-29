import streamlit as st
from groq import Groq

# API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# واجهة
st.title("🛡️ Cybersecurity AI Assistant")

user_input = st.text_area("💬 أدخل سؤالك أو Log:")

if st.button("تحليل"):
    if user_input:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional cybersecurity expert. Analyze threats, logs, attacks, and give clear technical answers."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )

            answer = response.choices[0].message.content
            st.success(answer)

        except Exception as e:
            st.error(f"❌ خطأ: {e}")
