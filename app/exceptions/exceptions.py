import json

from starlette import status

from app.config import settings


class ApplicationError(Exception):
    """Application 구동 불가 에러"""

    def __init__(self, code: int, message: str, result):
        self.code = code
        self.message = message
        self.result = result

    def __str__(self):
        exception_data = {
            "code": self.code,
            "message": self.message,
            "result": self.result
        }
        return json.dumps(exception_data, indent=4, ensure_ascii=False)


class ConfigError(ApplicationError):
    """config.yaml에서 발생할 수 있는 모든 에러"""
    pass


class ConfigLogValidationError(ConfigError):
    """유효하지 않은 로그 설정"""

    def __init__(self, current_log_config, required):
        self.code = int(f"{settings.SERVICE_CODE}{status.HTTP_400_BAD_REQUEST}"),  # type: ignore
        self.message = f"required keys in config 'LOG': {required}",  # type: ignore
        self.result = {"current_log_config": current_log_config}


class UnsupportedPortType(ConfigError):
    """유효하지 않은 포트 설정"""

    def __init__(self, port):
        self.code = int(f"{settings.SERVICE_CODE}{status.HTTP_400_BAD_REQUEST}"),  # type: ignore
        self.message = "Port must be int type",  # type: ignore
        self.result = {"current_port": port}
