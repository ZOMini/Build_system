from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    files_path = Field('./../builds/')
    redis_url = Field('redis://redis_build:6379')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
