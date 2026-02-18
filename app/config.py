from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str
    model_config = SettingsConfigDict(env_file='app/env/.env', env_file_encoding='utf-8')

settings = Settings()
