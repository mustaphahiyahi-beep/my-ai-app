import streamlit as st
import openai

st.title("🤖 AI Chat ذكي")

# ضع مفتاحك هنا
openai.api_key = "PUT-YOUR-API-KEY-HERE"

user_input = st.text_input("اكتب سؤالك:")

if user_input:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )

    answer = response.choices[0].message.content
    st.write("🤖:", answer)
