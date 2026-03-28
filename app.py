import streamlit as st
from openai import OpenAI
import os

st.title("🤖 AI Chat ذكي")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

user_input = st.text_input("اكتب سؤالك:")

if user_input:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )

    answer = response.choices[0].message.content
    st.write("🤖:", answer)
