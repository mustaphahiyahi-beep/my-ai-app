import streamlit as st
from groq import Groq
import requests
import time
import pandas as pd

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ================= UI ADVANCED =================

st.sidebar.title("🛡️ Cyber AI Pro")
st.sidebar.markdown("Advanced Security Platform")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📁 Logs", "🌐 IP Analysis", "🔗 URL Scan", "🦠 Malware Scan"]
)

st.title("🛡️ Cybersecurity AI Platform")

# ================= DASHBOARD =================
if page == "📊 Dashboard":
    st.subheader("📊 Risk Overview")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
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
        with st.spinner("Analyzing logs..."):
            ai = analyze_ai(text)

        st.success("Analysis Complete")
        st.write(ai)

# ================= IP =================
elif page == "🌐 IP Analysis":
    st.subheader("🌐 IP Intelligence")

    ip = st.text_input("Enter IP")

    if st.button("Check IP"):
        with st.spinner("Fetching IP info..."):
            data = get_ip(ip)

        if data and data["status"] == "success":
            st.success("IP Loaded")

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
        with st.spinner("Scanning URL..."):
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
