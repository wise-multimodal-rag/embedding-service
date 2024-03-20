"""
PUT, POST, GET 에 대한 다양한 API 예시를 작성해놨으니 참고해서 개발을 진행한다.
되도록이면 Swagger에서 API를 쉽게 파악하기 위해 API 및 Body, Path, Query에 대한 설명을 작성한다.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Body
from fastapi.responses import JSONResponse

from app.dependencies import get_token_header
from app.docs.items import create_item_examples, update_item_examples, get_item_examples
from app.models import APIResponseModel, CreateItemsRequestModel
from app.src.items.items import load_mock_items, read_item_from_db, update_item_to_db
from app.version import VERSION

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
)

# resonse message 통일, 통일을 원하지 않을 경우, 아래 리턴값에 개별적으로 설정한다.
response_success_msg = f"아이템 응답 성공 ({VERSION})"  # TODO: FastAPI의 데코레이터 기반 설정으로 변경


@router.get("", response_model=APIResponseModel, response_class=JSONResponse)
async def read_items():
    # mock data를 사용하는 경우. DB를 사용하는게 일반적임
    fake_items_db = load_mock_items()
    return {
        "message": response_success_msg,
        "result": fake_items_db,
        "description": "아이템 로드 성공"
    }


# TODO: Swagger에서 API를 쉽게 파악하기 위해 API 및 parameter에 대한 Query 설명 달기
@router.get("/{item_id}", response_model=APIResponseModel, response_class=JSONResponse)
async def read_item(
        item_id: str = Path(
            description="Item ID",
            openapi_examples=get_item_examples,  # type: ignore
            max_length=2048,
        )
):
    item_name = read_item_from_db(item_id)
    return {
        "message": response_success_msg,
        "result": {"name": item_name, "item_id": item_id},
        "description": "특정 아이템 아이디로 아이템 로드 성공"
    }


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
    item_name = update_item_to_db(item_id)
    return {
        "message": response_success_msg,
        "result": {"item_id": item_id, "name": item_name},
        "description": "아이템 업데이트 성공"
    }


@router.post("", response_model=APIResponseModel, response_class=JSONResponse)
async def create_item(
        item: Annotated[CreateItemsRequestModel, Body(
            title="아이템 업데이트를 위한 아이템명 설정",
            description="아이템 이름, 상태, 재고 입력",
            media_type="application/json",
            openapi_examples=create_item_examples,  # type: ignore
        )]
):
    return {
        "message": response_success_msg,
        "result": {"item": item},
        "description": "아이템 생성 성공"
    }
