from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Inventory Management API"
    ENVIRONMENT: str = "development"
    API_VERSION: str = "0.1.0"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    POSTMARK_SERVER_TOKEN: str | None = None
    SENTRY_DSN: str | None = None
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()
