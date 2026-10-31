from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "DecorAI API"
    environment: str = "development"
    secret_key: str = "change-this-in-production"
    database_url: str = "postgresql+psycopg://decorai:CHANGE_ME@localhost:5432/decorai"
    access_token_expire_minutes: int = 10080
    upload_dir: str = "uploads"
    generated_dir: str = "generated"
    max_upload_mb: int = 10
    frontend_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_from_name: str = "DecorAI"
    smtp_use_tls: bool = True

    ai_provider: str = "mock"
    ai_api_key: str = ""
    ai_model: str = "gemini-3.1-flash-image"
    ai_text_provider: str = "gemini"
    ai_text_model: str = "gemini-3.8-flash"
    ai_text_fallback_models: str = "gemini-3.1-flash-lite"
    ai_base_url: str = "https://generativelanguage.googleapis.com/v1beta"
    xai_base_url: str = "https://api.x.ai/v1"

    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    admin_email: str = "admin@decorai.local"
    admin_password: str = "ChangeMe123!"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def origins(self) -> list[str]:
        return [x.strip() for x in self.frontend_origins.split(",") if x.strip()]

settings = Settings()
