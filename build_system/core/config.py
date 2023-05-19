from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    files_path = Field('./../builds/')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
