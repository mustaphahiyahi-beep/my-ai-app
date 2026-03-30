import streamlit as st
from groq import Groq
import requests
import time

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# إعداد API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# واجهة
st.set_page_config(page_title="Cybersecurity AI", page_icon="🛡️")
st.title("🛡️ Cybersecurity AI Platform")

# إنشاء PDF
def create_pdf(text):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Cybersecurity Incident Report", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph(text, styles['BodyText']))

    doc.build(content)

# رفع ملف
uploaded_file = st.file_uploader("📁 Upload Log File", type=["txt", "log"])

# إدخال نص
user_input = ""
if uploaded_file:
    user_input = uploaded_file.read().decode("utf-8")
    st.success("✅ File uploaded")
else:
    user_input = st.text_area("💬 Enter logs")

# تقليل الحجم
if len(user_input) > 4000:
    user_input = user_input[:4000]
    st.warning("⚠️ Text trimmed")

# IP
st.subheader("🌐 IP Intelligence")
ip_input = st.text_input("Enter IP")

def get_ip_info(ip):
    try:
        return requests.get(f"http://ip-api.com/json/{ip}").json()
    except:
        return None

# VirusTotal
st.subheader("🔗 URL Scanner (VirusTotal)")
url_input = st.text_input("Enter URL")

def scan_url(url):
    api_key = st.secrets["VIRUSTOTAL_API_KEY"]

    headers = {"x-apikey": api_key}
    data = {"url": url}

    # إرسال الرابط
    response = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data=data
    )

    result = response.json()
    analysis_id = result["data"]["id"]

    # انتظار
    time.sleep(3)

    # جلب النتيجة
    report = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers=headers
    )

    return report.json()

# زر التحليل
if st.button("🔍 Analyze"):

    # 🧠 AI
    if user_input:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert."},
                    {"role": "user", "content": user_input}
                ]
            )

            result = response.choices[0].message.content

            st.subheader("🧠 AI Analysis")
            st.success(result)

            # PDF
            create_pdf(result)
            with open("report.pdf", "rb") as f:
                st.download_button("📥 Download PDF", f, "report.pdf")

            # Dashboard
            st.subheader("📊 Dashboard")
            st.write("Analysis complete ✅")

        except Exception as e:
            st.error(f"❌ AI Error: {e}")

    # 🌐 IP
    if ip_input:
        ip_data = get_ip_info(ip_input)

        if ip_data and ip_data["status"] == "success":
            st.subheader("🌍 IP Info")
            st.write(ip_data)
        else:
            st.error("❌ IP Error")

    # 🔗 URL
    if url_input:
        try:
            vt = scan_url(url_input)

            stats = vt["data"]["attributes"]["stats"]

            malicious = stats.get("malicious", 0)
            harmless = stats.get("harmless", 0)

            st.subheader("🧪 Scan Results")

            st.metric("🚨 Malicious", malicious)
            st.metric("✅ Safe", harmless)

            if malicious > 0:
                st.error("⚠️ This URL is potentially dangerous!")
            else:
                st.success("✅ This URL looks safe")

        except Exception as e:
            st.error(f"❌ URL Error: {e}")

    # ⚠️ لا يوجد إدخال
    if not user_input and not ip_input and not url_input:
        st.warning("⚠️ Enter something to analyze")
