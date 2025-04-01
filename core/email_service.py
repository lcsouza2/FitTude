from logging import getLogger
from typing import Optional

from fastapi import HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from fastapi_mail.errors import ConnectionErrors
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr

logger = getLogger(__name__)

html_template_env = Environment(
    loader=FileSystemLoader(searchpath="./templates/"), enable_async=True
)
template = html_template_env.get_template(name="verify_email.html")

connection = ConnectionConfig(
    MAIL_USERNAME="fittude.gym@gmail.com",
    MAIL_PASSWORD="ghwk qhez ovdr tofn",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    MAIL_FROM="fittude.gym@gmail.com",
    MAIL_FROM_NAME="FitTude Team",
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

    except ConnectionErrors as e:
        logger.error(f"Erro de conexão ao enviar email: {str(e)}")
        raise HTTPException(
            status_code=503, detail="Serviço de email temporariamente indisponível"
        )

    except Exception as e:
        logger.error(f"Erro ao enviar email de verificação: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro ao enviar email de verificação"
        )
