import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

logger = logging.getLogger(__name__)

def send_notification_email(recipient, subject, body):
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    email_host = os.getenv("EMAIL_HOST")
    email_port = int(os.getenv("EMAIL_PORT"))

    if not email_user or not email_pass:
        logger.warning("Email credentials not configured")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)
        
        logger.info(f"Email sent to {recipient}: {subject}")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False