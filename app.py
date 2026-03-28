import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")

st.title("🛡️ Cybersecurity AI Agent Pro")

# تقسيم الشاشة
col1, col2 = st.columns(2)

# =========================
# 🛡️ القسم الأول (تحليل)
# =========================
with col1:

    st.header("📊 Log Analyzer")

    if "history" not in st.session_state:
        st.session_state.history = []

    user_input = st.text_area("📥 أدخل Logs:")

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

        st.session_state.history.append({
            "log": user_input,
            "attack": attack,
            "risk": risk
        })

        st.success(f"🧠 {attack}")
        st.warning(f"⚠️ {risk}")
        st.info(f"🛠️ {solution}")

    # Dashboard
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.subheader("📈 Dashboard")
        st.write(df["attack"].value_counts())
        st.dataframe(df)


# =========================
# 🤖 القسم الثاني (AI)
# =========================
with col2:

    st.header("🤖 AI Cyber Assistant")

    ai_input = st.text_input("💬 اسأل عن الأمن السيبراني:")

    def ask_ai(question):
        url = "https://api.deepseek.com/v1/chat/completions"

        headers = {
            "Authorization": "sk-72885bff6559440286c83919058fbcc6",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a cybersecurity expert"},
                {"role": "user", "content": question}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "❌ خطأ في الاتصال بالذكاء الاصطناعي"

    if st.button("🤖 اسأل"):
        answer = ask_ai(ai_input)
        st.write(answer)
