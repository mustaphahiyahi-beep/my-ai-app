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
        with st.spinner("جاري التفكير..."):
            try:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": "Bearer " + st.secrets["OPENAI_API_KEY"],
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": "أنت خبير أمن سيبراني"},
                            {"role": "user", "content": question}
                        ]
                    }
                )

                result = response.json()
                answer = result["choices"][0]["message"]["content"]

                st.success("الإجابة:")
                st.write(answer)

            except Exception as e:
                st.error(f"خطأ: {e}")
    else:
        st.warning("اكتب سؤال أولاً")
