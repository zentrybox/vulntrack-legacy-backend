from typing import Optional

from pydantic_settings import BaseSettings


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

    # MongoDB settings
    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_user: str = "user"
    mongodb_password: str = "password"
    mongodb_db_name: str = "cve_db"
    mongodb_url: Optional[str] = None

    # Application settings
    app_port: int = 8000
    environment: str = "development"

    # Gemini AI Configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    gemini_max_tokens: int = 2048
    gemini_temperature: float = 0.1

    # Brave Search API Configuration
    brave_search_api_key: str = ""
    brave_search_base_url: str = "https://api.search.brave.com/res/v1"
    brave_search_count: int = 10

    # Vulnerability Scanning Settings
    vuln_scan_enabled: bool = True
    vuln_scan_timeout: int = 30
    vuln_scan_max_retries: int = 3
    vuln_scan_cache_ttl: int = 3600
    vuln_scan_batch_size: int = 5
    vuln_scan_rate_limit_delay: float = 1.0

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

    @property
    def development_database_url(self) -> str:
        """SQLite database URL for development when PostgreSQL is not available"""
        return "sqlite:///./vulntrack_dev.db"

    @property
    def mongodb_connection_url(self) -> str:
        if self.mongodb_url:
            return self.mongodb_url
        return f"mongodb://{self.mongodb_user}:{self.mongodb_password}@{self.mongodb_host}:{self.mongodb_port}/{self.mongodb_db_name}"


settings = Settings()
