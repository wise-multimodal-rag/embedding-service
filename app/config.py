import logging
from typing import Literal, List, Annotated, Any, Union

from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> Union[List[str], str]:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list) or isinstance(v, str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    PORT: int = 8000
    SERVICE_NAME: str = "Python FastAPI Template"
    SERVICE_CODE: int = 100
    MAJOR_VERSION: str = "v1"
    STATUS: str = "dev"

    LEVEL: str = "DEBUG"
    SYSTEM_LOG_LEVEL: int = logging.getLevelName(LEVEL)
    JSON_LOG: int = 0
    SAVE: int = 1
    ROTATION: str = "00:00"
    RETENTION: str = "10 days"
    COMPRESSION: str = "zip"
    LOG_SAVE_PATH: str = "./logs"

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        Union[List[AnyUrl], str], BeforeValidator(parse_cors)
    ] = []

    X_TOKEN: str = "fake-super-secret-token"


settings = Settings()  # type: ignore
