import smtplib
from email.message import EmailMessage
from app.core.config import settings


class EmailDeliveryError(RuntimeError):
    """Raised when DecorAI cannot deliver an email."""


def send_email(to_email: str, subject: str, body: str) -> None:
    if not settings.smtp_host or not settings.smtp_username or not settings.smtp_password:
        raise EmailDeliveryError(
            "Email delivery is not configured. Add SMTP_HOST, SMTP_USERNAME and "
            "SMTP_PASSWORD to backend/.env."
        )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email or settings.smtp_username}>"
    message["To"] = to_email
    message.set_content(body)

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=20) as server:
            server.ehlo()
            if settings.smtp_use_tls:
                server.starttls()
                server.ehlo()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(message)
    except (smtplib.SMTPException, OSError) as exc:
        raise EmailDeliveryError(
            "Unable to send email. Check your Gmail App Password, SMTP username, host and port."
        ) from exc
