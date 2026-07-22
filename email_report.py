import smtplib
from email.mime.text import MIMEText
from config import EMAIL, APP_PASSWORD


def send_email(subject, body, receiver):
    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(EMAIL, APP_PASSWORD)

    server.send_message(msg)

    server.quit()

    print("✅ Email sent successfully!")