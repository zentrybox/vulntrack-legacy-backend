from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "VulnTrack Backend"
    admin_email: str = "admin@example.com"
    secret_key: str = "your_secret_key"
    debug: bool = False
    
    # Database settings
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "user"
    db_password: str = "password"
    db_name: str = "analyzer-db"
    database_url: Optional[str] = None
    
    # Application settings
    app_port: int = 8000
    environment: str = "development"

    model_config = {"env_file": ".env"}
        
    @property
    def sync_database_url(self) -> str:
        if self.database_url and not self.database_url.startswith("postgresql+asyncpg"):
            return self.database_url.replace("postgresql+asyncpg://", "postgresql://")
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def async_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()