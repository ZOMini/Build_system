from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    files_path = Field('./../builds/')
    app_port = Field(8080)
    get_tasks_url: str = 'http://nginx:8081/build/api/v1/get_tasks'

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
