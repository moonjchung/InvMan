from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Inventory Management API"
    ENVIRONMENT: str = "development"
    API_VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "changeme"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    POSTMARK_SERVER_TOKEN: str | None = None
    SENTRY_DSN: str | None = None
    FIRST_SUPERUSER_EMAIL: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    FIRST_MANAGER_EMAIL: EmailStr = "manager@example.com"
    FIRST_MANAGER_PASSWORD: str = "manager"
    FIRST_STAFF_EMAIL: EmailStr = "staff@example.com"
    FIRST_STAFF_PASSWORD: str = "staff"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
