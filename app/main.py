import os
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import yaml
from starlette.responses import JSONResponse
from uvicorn import Config, Server
from loguru import logger
from fastapi import Depends, FastAPI, Request

from app.version import get_version_info, write_version_py
from app.dependencies import get_query_token, get_token_header
from app.exceptions import CustomHTTPError
from app.internal import admin
from app.routers import items, users


def read_config(conf_path: str = 'config.yaml') -> tuple[str]:
    conf_path = Path(conf_path).resolve()
    config: dict[str, str] = yaml.load(Path(conf_path).open('r', encoding='utf-8'), Loader=yaml.FullLoader)
    required_config = ['PORT', 'LOG']
    if config is None:
        sys.exit(f"Set {required_config} config.yaml")
    return config


write_version_py(file_name='version_info.py')
VERSION, GIT_REVISION, GIT_SHORT_REVISION, GIT_BRANCH, BUILD_DATE = get_version_info()
conf = read_config(conf_path='config.yaml')
LOG_LEVEL = logging.getLevelName(conf['LOG']['LEVEL'])
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])
    if conf['LOG']['SAVE'] == 1:
        logger.add(
            Path(conf['LOG']['PATH']) / "{time:YYYY}" / "{time:MM}" / "{time:YYYYMMDD}_info.log",
            level=LOG_LEVEL,
            rotation=conf['LOG']['ROTATION'],
            retention=conf['LOG']['RETENTION'],
            compression=conf['LOG']['COMPRESSION']
        )


def check_env_exist() -> None:
    """
    설정이 필요한 환경변수가 세팅되어있는지 체크
    TODO: 필요한 환경변수가 없을 경우, 프로그램 종료

    Returns: None

    """
    env_list = ['DEFAULT_X_TOKEN', 'DEFAULT_TOKEN']  # TODO: 확인할 환경변수 설정
    for env in env_list:
        if env not in os.environ.keys():
            logging.warning(f"set {repr(env)} environment variable.")


@asynccontextmanager
async def lifespan(lifespan_app: FastAPI):
    # startup event
    logging.debug(f"Working Directory: {repr(os.getcwd())}")
    logging.info("Start Python FastAPI Template")
    logging.info("Check env exist ...")
    check_env_exist()
    yield
    # shutdown event
    logging.info("Shut down Python FastAPI Template")


app = FastAPI(
    lifespan=lifespan,
    title="Python FastAPI Template",
    description="DE Team Python FastAPI Template",
    version=VERSION,
    dependencies=[Depends(get_query_token)]
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,  # app/internal/admin.py 원본을 수정하지 않고 선언 가능
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.exception_handler(CustomHTTPError)
async def badrequest_handler(request: Request, exc: CustomHTTPError):
    return JSONResponse(status_code=400,
                        content={"code": exc.status_code, "message": f"{exc.detail}"})


@app.exception_handler(CustomHTTPError)
async def unauthorized_handler(request: Request, exc: CustomHTTPError):
    return JSONResponse(status_code=401,
                        content={"code": exc.status_code, "message": f"{exc.detail}"})


@app.exception_handler(CustomHTTPError)
async def forbidden_handler(request: Request, exc: CustomHTTPError):
    return JSONResponse(status_code=403,
                        content={"code": exc.status_code, "message": f"{exc.detail}"})


@app.exception_handler(CustomHTTPError)
async def notfound_handler(request: Request, exc: CustomHTTPError):
    return JSONResponse(status_code=404,
                        content={"code": exc.status_code, "message": f"{exc.detail}"})


@app.get("/")
async def root():
    return {"title": app.title, "description": app.description, "version": app.version, "docs_url": app.docs_url}


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.get("/info")
async def info():
    version: str = VERSION
    if 'Unknown' in version:
        version = version.split('.')[0]
    return {
        "version": version,
        "git_branch": GIT_BRANCH,
        "git_revision": GIT_REVISION,
        "git_short_revision": GIT_SHORT_REVISION,
        "build_date": BUILD_DATE
    }


if __name__ == "__main__":
    if 'PORT' in conf.keys():
        port = int(conf['PORT'])
    else:
        port = 8000

    server = Server(
        Config(
            "main:app",
            host="0.0.0.0",
            port=port,
            log_level=LOG_LEVEL,
        ),
    )

    # setup logging last, to make sure no library overwrites it
    # (they shouldn't, but it happens)
    setup_logging()
    # uvicorn.run(app=app, host="0.0.0.0", port=8000, log_level=LOG_LEVEL)
    server.run()
