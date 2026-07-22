from report_generator import generate_report
from email_report import send_email

# Your email address
receiver = "ai.trading3421@gmail.com"

report = generate_report()

send_email(
    subject="📈 AI Trading Manager Daily Report",
    body=report,
    receiver=receiver
)