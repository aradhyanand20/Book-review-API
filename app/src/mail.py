from fastapi_mail import FastMail, ConnectionConfig
from src.config import config

config1 = ConnectionConfig(
    MAIL_USERNAME = config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM = config.MAIL_FROM,
    MAIL_PORT =config.MAIL_PORT,
    MAIL_SERVER =config.MAIL_SERVER,
    MAIL_FROM_NAME=config.MAIL_FROM_NAME,
    MAIL_SSL_TLS= False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
mail = FastMail()