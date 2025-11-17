from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "qa_dev"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    api_prefix: str = "/api/v1"

    echo: bool = True

    @property
    def url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class JWTSettings(BaseSettings):
    lifetime_seconds: int = 604800  # week
    reset_password_token_secret: str = "reset_pwd_secret"
    verification_token_secret: str = "verification_secret"


class Settings:
    db: DBSettings = DBSettings()
    jwt: JWTSettings = JWTSettings()
    auth_prefix: str = "/auth/jwt"


settings = Settings()
