from typing import Any

from pydantic import BaseModel

from app import SERVICE_CODE, Log
from app.version import VERSION


class APIResponseModel(BaseModel):
    """기본 API 응답 포맷 by AIP Restful API 디자인 가이드"""
    code: int = int(f"{SERVICE_CODE}200")
    message: str = f"API Response Success ({VERSION})" if Log.is_debug_enable() else "API Response Success"
    result: dict[str, Any] = {}
    description: str = ""
