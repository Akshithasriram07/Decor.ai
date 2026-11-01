
import smtplib
import logging
from email.message import EmailMessage
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailDeliveryError(RuntimeError):
    """Raised when DecorAI cannot deliver an email."""


def send_email(to_email: str, subject: str, body: str) -> None:
    provider = settings.email_provider.strip().lower()
    if provider == "resend":
        if not settings.resend_api_key or not settings.resend_from_email:
            raise EmailDeliveryError(
                "Resend email delivery requires RESEND_API_KEY and RESEND_FROM_EMAIL."
            )
        try:
            response = httpx.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {settings.resend_api_key}"},
                json={
                    "from": f"{settings.smtp_from_name} <{settings.resend_from_email}>",
                    "to": [to_email],
                    "subject": subject,
                    "text": body,
                },
                timeout=20,
            )
            response.raise_for_status()
            return
        except httpx.HTTPError as exc:
            logger.exception("DecorAI Resend delivery failed: %s", type(exc).__name__)
            raise EmailDeliveryError(
                "Unable to send email through Resend. Check the API key and verified sender."
            ) from exc

    if provider != "smtp":
        raise EmailDeliveryError("EMAIL_PROVIDER must be set to 'smtp' or 'resend'.")

    if not settings.smtp_host or not settings.smtp_username or not settings.smtp_password:
        raise EmailDeliveryError(
            "Email delivery is not configured. Add SMTP_HOST, SMTP_USERNAME and "
            "SMTP_PASSWORD to backend/.env."
        )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = (
        f"{settings.smtp_from_name} "
        f"<{settings.smtp_from_email or settings.smtp_username}>"
    )
    message["To"] = to_email
    message.set_content(body)

    try:
        with smtplib.SMTP(
            settings.smtp_host, settings.smtp_port, timeout=20
        ) as server:
            server.ehlo()
            if settings.smtp_use_tls:
                server.starttls()
                server.ehlo()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(message)

    except (smtplib.SMTPException, OSError) as exc:
        logger.exception("DecorAI email delivery failed: %s", type(exc).__name__)
        raise EmailDeliveryError(
            "Unable to send email. Check your email service configuration."
        ) from exc
