import streamlit as st
from groq import Groq
import requests
import time
import pandas as pd

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ================= PAGE =================
st.set_page_config(page_title="ThreatGuard AI", page_icon="🧠", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}

/* Top Tabs */
.topbar {
    text-align: center;
    font-size: 22px;
    margin-bottom: 20px;
    color: #8b949e;
}

/* Buttons */
.big-btn {
    background: linear-gradient(90deg, #1f6feb, #9333ea);
    padding: 15px;
    border-radius: 20px;
    text-align: center;
    color: white;
    font-weight: bold;
}

/* Card */
.card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

# ================= API =================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ✅ fix history bug
if "history" not in st.session_state:
    st.session_state.history = []

# ================= LOGO =================
st.markdown("""
<h1 style='text-align:center;'>🧠 ThreatGuard AI</h1>
<p style='text-align:center; color:gray;'>Next-Gen Cybersecurity Platform</p>
""", unsafe_allow_html=True)

# ================= NAV =================
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📁 Logs", "🌐 IP", "🔗 URL", "🦠 Malware", "📊 Dashboard"]
)

# ================= FUNCTIONS =================
def analyze_ai(text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a SOC expert."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

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

def get_ip(ip):
    try:
        return requests.get(f"http://ip-api.com/json/{ip}").json()
    except:
        return None

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

def create_pdf(text):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = [
        Paragraph("Cybersecurity Report", styles['Title']),
        Spacer(1, 12),
        Paragraph(text, styles['BodyText'])
    ]

    doc.build(content)

# ================= HOME =================
if page == "🏠 Home":
    st.markdown("## 🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    col1.markdown('<div class="big-btn">📁 Analyze Logs</div>', unsafe_allow_html=True)
    col2.markdown('<div class="big-btn">🌐 Scan IP</div>', unsafe_allow_html=True)
    col3.markdown('<div class="big-btn">🦠 Scan File</div>', unsafe_allow_html=True)

    st.info("Use sidebar to navigate")

# ================= LOGS =================
elif page == "📁 Logs":
    st.subheader("📁 Log Analysis")

    file = st.file_uploader("Upload log file", type=["txt", "log"])
    text = ""

    if file:
        text = file.read().decode("utf-8")
    else:
        text = st.text_area("Paste logs")

    if st.button("Analyze"):
        with st.spinner("Analyzing..."):
            ai = analyze_ai(text)

        st.markdown(f"<div class='card'>{ai}</div>", unsafe_allow_html=True)

        threats = detect_threats(text)
        st.write("🚨 Threats:", threats)

        risk = 25 if len(threats) > 1 else 15
        st.session_state.history.append({"Risk": risk})

        create_pdf(ai)
        with open("report.pdf", "rb") as f:
            st.download_button("📥 Download PDF", f, "report.pdf")

# ================= IP =================
elif page == "🌐 IP":
    st.subheader("🌐 IP Analysis")

    ip = st.text_input("Enter IP")

    if st.button("Analyze IP"):
        data = get_ip(ip)

        if data and data["status"] == "success":
            st.metric("Country", data["country"])
            st.metric("ISP", data["isp"])

            if ip.startswith("192.168"):
                st.warning("⚠️ Internal IP")

# ================= URL =================
elif page == "🔗 URL":
    st.subheader("🔗 URL Scanner")

    url = st.text_input("Enter URL")

    if st.button("Scan URL"):
        vt = scan_url(url)
        stats = vt["data"]["attributes"]["stats"]

        mal = stats.get("malicious", 0)
        safe = stats.get("harmless", 0)

        st.metric("Malicious", mal)
        st.metric("Safe", safe)

        if mal > 0:
            st.error("🚨 Dangerous")
        else:
            st.success("✅ Safe")

# ================= FILE =================
elif page == "🦠 Malware":
    st.subheader("🦠 Malware Scanner")

    file = st.file_uploader("Upload file")

    if file and st.button("Scan File"):
        vt_file = scan_file(file)
        stats = vt_file["data"]["attributes"]["stats"]

        mal = stats.get("malicious", 0)
        safe = stats.get("harmless", 0)

        st.metric("Malicious", mal)
        st.metric("Safe", safe)

        if mal > 0:
            st.error("🚨 Malware detected!")
        else:
            st.success("✅ Safe")

# ================= DASHBOARD =================
elif page == "📊 Dashboard":
    st.subheader("📊 Risk Dashboard")

    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        df["Risk"] = pd.to_numeric(df["Risk"])
        st.line_chart(df["Risk"])
    else:
        st.info("No data yet")
