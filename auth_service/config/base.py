from pydantic_settings import BaseSettings


class Base(BaseSettings):
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5445


base_config = Base()
