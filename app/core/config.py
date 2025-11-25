from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    REDIS_HOST:str
    REDIS_PORT:int
    REDIS_PASSWORD:str
    TOMORROW_API_KEY:str
    FREECURRENCY_API_KEY : str
    NEWS_API_KEY : str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore"  # The file name is relative to the CWD
    )


settings = Settings()
