import os


class Settings:
    PROJECT_NAME: str = "fatcode_chat"
    PROJECT_VERSION: str = "1.0.0"
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER", "localhost")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db_chat:5432/{POSTGRES_DB}"


settings = Settings()

