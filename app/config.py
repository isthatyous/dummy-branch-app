import os

class BaseConfig:
    DEBUG = False
    JSON_ERR0R_DEBUG = False
    LOG_LEVEL = "INFO"
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    PORT: int = int(os.getenv("PORT", "8000"))
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@db:5432/microloans",
    )

class DevConfig(BaseConfig):
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class StagConfig(BaseConfig):
    DEBUG = False
    LOG_LEVEL = "INFO"

class ProdConfig(BaseConfig):
    DEBUG = False
    LOG_LEVEL = "WARNING"
    STRUCTURED_LOGGING = True

def get_config():
    env = os.getenv("FLASK_ENV", "development")
    if env == "staging":
        return StagConfig
    elif env == "production":
        return ProdConfig
    return DevConfig


