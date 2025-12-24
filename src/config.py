"""
Configuration Module
Модуль конфигурации бота
"""

import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    """Класс конфигурации"""
    
    # VK API Settings
    VK_TOKEN: str = Field(..., env="VK_TOKEN")
    VK_GROUP_ID: int = Field(..., env="VK_GROUP_ID")
    VK_API_VERSION: str = Field(default="5.131", env="VK_API_VERSION")
    
    # Database
    DB_HOST: str = Field(default="localhost", env="DB_HOST")
    DB_PORT: int = Field(default=5432, env="DB_PORT")
    DB_NAME: str = Field(default="zemlya_bot", env="DB_NAME")
    DB_USER: str = Field(default="postgres", env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # External APIs
    ROSREESTR_API_KEY: str = Field(..., env="ROSREESTR_API_KEY")
    ROSREESTR_API_URL: str = Field(..., env="ROSREESTR_API_URL")
    CADASTRE_API_KEY: str = Field(..., env="CADASTRE_API_KEY")
    CADASTRE_API_URL: str = Field(..., env="CADASTRE_API_URL")
    MARKET_DATA_API_KEY: str = Field(..., env="MARKET_DATA_API_KEY")
    MARKET_DATA_API_URL: str = Field(..., env="MARKET_DATA_API_URL")
    
    # Payment Gateway
    YUKASSA_SHOP_ID: str = Field(..., env="YUKASSA_SHOP_ID")
    YUKASSA_SECRET_KEY: str = Field(..., env="YUKASSA_SECRET_KEY")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="logs/zemlya_bot.log", env="LOG_FILE")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    
    # Application
    PRODUCTION: bool = Field(default=False, env="PRODUCTION")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=30, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_PERIOD: int = Field(default=60, env="RATE_LIMIT_PERIOD")
    
    # Reports
    REPORT_CACHE_TTL: int = Field(default=3600, env="REPORT_CACHE_TTL")
    MAX_REPORT_SIZE_MB: int = Field(default=10, env="MAX_REPORT_SIZE_MB")
    
    # Payments
    REPORT_PRICE_RUB: int = Field(default=499, env="REPORT_PRICE_RUB")
    FREE_REPORTS_LIMIT: int = Field(default=3, env="FREE_REPORTS_LIMIT")
    
    # Redis (Optional)
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    REDIS_PASSWORD: str = Field(default="", env="REDIS_PASSWORD")
    
    # Monitoring
    PROMETHEUS_PORT: int = Field(default=9090, env="PROMETHEUS_PORT")
    METRICS_ENABLED: bool = Field(default=True, env="METRICS_ENABLED")
    SENTRY_DSN: str = Field(default="", env="SENTRY_DSN")
    
    # Feature Flags
    ENABLE_PAYMENTS: bool = Field(default=True, env="ENABLE_PAYMENTS")
    ENABLE_CADASTRE_LOOKUP: bool = Field(default=True, env="ENABLE_CADASTRE_LOOKUP")
    ENABLE_MARKET_ANALYSIS: bool = Field(default=True, env="ENABLE_MARKET_ANALYSIS")
    ENABLE_RISK_ASSESSMENT: bool = Field(default=True, env="ENABLE_RISK_ASSESSMENT")
    
    # Admin
    ADMIN_VK_IDS: List[int] = Field(default_factory=list, env="ADMIN_VK_IDS")
    SUPPORT_CHAT_URL: str = Field(default="", env="SUPPORT_CHAT_URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Глобальный экземпляр конфигурации
config = Config()
