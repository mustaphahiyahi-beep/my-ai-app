import streamlit as st
from groq import Groq
import requests

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# UI
st.set_page_config(page_title="Cybersecurity AI", page_icon="🛡️")
st.title("🛡️ Cybersecurity AI Platform")

# PDF Function
def create_pdf(text):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Cybersecurity Incident Report", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph(text, styles['BodyText']))

    doc.build(content)

# Upload file
uploaded_file = st.file_uploader("📁 Upload Log File", type=["txt", "log"])

# Text input
user_input = ""
if uploaded_file:
    user_input = uploaded_file.read().decode("utf-8")
    st.success("✅ File uploaded")
else:
    user_input = st.text_area("💬 Enter logs")

# Limit size
if len(user_input) > 4000:
    user_input = user_input[:4000]
    st.warning("⚠️ Text trimmed")

# IP Section
st.subheader("🌐 IP Intelligence")
ip_input = st.text_input("Enter IP")

def get_ip_info(ip):
    try:
        return requests.get(f"http://ip-api.com/json/{ip}").json()
    except:
        return None

# 🔗 VirusTotal URL
st.subheader("🔗 URL Scanner (VirusTotal)")
url_input = st.text_input("Enter URL")

def scan_url(url):
    api_key = st.secrets["VIRUSTOTAL_API_KEY"]

    headers = {"x-apikey": api_key}
    data = {"url": url}

    response = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data=data
    )

    return response.json()

# BUTTON
if st.button("🔍 Analyze"):

    # AI Analysis
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

    # IP Analysis
    if ip_input:
        ip_data = get_ip_info(ip_input)
        if ip_data and ip_data["status"] == "success":
            st.subheader("🌍 IP Info")
            st.write(ip_data)
        else:
            st.error("❌ IP Error")

    # URL Analysis
    if url_input:
        try:
            vt = scan_url(url_input)

            st.subheader("🦠 VirusTotal Result")

            # عرض بسيط
            st.write(vt)

        except Exception as e:
            st.error(f"❌ URL Error: {e}")

    if not user_input and not ip_input and not url_input:
        st.warning("⚠️ Enter something to analyze") 
        
