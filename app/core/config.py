import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str = "not_a_serious_key"
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


class DevelopmentConfig(Config):
    DEBUG: bool = True


class ProductionConfig(Config):
    DEBUG: bool = False


@lru_cache
def get_settings():
    config_by_env = {"development": DevelopmentConfig, "production": ProductionConfig}

    enviroment: str = os.getenv("env", "development")
    settings = config_by_env[enviroment]
    return settings()


settings = get_settings()
