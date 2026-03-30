import streamlit as st
from groq import Groq
import requests
import time
import pandas as pd

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ================= إعداد الصفحة =================
st.set_page_config(page_title="Cybersecurity AI Pro", page_icon="🛡️")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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

# ================= URL Scan =================
def scan_url(url):
    key = st.secrets["VIRUSTOTAL_API_KEY"]
    headers = {"x-apikey": key}

    res = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data={"url": url}
    )

    analysis_id = res.json()["data"]["id"]

    time.sleep(8)

    report = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers=headers
    )

    return report.json()

# ================= Malware Scan =================
def scan_file(file):
    key = st.secrets["VIRUSTOTAL_API_KEY"]
    headers = {"x-apikey": key}

    files = {"file": file.getvalue()}

    res = requests.post(
        "https://www.virustotal.com/api/v3/files",
        headers=headers,
        files=files
    )

    analysis_id = res.json()["data"]["id"]

    time.sleep(10)

    report = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers=headers
    )

    return report.json()

# ================= UI =================

st.subheader("📁 Upload Log File")
log_file = st.file_uploader("Upload logs", type=["txt", "log"])

st.subheader("🦠 Malware File Scanner")
malware_file = st.file_uploader("Upload file to scan", type=None)

text = ""
if log_file:
    text = log_file.read().decode("utf-8")
else:
    text = st.text_area("💬 Enter logs")

ip = st.text_input("🌐 Enter IP")
url = st.text_input("🔗 Enter URL")

# ================= تحليل =================
if st.button("🔍 Analyze"):

    risk = 0

    # ===== Logs =====
    if text:
        ai = analyze_ai(text)

        st.subheader("🧠 AI Analysis")
        st.success(ai)

        threats = detect_threats(text)

        st.subheader("🚨 Threat Detection")
        st.write(threats)

        if len(threats) == 0:
            risk += 5
        elif len(threats) == 1:
            risk += 15
        else:
            risk += 25

        create_pdf(ai)
        with open("report.pdf", "rb") as f:
            st.download_button("📥 Download PDF", f, "report.pdf")

    # ===== IP =====
    if ip:
        data = get_ip(ip)

        if data and data["status"] == "success":
            st.subheader("🌍 IP Info")
            st.write(f"Country: {data['country']}")
            st.write(f"ISP: {data['isp']}")

            if ip.startswith("192.168"):
                st.info("⚠️ Internal IP detected")
                risk += 5
            elif "Google" in data["isp"]:
                risk += 10
            else:
                risk += 30

    # ===== URL =====
    if url:
        vt = scan_url(url)

        stats = vt["data"]["attributes"]["stats"]
        mal = stats.get("malicious", 0)
        safe = stats.get("harmless", 0)

        st.subheader("🧪 URL Scan")
        st.metric("Malicious", mal)
        st.metric("Safe", safe)

        if mal > 0:
            st.error("🚨 Dangerous URL")
            risk += 50
        else:
            st.success("✅ Safe URL")

    # ===== Malware File =====
    if malware_file:
        vt_file = scan_file(malware_file)

        stats = vt_file["data"]["attributes"]["stats"]
        mal = stats.get("malicious", 0)
        safe = stats.get("harmless", 0)

        st.subheader("🦠 Malware Scan Result")
        st.metric("Malicious", mal)
        st.metric("Safe", safe)

        if mal > 0:
            st.error("🚨 Malware detected!")
            risk += 70
        else:
            st.success("✅ File is safe")

    # ===== Risk =====
    st.subheader("🔥 Risk Score")

    if risk < 30:
        st.success(f"Low Risk: {risk}%")
    elif risk < 70:
        st.warning(f"Medium Risk: {risk}%")
    else:
        st.error(f"High Risk: {risk}%")

    st.session_state.history.append({"Risk": risk})

# ===== Dashboard =====
st.subheader("📊 Dashboard")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.line_chart(df, y="Risk")
