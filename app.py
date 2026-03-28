import streamlit as st

st.title("🛡️ Cyber AI Assistant (Free)")

user_input = st.text_input("اكتب سؤالك:")

def simple_ai(question):
    question = question.lower()

    if "اختراق" in question or "hack" in question:
        return "⚠️ تحذير: نشاط مشبوه! تأكد من تغيير كلمات المرور وتفعيل الحماية."

    elif "فيروس" in question or "virus" in question:
        return "🦠 ربما يوجد فيروس. قم بفحص الجهاز باستخدام برنامج حماية."

    elif "ip" in question:
        return "🌐 تحقق من عنوان IP، وإذا كان غريب قم بحظره."

    elif "مرحبا" in question or "hello" in question:
        return "👋 مرحبا! أنا مساعد الأمن السيبراني."

    else:
        return "🤖 حاول توضيح سؤالك أكثر."

if user_input:
    answer = simple_ai(user_input)
    st.write("🤖:", answer)
