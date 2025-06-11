from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "VulnTrack Backend"
    admin_email: str = "admin@example.com"
    secret_key: str = "your_secret_key"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()