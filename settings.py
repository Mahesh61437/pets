import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str = os.getenv('POSTGRES_SERVER')
    db_port: str = os.getenv('POSTGRES_PORT')
    db_database: str = os.getenv('POSTGRES_DB')
    db_user: str = os.getenv('POSTGRES_USER')
    db_password: str = os.getenv('POSTGRES_PASSWORD')

    class Config:
        # Reads from '.env' file
        env_file = '.env'


settings = Settings()


