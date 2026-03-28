import streamlit as st

st.title("🛡️ Cyber AI Assistant (Free)")

user_input = st.text_input("اكتب سؤالك:")

def simple_ai(question):
    question = question.lower()

    if "اختراق" in question or "hack" in question:
        return "⚠️ هذا قد يكون هجوم إلكتروني. تأكد من تأمين النظام وتغيير كلمات المرور."

    elif "فيروس" in question or "virus" in question:
        return "🦠 قد يكون فيروس. استخدم مضاد فيروسات وقم بفحص الجهاز."

    elif "ip" in question:
        return "🌐 عنوان IP مهم في التتبع. تأكد من مراقبته وحظره إذا كان مشبوه."

    elif "hello" in question or "مرحبا" in question:
        return "👋 مرحبا! كيف يمكنني مساعدتك في الأمن السيبراني؟"

    else:
        return "🤖 لم أفهم سؤالك جيدًا، حاول إعادة صياغته."

if user_input:
    answer = simple_ai(user_input)
    st.write("🤖:", answer)
