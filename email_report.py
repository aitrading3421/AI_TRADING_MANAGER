import smtplib
from email.mime.text import MIMEText
from config import EMAIL, APP_PASSWORD


class EmailAI:

    def __init__(self):
        print("=" * 60)
        print("📧 EMAIL AI")
        print("=" * 60)
        print("✅ Email AI Ready")

    def send_email(self, subject, body, receiver):

        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = receiver

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(EMAIL, APP_PASSWORD)

        server.send_message(msg)

        server.quit()

        print("✅ Email Sent Successfully") 