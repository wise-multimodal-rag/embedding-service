"""
PUT, POST, GET 에 대한 다양한 API 예시를 작성해놨으니 참고해서 개발을 진행한다.
되도록이면 Swagger에서 API를 쉽게 파악하기 위해 API 및 Body, Path, Query에 대한 설명을 작성한다.
"""
from typing import Any

from fastapi import APIRouter, Depends, Path, Body, status
from fastapi.responses import JSONResponse

from app.config import settings
from app.dependencies import get_token_header
from app.docs.items import create_item_examples, update_item_examples, get_item_examples
from app.models import APIResponseModel
from app.src.exception.service import SampleServiceError

# mock data
fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
)


# 1. mock data를 사용하는 경우
@router.get("", response_model=APIResponseModel, response_class=JSONResponse)
async def read_items():
    return {"result": fake_items_db}


# TODO: Swagger에서 API를 쉽게 파악하기 위해 API 및 parameter에 대한 Query 설명 달기
@router.get("/{item_id}", response_model=APIResponseModel, response_class=JSONResponse)
async def read_item(
        item_id: str = Path(
            description="Item ID",
            openapi_examples=get_item_examples,  # type: ignore
            max_length=2048,
        )
):
    if item_id not in fake_items_db.keys():
        raise SampleServiceError(
            code=int(str(settings.SERVICE_CODE) + str(status.HTTP_404_NOT_FOUND)),
            message="Item not found", result={}
        )
    return {"result": {"name": fake_items_db[item_id]["name"], "item_id": item_id}}


@router.put(
    "/{item_id}",
    tags=["custom"],  # 해당 path operation은 ["items", "custom"] 두 가지 태그를 가지게 된다.
    responses={403: {"description": "Operation forbidden"}},  # 해당 path operation은 404, 403 두 가지 response를 내보낸다.
    response_model=APIResponseModel,  # API reponse model (format)
    summary="아이템 업데이트",  # 해당 API에 대한 요약 (작성하지 않을 경우, 함수명으로 처리됨 ex. Update Item)
    description="아이템을 업데이트하는 API",  # 해당 API에 대한 간략한 설명
    response_class=JSONResponse
)
async def update_item(
        item_id: str = Path(
            title="item_id",
            description="Item ID",
            openapi_examples=update_item_examples,  # type: ignore
            max_length=2048,
        )
):
    if item_id != "plumbus":
        raise SampleServiceError(
            code=int(str(settings.SERVICE_CODE) + str(status.HTTP_403_FORBIDDEN)),
            message="You can only update the item: plumbus", result={}
        )
    return {"result": {"item_id": item_id, "name": "The great Plumbus"}}


@router.post("", response_model=APIResponseModel, response_class=JSONResponse)
async def create_item(
        item: dict[str, Any] = Body(
            title="item name",
            description="아이템 업데이트를 위한 아이템명 설정",
            media_type="application/json",
            openapi_examples=create_item_examples,  # type: ignore
        )
):
    return {"result": {"item": item}}
