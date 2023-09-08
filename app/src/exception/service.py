import json

from starlette import status

from app import SERVICE_CODE


class SampleServiceError(Exception):

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


class TokenizerNotFoundError(SampleServiceError):
    """토크나이저 미설정"""

    def __init__(self, tokenizer):
        self.code = int(f"{SERVICE_CODE}{status.HTTP_404_NOT_FOUND}")
        self.message = "Tokenizer is required"
        self.result = {"current_tokenizer": tokenizer}


class TokenValidationError(SampleServiceError):
    """유효하지 않은 토큰 설정"""

    def __init__(self, x_token):
        self.code = int(f"{SERVICE_CODE}{status.HTTP_401_UNAUTHORIZED}")
        self.message = "Invalid x-token header"
        self.result = {"current_x_token": x_token}
