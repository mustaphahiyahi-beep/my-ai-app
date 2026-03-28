import streamlit as st
import pandas as pd

st.title("🛡️ Cybersecurity AI Agent Pro")

# تخزين البيانات
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_area("📥 أدخل Logs أو سؤال:")

def analyze_security(log):
    log = log.lower()

    if "failed login" in log:
        return "Brute Force", "🔴 عالي", "حظر IP + MFA"

    elif "nmap" in log or "port scan" in log:
        return "Port Scan", "🟠 متوسط", "إغلاق المنافذ + Firewall"

    elif "sql" in log:
        return "SQL Injection", "🔴 عالي", "استخدام Prepared Statements"

    elif "script" in log:
        return "XSS Attack", "🟠 متوسط", "تصفية المدخلات"

    else:
        return "Normal", "🟢 منخفض", "لا يوجد خطر"

if st.button("🔍 تحليل"):

    attack, risk, solution = analyze_security(user_input)

    # حفظ النتيجة
    st.session_state.history.append({
        "log": user_input,
        "attack": attack,
        "risk": risk
    })

    st.subheader("📊 النتيجة:")
    st.write(f"🧠 الهجوم: {attack}")
    st.write(f"⚠️ الخطورة: {risk}")
    st.write(f"🛠️ الحل: {solution}")

# 📊 Dashboard
st.subheader("📈 لوحة التحكم")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)

    st.write("عدد العمليات:", len(df))
    st.write("أنواع الهجمات:")
    st.write(df["attack"].value_counts())

    st.dataframe(df)
