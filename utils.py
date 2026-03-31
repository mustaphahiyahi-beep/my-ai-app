import smtplib
from email.mime.text import MIMEText

def send_email(subject, message):
    sender = st.secrets["EMAIL"]
    password = st.secrets["EMAIL_PASSWORD"]
    receiver = sender  # ترسل لنفسك

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return str(e)
