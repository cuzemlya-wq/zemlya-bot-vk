from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VK_TOKEN: str
    VK_GROUP_ID: int
    DATABASE_URL: str = "sqlite+aiosqlite:///./bot_database.db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
