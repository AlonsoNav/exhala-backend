import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure all required environment variables are set
required_env_vars = ["MAIL_USERNAME", "MAIL_PASSWORD", "MAIL_FROM"]
for var in required_env_vars:
    if not os.getenv(var):
        logger.error(f"Environment variable {var} is not set")
        raise ValueError(f"Environment variable {var} is not set")

# Email configuration
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

async def send_reset_email(email: str, reset_code: str) -> None:
    """
    Send a password reset email to the user.

    :param email: str: The email address of the recipient
    :param reset_code: str: The password reset code
    """
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=f"Your password reset code is {reset_code}. It will expire in 15 minutes.",
        subtype="plain"
    )
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        logger.info(f"Password reset email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        raise
