from typing import Optional

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from fastapi_mail.errors import ConnectionErrors
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr

from core.config import Config
from core.exceptions import MailServiceError

html_template_env = Environment(
    loader=FileSystemLoader(searchpath="./templates/"), enable_async=True
)
template = html_template_env.get_template(name="verify_email.html")

connection = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.get_mail_password(),
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.get_mail_server(),
    MAIL_STARTTLS=Config.MAIL_STARTTLS,
    MAIL_SSL_TLS=Config.MAIL_SSL_TLS,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
)


async def send_verification_mail(
    dest_email: EmailStr, protocol: str, username: str
) -> Optional[bool]:
    """
    Send verification email to user.

    Args:
        dest_email (EmailStr): Destination email address
        protocol (str): Verification protocol/token
        username (str): User's name for email personalization

    Returns:
        Optional[bool]: True if email sent successfully, None if failed

    Raises:
        HTTPException: If email sending fails
    """
    try:
        message = MessageSchema(
            recipients=[dest_email],
            subject="Confirme seu cadastro na FitTude!",
            body=await template.render_async(nome=username, prot=protocol),
            subtype="html",
        )

        await FastMail(connection).send_message(message)
        return True

    except ConnectionErrors:
        raise MailServiceError()


async def send_pwd_change_mail(dest_email: EmailStr, username: str, char_protocol: str):
    """
    Handle password change request.

    Returns:
        Optional[bool]: True if email sent successfully, None if failed

    Raises:
        HTTPException: If email sending fails
    """
    try:
        message = MessageSchema(
            recipients=[dest_email],
            subject="Alteração de senha no FitTude",
            body=await template.render_async(
                nome=username, random_char_sequence=char_protocol
            ),
            subtype="html",
        )
        await FastMail(connection).send_message(message)

    except ConnectionErrors:
        raise MailServiceError()
