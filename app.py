def ask_ai(question):
    return "AI غير مفعل حالياً"
    try:
import streamlit as st

try:
    import pandas as pd
    import requests

    st.set_page_config(layout="wide")

    st.title("🛡️ Cybersecurity AI Agent Pro")

    # باقي كودك هنا بالكامل 👇
    # (لا تغيره فقط ضعه داخل try)

except Exception as e:
    st.error(f"❌ خطأ في التطبيق: {str(e)}")
