import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr

load_dotenv()


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_FROM_NAME="Recover Exhala Password",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)


async def send_reset_email(email: str, reset_code: str):
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=f"Your password reset code is {reset_code}. It will expire in 15 minutes.",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
