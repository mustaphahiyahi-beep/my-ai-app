import streamlit as st
from groq import Groq
import requests
import time
import pandas as pd

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ================= إعداد الصفحة =================
st.set_page_config(page_title="Cyber AI Pro", page_icon="🛡️", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ================= API =================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ✅ حل مشكلة session_state
if "history" not in st.session_state:
    st.session_state.history = []

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

# ================= SIDEBAR =================
st.sidebar.title("🛡️ Cyber AI Pro")
page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📁 Logs", "🌐 IP Analysis", "🔗 URL Scan", "🦠 Malware Scan"]
)

st.title("🛡️ Cybersecurity AI Platform")

# ================= DASHBOARD =================
if page == "📊 Dashboard":
    st.subheader("📊 Risk Overview")

    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        df["Risk"] = pd.to_numeric(df["Risk"])
        st.line_chart(df["Risk"])

    st.info("System monitoring active...")

# ================= LOGS =================
elif page == "📁 Logs":
    st.subheader("📁 Log Analysis")

    log_file = st.file_uploader("Upload log file", type=["txt", "log"])
    text = ""

    if log_file:
        text = log_file.read().decode("utf-8")
    else:
        text = st.text_area("Paste logs")

    if st.button("Analyze Logs"):
        with st.spinner("Analyzing..."):
            ai = analyze_ai(text)

        st.success("Analysis Complete")
        st.write(ai)

        threats = detect_threats(text)
        st.subheader("🚨 Threat Detection")
        st.write(threats)

        # Risk
        risk = 25 if len(threats) > 1 else 15
        st.session_state.history.append({"Risk": risk})

        create_pdf(ai)
        with open("report.pdf", "rb") as f:
            st.download_button("📥 Download Report", f, "report.pdf")

# ================= IP =================
elif page == "🌐 IP Analysis":
    st.subheader("🌐 IP Intelligence")

    ip = st.text_input("Enter IP")

    if st.button("Check IP"):
        with st.spinner("Loading..."):
            data = get_ip(ip)

        if data and data["status"] == "success":
            col1, col2 = st.columns(2)
            col1.metric("Country", data["country"])
            col2.metric("ISP", data["isp"])

            if ip.startswith("192.168"):
                st.warning("⚠️ Internal IP")

# ================= URL =================
elif page == "🔗 URL Scan":
    st.subheader("🔗 URL Scanner")

    url = st.text_input("Enter URL")

    if st.button("Scan URL"):
        with st.spinner("Scanning..."):
            vt = scan_url(url)

        stats = vt["data"]["attributes"]["stats"]

        mal = stats.get("malicious", 0)
        safe = stats.get("harmless", 0)

        col1, col2 = st.columns(2)
        col1.metric("Malicious", mal)
        col2.metric("Safe", safe)

        if mal > 0:
            st.error("🚨 Dangerous")
        else:
            st.success("✅ Safe")

# ================= FILE =================
elif page == "🦠 Malware Scan":
    st.subheader("🦠 File Scanner")

    file = st.file_uploader("Upload file")

    if file and st.button("Scan File"):
        with st.spinner("Scanning file..."):
            vt_file = scan_file(file)

        stats = vt_file["data"]["attributes"]["stats"]

        mal = stats.get("malicious", 0)
        safe = stats.get("harmless", 0)

        col1, col2 = st.columns(2)
        col1.metric("Malicious", mal)
        col2.metric("Safe", safe)

        if mal > 0:
            st.error("🚨 Malware detected!")
        else:
            st.success("✅ File is safe")
