import streamlit as st
from security import analyze_event
from actions import auto_response
from utils import scan_file

# ✅ إصلاح مشكلة session_state
if "history" not in st.session_state:
    st.session_state.history = []

# 🎨 إعداد الصفحة
st.set_page_config(
    page_title="AI Cybersecurity Platform",
    page_icon="🛡️",
    layout="wide"
)

# 🎨 CSS لتحسين الشكل
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: #00ffcc;
}
.stButton>button {
    background-color: #00ffcc;
    color: black;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# 🧠 العنوان
st.title("🛡️ AI Cybersecurity Platform")
st.caption("Smart Threat Detection • Automated Response • Malware Scanner")

# تقسيم الصفحة
col1, col2 = st.columns(2)

# 📥 إدخال البيانات
with col1:
    st.subheader("📡 Input Data")
    ip = st.text_input("🌐 IP Address", placeholder="192.168.1.1")
    event = st.text_area("📜 Event / Log", placeholder="Failed login or SQL injection...")

# 🦠 رفع ملف
with col2:
    st.subheader("🦠 Malware Scanner")
    uploaded_file = st.file_uploader("Upload File")

# 🔍 زر التحليل
if st.button("🚀 Analyze Threat"):

    if not ip or not event:
        st.warning("⚠️ Please enter IP and Event")
    else:
        threats, score, level = analyze_event(event, ip)
        actions = auto_response(ip, threats, score, level)

        # حفظ في التاريخ
        st.session_state.history.append({
            "ip": ip,
            "threats": threats,
            "score": score,
            "level": level
        })

        st.markdown("---")

        # 🚨 النتائج
        col3, col4, col5 = st.columns(3)

        with col3:
            st.subheader("🚨 Threats")
            if threats:
                for t in threats:
                    st.error(t)
            else:
                st.success("No Threats")

        with col4:
            st.subheader("🔥 Risk Score")
            st.progress(score / 100)
            st.write(f"{score} / 100")
            st.write(f"Level: {level}")

        with col5:
            st.subheader("⚡ Actions")
            for action in actions:
                st.info(action)

# 🦠 فحص الملف
if uploaded_file:
    result = scan_file(uploaded_file)
    st.markdown("---")
    st.subheader("🦠 Malware Result")

    if result == "Malicious":
        st.error("🚨 Malicious File Detected")
    else:
        st.success("✅ File is Safe")

# 📊 Dashboard
st.markdown("---")
st.subheader("📊 Attack Dashboard")

if st.session_state.history:
    total = len(st.session_state.history)
    high = len([h for h in st.session_state.history if h["level"] == "HIGH"])
    medium = len([h for h in st.session_state.history if h["level"] == "MEDIUM"])

    col6, col7, col8 = st.columns(3)

    with col6:
        st.metric("Total Attacks", total)

    with col7:
        st.metric("High Risk", high)

    with col8:
        st.metric("Medium Risk", medium)

    st.markdown("### 📜 Logs History")

    for item in reversed(st.session_state.history):
        st.write(f"🌐 {item['ip']} | 🚨 {item['threats']} | 🔥 {item['score']} ({item['level']})")

else:
    st.info("No attacks recorded yet.")
