import streamlit as st
from groq import Groq
import requests

# 📄 PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# 🔑 API KEY
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 🎨 واجهة التطبيق
st.set_page_config(page_title="Cybersecurity AI", page_icon="🛡️")
st.title("🛡️ Cybersecurity AI Platform")

st.write("📂 Upload logs, analyze threats, and check IP intelligence")

# 📄 دالة إنشاء PDF
def create_pdf(text):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Cybersecurity Incident Report", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph(text, styles['BodyText']))

    doc.build(content)

# 📂 رفع ملف
uploaded_file = st.file_uploader("📁 Upload Log File", type=["txt", "log"])

# 📝 إدخال نص
user_input = ""
if uploaded_file is not None:
    user_input = uploaded_file.read().decode("utf-8")
    st.success("✅ File uploaded successfully")
else:
    user_input = st.text_area("💬 Enter logs or text:")

# ✂️ تقليل الحجم (حل مشكلة 413)
MAX_CHARS = 4000
if len(user_input) > MAX_CHARS:
    user_input = user_input[:MAX_CHARS]
    st.warning("⚠️ File too large, trimmed automatically")

# 🌐 تحليل IP
st.subheader("🌐 IP Intelligence")
ip_input = st.text_input("Enter IP address")

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        return response.json()
    except:
        return None

# 🚀 زر التحليل
if st.button("🔍 Analyze"):

    # 🧠 تحليل AI
    if user_input:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a senior cybersecurity analyst working in a SOC.

Analyze logs and detect:
- Threat classification (multiple if needed)
- Risk level (Low, Medium, High, Critical)
- Internal threats and lateral movement
- Technical explanation
- Mitigation steps

Be professional and precise."""
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )

            result = response.choices[0].message.content

            # ✅ عرض النتيجة
            st.subheader("🧠 AI Analysis")
            st.success(result)

            # 📥 تحميل PDF
            if st.button("📥 Download Report as PDF"):
                create_pdf(result)

                with open("report.pdf", "rb") as f:
                    st.download_button(
                        label="⬇️ Click to Download",
                        data=f,
                        file_name="security_report.pdf",
                        mime="application/pdf"
                    )

            # 📊 Dashboard
            st.subheader("📊 Security Dashboard")

            analysis_text = result.lower()

            threats = 0
            if "brute" in analysis_text:
                threats += 1
            if "sql" in analysis_text:
                threats += 1
            if "critical" in analysis_text:
                threats += 1

            col1, col2, col3 = st.columns(3)

            col1.metric("🚨 Threats Detected", threats)
            col2.metric("⚠️ Risk Level", "Critical" if "critical" in analysis_text else "Medium")
            col3.metric("✅ Status", "Completed")

        except Exception as e:
            st.error(f"❌ Error: {e}")

    # 🌐 تحليل IP
    if ip_input:
        ip_data = get_ip_info(ip_input)

        if ip_data and ip_data["status"] == "success":
            st.subheader("🌍 IP Information")
            st.write(f"Country: {ip_data['country']}")
            st.write(f"City: {ip_data['city']}")
            st.write(f"ISP: {ip_data['isp']}")
            st.write(f"Organization: {ip_data['org']}")
        else:
            st.error("❌ Failed to fetch IP info")

    # ⚠️ تنبيه
    if not user_input and not ip_input:
        st.warning("⚠️ Please enter logs or IP to analyze")

            
