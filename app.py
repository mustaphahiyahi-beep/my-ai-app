import streamlit as st
from groq import Groq
import requests
import time
import pandas as pd

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# إعداد
st.set_page_config(page_title="Cybersecurity AI Pro", page_icon="🛡️")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ذاكرة
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🛡️ Cybersecurity AI Pro")

# ================= PDF =================
def create_pdf(text):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Cybersecurity Incident Report", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph(text, styles['BodyText']))

    doc.build(content)

# ================= AI =================
def analyze_with_ai(text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a professional SOC analyst."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

# ================= IP =================
def get_ip_info(ip):
    try:
        return requests.get(f"http://ip-api.com/json/{ip}").json()
    except:
        return None

# ================= VirusTotal =================
def scan_url(url):
    api_key = st.secrets["VIRUSTOTAL_API_KEY"]
    headers = {"x-apikey": api_key}
    data = {"url": url}

    response = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data=data
    )

    result = response.json()
    analysis_id = result["data"]["id"]

    time.sleep(3)

    report = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers=headers
    )

    return report.json()

# ================= واجهة =================

# إدخال
uploaded_file = st.file_uploader("📁 Upload Log File", type=["txt", "log"])
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

# URL
st.subheader("🔗 URL Scanner")
url_input = st.text_input("Enter URL")

# ================= زر =================
if st.button("🔍 Analyze"):

    total_risk = 0

    # ===== AI =====
    if user_input:
        try:
            ai_result = analyze_with_ai(user_input)

            st.subheader("🧠 AI Analysis")
            st.success(ai_result)

            create_pdf(ai_result)
            with open("report.pdf", "rb") as f:
                st.download_button("📥 Download PDF", f, "report.pdf")

            total_risk += 40

        except Exception as e:
            st.error(f"AI Error: {e}")

    # ===== IP =====
    if ip_input:
        ip_data = get_ip_info(ip_input)

        if ip_data and ip_data["status"] == "success":
            st.subheader("🌍 IP Details")

            col1, col2 = st.columns(2)
            col1.write(f"Country: {ip_data['country']}")
            col1.write(f"City: {ip_data['city']}")
            col2.write(f"ISP: {ip_data['isp']}")
            col2.write(f"Org: {ip_data['org']}")

            if "Google" in ip_data["isp"]:
                risk_ip = 10
            else:
                risk_ip = 30

            total_risk += risk_ip

        else:
            st.error("IP Error")

    # ===== URL =====
    if url_input:
        try:
            vt = scan_url(url_input)
            stats = vt["data"]["attributes"]["stats"]

            malicious = stats.get("malicious", 0)
            harmless = stats.get("harmless", 0)

            st.subheader("🧪 VirusTotal Result")

            col1, col2 = st.columns(2)
            col1.metric("🚨 Malicious", malicious)
            col2.metric("✅ Safe", harmless)

            total = malicious + harmless
            score = (malicious / total) * 100 if total > 0 else 0

            st.progress(int(score))

            if malicious > 0:
                st.error("⚠️ Dangerous URL")
                total_risk += 50
            else:
                st.success("✅ Safe URL")

        except Exception as e:
            st.error(f"URL Error: {e}")

    # ===== Risk Score =====
    st.subheader("🔥 Risk Score")

    if total_risk < 30:
        st.success(f"Low Risk: {total_risk}%")
    elif total_risk < 70:
        st.warning(f"Medium Risk: {total_risk}%")
    else:
        st.error(f"High Risk: {total_risk}%")

    # ===== History =====
    st.session_state.history.append({
        "Input": user_input[:50],
        "IP": ip_input,
        "URL": url_input,
        "Risk": total_risk
    })

# ================= Dashboard =================

st.subheader("📊 Dashboard")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)

    st.dataframe(df)

    st.line_chart(df["Risk"])
else:
    st.info("No data yet")
