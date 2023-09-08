"""package level global variables declare here."""
import logging
import os
import sys
from pathlib import Path

import toml
import yaml
from loguru import logger

from app.src import config

SERVICE_CODE: int = config.SERVICE_CODE

from app.src.exception.exceptions import UnsupportedPortType, EmptyConfigFile, ConfigLogValidationError


def validate_config_file(config):
    # required_config = ['PORT', 'LOG', 'SERVICE']
    # 설정 파일에 아무런 값이 없을 경우, PORT와 LOG_LEVEL 디폴트로 설정
    if config is None:
        logging.warning(
            "config is Empty. Automatically set port and log level to default value.(PORT=8000, LOG_LEVEL=DEBUG)")
    # PORT가 설정되어 있을 경우, int형 타입의 데이터인지 확인
    try:
        if 'PORT' in config:
            port: int = int(config['PORT'])
        else:
            port = 8000
    except ValueError:
        raise UnsupportedPortType(config['PORT'])
    # LOG가 설정되어 있을 경우, LOG에 대한 설정이 모두 되어있는지 확인
    required_log_keys = ['LEVEL', 'SAVE', 'ROTATION', 'RETENTION', 'COMPRESSION', 'PATH']
    if 'LOG' in config:
        if required_log_keys != list(config['LOG']):
            raise ConfigLogValidationError(
                current_log_config=config['LOG'],
                required=required_log_keys
            )
    return port


def read_config(conf_path: str = 'config.yaml'):
    try:
        config = yaml.load(Path(conf_path).resolve().open('r', encoding='utf-8'), Loader=yaml.FullLoader)
    except FileNotFoundError:
        raise EmptyConfigFile(conf_path)
    port = validate_config_file(config)
    return config, port


def check_env_exist() -> None:
    """
    설정이 필요한 환경변수가 세팅되어있는지 체크

    Returns: None

    """
    env_list = ['X_TOKEN']
    for env in env_list:
        if env not in os.environ.keys():
            logging.warning(f"set {repr(env)} environment variable.")


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # type: ignore
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(conf, log_level, json_logs):
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    try:
        logging.root.setLevel(log_level)
    except ValueError:
        sys.exit(f"Set appropriate 'LOG_LEVEL' environment variable. current {log_level=}")

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": json_logs}])
    required_log_keys = ['LEVEL', 'SAVE', 'ROTATION', 'RETENTION', 'COMPRESSION', 'PATH']
    if required_log_keys != list(conf['LOG'].keys()):
        raise ConfigLogValidationError(conf, required_log_keys)
    if conf['LOG']['SAVE'] == 1:
        logger.add(
            Path(conf['LOG']['PATH']) / "{time:YYYY}" / "{time:MM}" / "{time:YYYYMMDD}_info.log",
            level=log_level,
            rotation=conf['LOG']['ROTATION'],
            retention=conf['LOG']['RETENTION'],
            compression=conf['LOG']['COMPRESSION']
        )
    return logger.bind()


pyproject_info = toml.load(Path('pyproject.toml').open('r', encoding='utf-8'))
conf, port = read_config(conf_path='config.yaml')

# LOG_LEVEL: DEBUG(10), INFO(20)
LOG_LEVEL: str = logging.getLevelName(os.getenv('LOG_LEVEL', conf['LOG']['LEVEL']))  # type: ignore
JSON_LOGS: bool = True if os.environ.get("JSON_LOGS", "0") == "1" else False


# setup_logging(conf=conf, json_logs=JSON_LOGS, log_level=LOG_LEVEL)


class Log:
    """todo : 펑션으로 처리"""
    TRACE: int = 10
    log_level = int(LOG_LEVEL)

    @staticmethod
    def get_healthckeck_log_level():
        if LOG_LEVEL == logging.DEBUG:
            return 'debug'
        elif LOG_LEVEL == logging.INFO:
            return 'info'
        elif LOG_LEVEL == logging.WARN:
            return 'warn'
        elif LOG_LEVEL == logging.ERROR:
            return 'error'
        elif LOG_LEVEL == logging.FATAL:
            return 'critical'
        else:
            return 'no log_level'

    @staticmethod
    def is_trace_enable():
        return Log.log_level <= Log.TRACE

    @staticmethod
    def is_debug_enable():
        return Log.log_level <= logging.DEBUG

    @staticmethod
    def is_info_enable():
        return Log.log_level <= logging.INFO

    @staticmethod
    def is_warn_enable():
        return Log.log_level <= logging.WARN

    @staticmethod
    def is_error_enable():
        return Log.log_level <= logging.ERROR

    @staticmethod
    def is_fatal_enable():
        return Log.log_level <= logging.FATAL


X_TOKEN = os.getenv('X_TOKEN', "fake-super-secret-token")
MAJOR_VERSION = pyproject_info['project']['version']
ISRELEASED = False
