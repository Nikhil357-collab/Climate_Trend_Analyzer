import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------- EMAIL ALERT ----------
def send_email_alert(subject, message):
    sender = os.getenv("ALERT_bhoyarnikhil115@gmail.com")           # your email
    password = os.getenv("ALERT_123")    # app password
    receiver = os.getenv("ALERT_bhoyarnikhil23@gmail.com")      # receiver email

    if not sender or not password or not receiver:
        print("⚠️ Email credentials not set. Skipping email alert.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        print("📧 Email alert sent!")
    except Exception as e:
        print("❌ Email failed:", e)


# ---------- SMS ALERT (Twilio) ----------
def send_sms_alert(message):
    try:
        from twilio.rest import Client
    except ImportError:
        print("⚠️ Twilio not installed. Run: pip install twilio")
        return

    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_TOKEN")
    twilio_number = os.getenv("TWILIO_NUMBER")
    target_number = os.getenv("TARGET_NUMBER")

    if not all([account_sid, auth_token, twilio_number, target_number]):
        print("⚠️ Twilio credentials not set. Skipping SMS alert.")
        return

    try:
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message,
            from_=twilio_number,
            to=target_number
        )
        print("📱 SMS alert sent!")
    except Exception as e:
        print("❌ SMS failed:", e)