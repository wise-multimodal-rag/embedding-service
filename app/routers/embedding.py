from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.params import Body
from fastapi.responses import JSONResponse

from app.dependencies import get_token_header
from app.docs.embedding import sbert_embedding_examples, doc2vec_embedding_examples, use_embedding_examples
from app.models import APIResponseModel, EmbeddingRequest, SBertEmbeddingRequest
from app.src.embedding import sbert_embedding, doc2vec_embedding, formatting_embedding_result, use_embedding
from app.version import VERSION

router = APIRouter(
    prefix="/embeddings",
    tags=["embedding"],
    dependencies=[Depends(get_token_header)],
)

response_message = f"임베딩 성공 ({VERSION})"


@router.post("/doc2vec", response_model=APIResponseModel, response_class=JSONResponse)
async def embedding_doc2vec(
        request: Annotated[
            EmbeddingRequest,
            Body(
                title="임베딩을 위한 인풋 및 파라미터 설정",
                media_type="application/json",
                openapi_examples=doc2vec_embedding_examples  # pyright: ignore
            )
        ]
):
    # embedding
    embeddings = doc2vec_embedding(request.input, request.model)  # pyright: ignore
    # formatting
    embedding_response = formatting_embedding_result(embeddings, request.model)
    return {
        "message": response_message,
        "result": embedding_response,
        "description": "Doc2Vec 기반 임베딩 처리 완료"
    }


@router.post("/use", response_model=APIResponseModel, response_class=JSONResponse)
async def embedding_use(
        request: Annotated[
            EmbeddingRequest,
            Body(
                title="임베딩을 위한 인풋 및 파라미터 설정",
                media_type="application/json",
                openapi_examples=use_embedding_examples  # pyright: ignore
            )
        ]
):
    # embedding
    embeddings = use_embedding(request.input, request.model)    # pyright: ignore
    # formatting
    embedding_response = formatting_embedding_result(embeddings, request.model)
    return {
        "message": response_message,
        "result": embedding_response,
        "description": "USE 기반 임베딩 처리 완료"
    }


@router.post("/sbert", response_model=APIResponseModel, response_class=JSONResponse)
async def embedding_sbert(
        request: Annotated[
            SBertEmbeddingRequest,
            Body(
                title="임베딩을 위한 인풋 및 파라미터 설정",
                media_type="application/json",
                openapi_examples=sbert_embedding_examples  # pyright: ignore
            )
        ]
):
    # embedding
    embeddings = sbert_embedding(request.input, request.model, request.encoding_format)  # pyright: ignore
    # formatting
    embedding_response = formatting_embedding_result(embeddings, request.model)
    return {
        "message": response_message,
        "result": embedding_response,
        "description": "S-BERT 기반 임베딩 처리 완료"
    }
