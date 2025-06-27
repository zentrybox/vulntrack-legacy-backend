import os


class Settings:
    # Brave Search
    brave_search_api_key: str = os.environ.get("BRAVE_SEARCH_API_KEY", "")
    brave_search_base_url: str = os.environ.get(
        "BRAVE_SEARCH_BASE_URL", "https://api.search.brave.com"
    )
    brave_search_count: int = int(os.environ.get("BRAVE_SEARCH_COUNT", 10))
    vuln_scan_timeout: int = int(os.environ.get("VULN_SCAN_TIMEOUT", 30))

    # Gemini AI
    gemini_api_key: str = os.environ.get("GEMINI_API_KEY", "")
    gemini_model: str = os.environ.get("GEMINI_MODEL", "gemini-pro")
    gemini_base_url: str = os.environ.get(
        "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"
    )
    gemini_temperature: float = float(os.environ.get("GEMINI_TEMPERATURE", 0.2))
    gemini_max_tokens: int = int(os.environ.get("GEMINI_MAX_TOKENS", 1024))


settings = Settings()
