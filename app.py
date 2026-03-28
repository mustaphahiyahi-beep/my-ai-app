import streamlit as st

st.title("🛡️ Cybersecurity AI Agent Pro")

user_input = st.text_area("📥 أدخل Logs أو سؤال:")

def analyze_security(log):

    log = log.lower()

    # 🔴 Brute Force
    if "failed login" in log or "multiple times" in log:
        return {
            "type": "Brute Force Attack",
            "risk": "🔴 عالي",
            "solution": "قم بحظر الـ IP + تفعيل MFA + تحديد عدد المحاولات"
        }

    # 🟠 Port Scan
    elif "port scan" in log or "nmap" in log:
        return {
            "type": "Port Scanning",
            "risk": "🟠 متوسط",
            "solution": "استخدم Firewall واغلق المنافذ غير المستخدمة"
        }

    # 🔴 Malware
    elif "malware" in log or "virus" in log:
        return {
            "type": "Malware Infection",
            "risk": "🔴 عالي",
            "solution": "اعزل الجهاز + استخدم Antivirus + فحص كامل"
        }

    # 🟡 Suspicious IP
    elif "ip" in log:
        return {
            "type": "Suspicious Activity",
            "risk": "🟡 متوسط",
            "solution": "راقب الـ IP وقم بحظره إذا تكرر"
        }

    # 🟢 طبيعي
    else:
        return {
            "type": "Normal Activity",
            "risk": "🟢 منخفض",
            "solution": "لا يوجد خطر واضح"
        }

if st.button("🔍 تحليل"):

    result = analyze_security(user_input)

    st.subheader("📊 النتيجة:")

    st.write(f"🧠 نوع الهجوم: {result['type']}")
    st.write(f"⚠️ مستوى الخطورة: {result['risk']}")
    st.write(f"🛠️ الحل: {result['solution']}")
