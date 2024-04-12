from typing import List, Union, Literal

from pydantic import BaseModel, Field, model_validator

from app.config import settings
from app.log import Log
from app.version import VERSION


class EmbeddingRequest(BaseModel):
    input: Union[str, List[str]] = Field(description="임베딩을 진행할 단일 문서 or 여러 문서")
    model: str = Field(description="임베딩을 수행할 모델명")

    @model_validator(mode="after")
    def str_input_to_list(self):
        if isinstance(self.input, str):
            self.input = [self.input]
        return self


class SBertEmbeddingRequest(EmbeddingRequest):
    encoding_format: Literal["float32", "int8", "uint8", "binary", "ubinary"] = Field(
        title="임베딩 리턴 포맷 설정",
        description="옵션: ['float32', 'int8', 'uint8', 'binary', 'ubinary']",
        default="float32"
    )


class EmbeddingData(BaseModel):
    object: str = Field(description="임베딩 결과 오브젝트명", default="embedding")
    embedding: List[float] = Field(description="임베딩 결과", default=[])
    index: int = Field(description="문서 임베딩 결과 인덱스", default=-1)


class EmbeddingResponse(BaseModel):
    object: str = Field(description="오브젝트명", default="list")
    data: List[EmbeddingData]
    model: str = Field(description="설정한 모델명")


class APIResponseModel(BaseModel):
    code: int = int(f"{settings.SERVICE_CODE}200")
    message: str = f"임베딩 성공 ({VERSION})" if Log.is_debug_enable() else "임베딩 성공"
    result: EmbeddingResponse
    description: str = Field(default="임베딩 성공")
