"""Конфигурация приложения через Pydantic Settings."""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Настройки приложения."""
    
    # VK Bot настройки
    vk_token: str = Field(..., description="VK токен группы")
    vk_group_id: int = Field(..., description="ID группы ВКонтакте")
    
    # Общие настройки
    environment: str = Field(default="development", description="Окружение")
    log_level: str = Field(default="INFO", description="Уровень логирования")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = Settings()
