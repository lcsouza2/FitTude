from fastapi_mail import MessageSchema, ConnectionConfig, FastMail
from pydantic import EmailStr
from jinja2 import Environment, FileSystemLoader
from asyncio import run

html_template_env = Environment(
    loader=FileSystemLoader(searchpath="./Html_Templates/Email/"), enable_async=True
)
template = html_template_env.get_template(name="email_template.html")

connection = ConnectionConfig(
    MAIL_USERNAME="fittude.gym@gmail.com",
    MAIL_PASSWORD="zmdt oxkm qihk ugzp",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    MAIL_FROM="fittude.gym@gmail.com",
    MAIL_FROM_NAME="FitTude Team",
)

async def send_verification_mail(dest_email: EmailStr, protocol: str, username: str):
    message = MessageSchema(
        recipients=[dest_email],
        subject="Confirme seu cadastro na FitTude!",
        body=await template.render_async(
            nome=username, prot=protocol
        ),
        subtype="html",
    )

    await FastMail(connection).send_message(message)