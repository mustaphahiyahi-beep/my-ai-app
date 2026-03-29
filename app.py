import streamlit as st
from groq import Groq

# 🔑 API KEY
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🎨 واجهة التطبيق
st.set_page_config(page_title="Cybersecurity AI", page_icon="🛡️")
st.title("🛡️ Cybersecurity AI Analyst")

st.write("أدخل Log أو سؤال أمني وسيتم تحليله:")

# 📥 إدخال المستخدم
user_input = st.text_area("💬 أدخل البيانات هنا:")

# 🚀 زر التحليل
if st.button("🔍 تحليل"):
    if user_input:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a senior cybersecurity analyst working in a SOC (Security Operations Center).
You analyze logs and detect cyber threats.

Always provide:
- Threat classification (e.g., brute force, phishing, lateral movement)
- Risk level (Low, Medium, High, Critical)
- Technical explanation
- Clear mitigation steps

Be precise and professional."""
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )

            # 📤 عرض النتيجة
            answer = response.choices[0].message.content
            st.success(answer)

        except Exception as e:
            st.error(f"❌ خطأ: {e}")
    else:
        st.warning("⚠️ الرجاء إدخال نص للتحليل")
