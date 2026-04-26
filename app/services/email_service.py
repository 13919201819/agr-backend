import smtplib
from email.mime.text import MIMEText
from app.core.config import settings


def send_reset_email(to_email: str, reset_link: str):

    subject = "Reset Your Password"

    body = f"""
Hello,

You requested to reset your password.

Click the link below to reset it:

{reset_link}

This link will expire in 15 minutes.

If you did not request this, ignore this email.

Thanks,
Your Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.HOST_EMAIL
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(settings.SMTP_EMAIL, settings.SMTP_PASS)

        server.sendmail(settings.HOST_EMAIL, to_email, msg.as_string())

        server.quit()

        print("✅ Email sent successfully")

        return True

    except Exception as e:
        print("❌ Email error:", str(e))
        return False