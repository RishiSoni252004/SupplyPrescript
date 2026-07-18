from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings and configuration.
    Uses Pydantic BaseSettings to load from environment variables or .env file.
    """
    PROJECT_NAME: str = "SupplyPrescript API"
    PROJECT_DESCRIPTION: str = "API for Closed-Loop Prescriptive Analytics"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Placeholder for future database integration
    DATABASE_URL: str = "sqlite:///./supplyprescript.db"

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instantiate settings to be imported across the application
settings = Settings()
