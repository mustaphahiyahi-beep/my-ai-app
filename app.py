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
    content = [
        Paragraph("Cybersecurity Report", styles['Title']),
        Spacer(1, 12),
        Paragraph(text, styles['BodyText'])
    ]
    doc.build(content)

# ================= Threat Detection =================
def detect_threats(text):
    text = text.lower()
    threats = []

    if "sql" in text:
        threats.append("SQL Injection")
    if "login" in text:
        threats.append("Brute Force")
    if "malware" in text:
        threats.append("Malware")

    return threats

# ================= AI =================
def analyze_ai(text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a SOC expert."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

# ================= IP =================
def get_ip(ip):
    try:
        return requests.get(f"http://ip-api.com/json/{ip}").json()
    except:
        return None

# ================= VirusTotal =================
def scan_url(url):
    key = st.secrets["VIRUSTOTAL_API_KEY"]
    headers = {"x-apikey": key}

    res = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data={"url": url}
    )

    analysis_id = res.json()["data"]["id"]
    time.sleep(3)

    report = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers=headers
    )

    return report.json()

# ================= UI =================

file = st.file_uploader("📁 Upload Logs", type=["txt", "log"])
text = ""

if file:
    text = file.read().decode("utf-8")
else:
    text = st.text_area("💬 Enter logs")

ip = st.text_input("🌐 Enter IP")
url = st.text_input("🔗 Enter URL")

# ================= RUN =================
if st.button("🔍 Analyze"):

    risk = 0

    # AI
    if text:
        ai = analyze_ai(text)

        st.subheader("🧠 AI Analysis")
        st.success(ai)

        threats = detect_threats(text)

        st.subheader("🚨 Threat Detection")
        st.write(threats)

        # Risk من AI
        risk += 20 + (10 * len(threats))

        create_pdf(ai)
        with open("report.pdf", "rb") as f:
            st.download_button("📥 PDF", f, "report.pdf")

    # IP
    if ip:
        data = get_ip(ip)

        if data and data["status"] == "success":
            st.subheader("🌍 IP Info")

            st.write(f"Country: {data['country']}")
            st.write(f"ISP: {data['isp']}")

            if "Google" in data["isp"]:
                risk += 10
            else:
                risk += 25

    # URL
    if url:
        vt = scan_url(url)

        stats = vt["data"]["attributes"]["stats"]
        mal = stats.get("malicious", 0)
        safe = stats.get("harmless", 0)

        st.subheader("🧪 URL Scan")

        st.metric("Malicious", mal)
        st.metric("Safe", safe)

        if mal > 0:
            st.error("Dangerous URL")
            risk += 50
        else:
            st.success("Safe URL")

    # Risk النهائي
    st.subheader("🔥 Risk Score")

    if risk < 30:
        st.success(f"Low Risk: {risk}%")
    elif risk < 70:
        st.warning(f"Medium Risk: {risk}%")
    else:
        st.error(f"High Risk: {risk}%")

    # حفظ
    st.session_state.history.append({"Risk": risk})

# Dashboard
st.subheader("📊 Dashboard")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.line_chart(df["Risk"])
