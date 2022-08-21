from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str
    password: str
    database: str
    port: int
    host: str

    class Config:
        env_file = ".env"


settings = Settings()
