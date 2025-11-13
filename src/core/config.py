from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int = "5432"
    POSTGRES_PASSWORD: str = "herrington"
    POSTGRES_USER: str = "billy"
    POSTGRES_DB: str = "qa_dev"
    POSTGRES_HOST: str = "172.27.32.1"
    api_prefix: str = "/api/v1"

    db_echo: bool = True

    @property
    def db_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.DATABASE_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
