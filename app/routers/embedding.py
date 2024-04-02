from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.params import Body
from fastapi.responses import JSONResponse

from app.dependencies import get_token_header
from app.docs.embedding import embedding_examples
from app.models import APIResponseModel, EmbeddingRequest, EmbeddingResponse, EmbeddingData
from app.src.embedding import sbert_embedding
from app.version import VERSION

router = APIRouter(
    prefix="/embeddings",
    tags=["embedding"],
    dependencies=[Depends(get_token_header)],
)


@router.post("", response_model=APIResponseModel, response_class=JSONResponse)
async def embedding(
        request: Annotated[
            EmbeddingRequest,
            Body(
                title="임베딩을 위한 인풋 및 파라미터 설정",
                media_type="application/json",
                openapi_examples=embedding_examples  # type: ignore
            )
        ]
):
    # embedding
    embeddings = sbert_embedding(request.input, request.model, request.encoding_format)  # type: ignore
    # formatting
    embedding_response = EmbeddingResponse(
        data=[EmbeddingData(embedding=emb, index=idx) for idx, emb in enumerate(embeddings)],  # type: ignore
        model=request.model
    )
    return {
        "message": f"임베딩 성공 ({VERSION})",
        "result": embedding_response,
        "description": "S-BERT 기반 임베딩 처리 완료"
    }
