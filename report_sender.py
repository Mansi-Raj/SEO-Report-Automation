import smtplib
import ssl
from email.message import EmailMessage

# Email credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # For SSL
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Use an App Password if using Gmail
RECIPIENT_EMAILS = ["stakeholder1@example.com", "stakeholder2@example.com"]

# Create email
msg = EmailMessage()
msg["Subject"] = "Monthly SEO Performance Report"
msg["From"] = SENDER_EMAIL
msg["To"] = ", ".join(RECIPIENT_EMAILS)
msg.set_content("Attached is the Monthly SEO Performance Report.")

# Attach PDF
with open("monthly_seo_report.pdf", "rb") as f:
    msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="monthly_seo_report.pdf")

# Send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)

print("Report sent successfully!")
