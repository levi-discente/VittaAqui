from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "VittaAqui"
    app_version: str = "0.1.0"
    debug: bool = False

    database_url: PostgresDsn

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    cors_origins: str = "*"

    # AWS S3 configuration
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "sa-east-1"
    aws_s3_bucket: str = "vitta-image-profile"

    @computed_field
    @property
    def cors_origins_list(self) -> list[str]:
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# pyright: reportCallIssue=false
settings = Settings()
