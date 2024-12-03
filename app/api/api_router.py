from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.api.routers import embedding
from app.dependencies import get_token_header

api_router = APIRouter(dependencies=[Depends(get_token_header)], default_response_class=JSONResponse)

api_router.include_router(embedding.router, dependencies=[Depends(get_token_header)])
