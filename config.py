from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class EnviromentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # DATABASE
    POSTGRES_USER: str
    POSTGRES_USER_PASSWORD: str
    POSTGRES_DATABASE: str

    # SETUP
    ADMIN_EMAIL: EmailStr

    # EMAIL CONFIG
    YOUR_DOMAIN: str

    # TOKEN CONFIG
    TOKEN_SECRET: str
    TOKEN_EXPIRY: int



enviroment_settings = EnviromentSettings()
