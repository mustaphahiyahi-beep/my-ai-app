import streamlit as st

st.title("🤖 AI Chat بسيط")

user_input = st.text_input("اكتب سؤالك:")

if user_input:
    st.write("انت قلت:", user_input)
