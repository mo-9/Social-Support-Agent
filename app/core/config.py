from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Social Support AI"

    # Database Config
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "adminpass"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5435"  # <--- نفس الرقم الجديد
    POSTGRES_DB: str = "social_support"

    # هنبني الرابط ديناميكياً باستخدام validator أو property، أو نخليه زي ما هو
    # هنا هنستخدم الطريقة المباشرة بس هنتجاهل الـ computed fields في الـ env
    DATABASE_URL: str = ""

    # Qdrant Config
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    # Redis Config
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""

    # دالة خاصة لتجهيز الروابط بعد تحميل المتغيرات
    def model_post_init(self, __context):
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        if not self.CELERY_BROKER_URL:
            self.CELERY_BROKER_URL = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        if not self.CELERY_RESULT_BACKEND:
            self.CELERY_RESULT_BACKEND = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    # هذا هو الحل السحري: extra="ignore"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )


settings = Settings()
