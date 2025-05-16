from typing import Optional

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from fastapi_mail.errors import ConnectionErrors
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr

from app.core.config import Config
from app.core.exceptions import MailServiceError


class EmailClient:
    """
    Email client for sending emails using FastAPI Mail.
    This class handles the configuration and sending of emails
    for user verification and password change requests.
    """

    def __init__(self):
        """
        Initialize the EmailClient with configuration settings.
        This includes setting up the email connection configuration,
        HTML template environment, and the email client itself.
        """

        self.html_template_env = Environment(
            loader=FileSystemLoader(searchpath="./templates/"), enable_async=True
        )

        self.connection = ConnectionConfig(
            MAIL_USERNAME=Config.MAIL_USERNAME,
            MAIL_PASSWORD=Config.get_mail_password(),
            MAIL_PORT=Config.MAIL_PORT,
            MAIL_SERVER=Config.get_mail_server(),
            MAIL_STARTTLS=Config.MAIL_STARTTLS,
            MAIL_SSL_TLS=Config.MAIL_SSL_TLS,
            MAIL_FROM=Config.MAIL_FROM,
            MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
        )

        self.email_client = FastMail(self.connection)

    async def send_register_verify_mail(
        self, dest_email: EmailStr, protocol: str, username: str
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
            MailServiceError: If email sending fails
        """
        try:
            html_template = self.html_template_env.get_template(
                name="confirm_register.html"
            )

            message = MessageSchema(
                recipients=[dest_email],
                subject="Confirme seu cadastro na FitTude!",
                body=await html_template.render_async(nome=username, prot=protocol),
                subtype="html",
            )

            await self.email_client.send_message(message)
            return True

        except ConnectionErrors:
            raise MailServiceError()

    async def send_pwd_change_mail(
        self, dest_email: EmailStr, username: str, char_protocol: str
    ):
        """
        Send a email with password change instructions and code.
        Args:
            dest_email (EmailStr): Destination email address
            username (str): User's name for email personalization
            char_protocol (str): Password change protocol/token
        Returns:
            Optional[bool]: True if email sent successfully, None if failed
        Raises:
            MailServiceError: If email sending fails
        """
        try:
            html_template = self.html_template_env.get_template(
                name="change_password.html"
            )

            message = MessageSchema(
                recipients=[dest_email],
                subject="Alteração de senha no FitTude",
                body=await html_template.render_async(
                    nome=username, random_char_sequence=char_protocol
                ),
                subtype="html",
            )
            await self.email_client.send_message(message)

            return True

        except ConnectionErrors:
            raise MailServiceError()
