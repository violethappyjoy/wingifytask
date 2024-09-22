import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException


def extract_name_from_email(email: str) -> str:
    return email.split("@")[0]


def remove_text_before_dear(results: str) -> str:
    dear_index = results.find("Dear")
    if dear_index != -1:
        return results[dear_index:], results[:dear_index]
    return results, "Blood Report Results"


def send_email_to_user(email: str, subject: str, message_body: str):
    sender_email = os.getenv("MY_EMAIL")
    sender_password = os.getenv("MY_PASSWD")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = email
        msg["Subject"] = subject

        msg.attach(MIMEText(message_body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection

        server.login(sender_email, sender_password)

        server.sendmail(sender_email, email, msg.as_string())

        server.quit()

        print(f"Email sent to {email} successfully!")
    except Exception as e:
        print(f"Failed to send email to {email}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")
