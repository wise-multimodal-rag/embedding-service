import json

from starlette import status

from app.config import settings


class EmbeddingServiceError(Exception):

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


class TokenValidationError(EmbeddingServiceError):
    """유효하지 않은 토큰 설정"""

    def __init__(self, x_token):
        self.code = int(f"{settings.SERVICE_CODE}{status.HTTP_401_UNAUTHORIZED}")
        self.message = "Invalid x-token header"
        self.result = {"current_x_token": x_token}


class InvalidModelError(EmbeddingServiceError):
    """유효하지 않는 S-BERT 모델"""

    def __init__(self, model_name, error_message):
        self.code = int(f"{settings.SERVICE_CODE}{status.HTTP_404_NOT_FOUND}")
        self.message = f"Invalid model name: {error_message=}"
        self.result = {"current_model_name": model_name}


class NotExistModelError(EmbeddingServiceError):
    """로컬에 존재하지 않는 모델"""

    def __init__(self, model_name: str, error_message):
        self.code = int(f"{settings.SERVICE_CODE}{status.HTTP_422_UNPROCESSABLE_ENTITY}")
        self.message = f"Model does not exist in the storage: {error_message=}"
        self.result = {"current_model_name": model_name}


class UnknownError(EmbeddingServiceError):
    """미확인 에러"""

    def __init__(self, error_message):
        self.code = int(f"{settings.SERVICE_CODE}{status.HTTP_422_UNPROCESSABLE_ENTITY}")
        self.message = f"Unknown Error: {error_message=}"
        self.result = {"current_error_message": error_message}
