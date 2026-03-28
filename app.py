import streamlit as st
import requests

st.title("🛡️ Cyber Security AI Agent")

API_KEY = "sk-72885bff6559440286c83919058fbcc6"

user_input = st.text_area("📥 أدخل السؤال أو الـ Logs:")

def analyze_with_ai(text):
    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional cybersecurity expert. Analyze threats and give clear advice."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

if st.button("🔍 تحليل"):
    result = analyze_with_ai(user_input)
    st.write("🤖:", result)
