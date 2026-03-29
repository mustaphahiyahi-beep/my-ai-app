import streamlit as st
from groq import Groq

# 🔑 API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🎨 واجهة
st.set_page_config(page_title="Cybersecurity AI", page_icon="🛡️")
st.title("🛡️ Cybersecurity AI Analyst")

st.write("📂 ارفع ملف Log أو أدخل نص للتحليل")

# 📂 رفع ملف
uploaded_file = st.file_uploader("📁 اختر ملف Log", type=["txt", "log"])

# 📝 إدخال يدوي (إذا لم يتم رفع ملف)
user_input = ""
if uploaded_file is not None:
    user_input = uploaded_file.read().decode("utf-8")
    st.success("✅ تم تحميل الملف بنجاح")
else:
    user_input = st.text_area("💬 أو اكتب البيانات هنا:")

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
- Threat classification
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

            answer = response.choices[0].message.content
            st.success(answer)

        except Exception as e:
            st.error(f"❌ خطأ: {e}")
    else:
        st.warning("⚠️ الرجاء إدخال نص أو رفع ملف")
