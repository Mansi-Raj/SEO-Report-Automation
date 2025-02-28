import smtplib
import ssl
import os
from email.message import EmailMessage
from datetime import datetime

# Email credentials (Use environment variables for security)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL Port
SENDER_EMAIL = os.getenv("SENDER_EMAIL")  # Set this in your environment
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")  # Use App Password if using Gmail
RECIPIENT_EMAILS = ["stakeholder1@example.com", "stakeholder2@example.com"]

# Get the latest report
current_date = datetime.now()
month_year = current_date.strftime("%B-%Y")
report_filename = f"report-{month_year}.pdf"
report_path = os.path.join(os.getcwd(), "report", month_year, report_filename)

# Check if the report exists
if not os.path.exists(report_path):
    print("Error: Report file not found!")
    exit()

# Create email
msg = EmailMessage()
msg["Subject"] = f"SEO Report - {month_year}"
msg["From"] = SENDER_EMAIL
msg["To"] = ", ".join(RECIPIENT_EMAILS)
msg.set_content(f"Hello,\n\nAttached is the SEO Performance Report for {month_year}.\n\nBest regards,\nSEO Automation System")

# Attach PDF
with open(report_path, "rb") as f:
    msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=report_filename)

# Send email
context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
    print("Report sent successfully!")
except smtplib.SMTPAuthenticationError:
    print("Error: Authentication failed. Check your email credentials.")
except Exception as e:
    print(f"Error: {e}")
