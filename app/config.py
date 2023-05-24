from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int
    algorithm: str

    class Config:
        env_file = ".env"

settings = Settings()