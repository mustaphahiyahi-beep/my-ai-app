import streamlit as st

st.set_page_config(layout="wide")

st.title("🛡️ Cybersecurity AI Agent Pro")

st.header("📊 Log Analyzer")

logs = st.text_area("📥 أدخل Logs:")

if st.button("تحليل"):
    if logs:
        st.success("تم استلام البيانات ✅")
        st.write(logs)
    else:
        st.warning("يرجى إدخال Logs")

st.header("🤖 AI Cyber Assistant")

question = st.text_input("💬 اسأل عن الأمن السيبراني:")

if st.button("اسأل"):
    if question:
        st.success("سؤالك: ")
        st.write(question)
    else:
        st.warning("اكتب سؤال أولاً")
