import streamlit as st
from groq import Groq
import requests
import time
import pandas as pd

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ================= UI STYLE =================
st.set_page_config(page_title="Cyber AI Pro", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
.card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ================= API =================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🛡️ Cybersecurity AI Platform")

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

# ================= URL =================
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

# ================= FILE =================
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
    time.sleep(15)

    report = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
        headers=headers
    )

    return report.json()

# ================= UI INPUT =================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📁 Logs")
    log_file = st.file_uploader("Upload log file", type=["txt", "log"])
    text = ""
    if log_file:
        text = log_file.read().decode("utf-8")
    else:
        text = st.text_area("Paste logs here")

with col2:
    st.markdown("### 🌐 Intelligence")
    ip = st.text_input("Enter IP")
    url = st.text_input("Enter URL")

st.markdown("### 🦠 Malware Scanner")
malware_file = st.file_uploader("Upload file (EXE, PDF, etc)")

# ================= ANALYSIS =================
if st.button("🚀 Analyze"):

    risk = 0

    # ===== AI =====
    if text:
        ai = analyze_ai(text)

        st.markdown("## 🧠 AI Analysis")
        st.markdown(f"<div class='card'>{ai}</div>", unsafe_allow_html=True)

        threats = detect_threats(text)

        st.markdown("## 🚨 Threat Detection")
        st.write(threats)

        if len(threats) == 0:
            risk += 5
        elif len(threats) == 1:
            risk += 15
        else:
            risk += 25

        create_pdf(ai)
        with open("report.pdf", "rb") as f:
            st.download_button("📥 Download Report", f, "report.pdf")

    # ===== IP =====
    if ip:
        data = get_ip(ip)

        if data and data["status"] == "success":
            st.markdown("## 🌍 IP Info")
            st.write(f"Country: {data['country']}")
            st.write(f"ISP: {data['isp']}")

            if ip.startswith("192.168"):
                st.warning("⚠️ Internal IP (Not external attacker)")
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

        st.markdown("## 🧪 URL Scan")
        st.metric("Malicious", mal)
        st.metric("Safe", safe)

        if mal > 0:
            st.error("🚨 Dangerous URL")
            risk += 50
        else:
            st.success("✅ Safe URL")

    # ===== FILE =====
    if malware_file:
        vt_file = scan_file(malware_file)
        stats = vt_file["data"]["attributes"]["stats"]

        mal = stats.get("malicious", 0)
        safe = stats.get("harmless", 0)

        st.markdown("## 🦠 Malware Scan")
        st.metric("Malicious", mal)
        st.metric("Safe", safe)

        if mal > 0:
            st.error("🚨 Malware detected!")
            risk += 70
        else:
            st.success("✅ File is safe")

    # ===== RISK =====
    st.markdown("## 🔥 Risk Score")

    if risk < 30:
        st.success(f"Low Risk: {risk}%")
    elif risk < 70:
        st.warning(f"Medium Risk: {risk}%")
    else:
        st.error(f"High Risk: {risk}%")

    st.session_state.history.append({"Risk": risk})

# ================= DASHBOARD =================
st.markdown("## 📊 Dashboard")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    df["Risk"] = pd.to_numeric(df["Risk"])
    st.line_chart(df["Risk"])
