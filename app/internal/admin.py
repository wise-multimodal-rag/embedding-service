from fastapi import APIRouter

from app.models import APIResponseModel

router = APIRouter()


@router.post("", response_model=APIResponseModel)
async def update_admin():
    return {"message": "Admin getting schwifty"}
