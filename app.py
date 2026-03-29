import streamlit as st
import requests

st.set_page_config(layout="wide")

st.title("🛡️ Cybersecurity AI Agent Pro")

# =============================
# 📊 Log Analyzer
# =============================
st.header("📊 Log Analyzer")

logs = st.text_area("📥 أدخل Logs:")

if st.button("تحليل"):
    if logs:
        st.success("تم استلام البيانات ✅")
        st.write(logs)
    else:
        st.warning("يرجى إدخال Logs")

# =============================
# 🤖 AI Cyber Assistant
# =============================
st.header("🤖 AI Cyber Assistant")

question = st.text_input("💬 اسأل عن الأمن السيبراني:")

if st.button("اسأل"):
    if question:
        with st.spinner("جاري التفكير..."):
            try:
                response = requests.post(
                    "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                    headers={
                        "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
                    },
                    json={
                        "inputs": question
                    }
                )

                result = response.json()

                if isinstance(result, list):
                    answer = result[0]["generated_text"]
                else:
                    answer = str(result)

                st.success("✅ الإجابة:")
                st.write(answer)

            except Exception as e:
                st.error(f"❌ خطأ: {e}")
    else:
        st.warning("اكتب سؤال أولاً")
