import logging
import os
import sys
from pathlib import Path

import yaml

from app.version import write_version_py, get_version_info

SERVICE_CODE: int = 100


def read_config(conf_path: str = 'config.yaml'):
    config = yaml.load(Path(conf_path).resolve().open('r', encoding='utf-8'), Loader=yaml.FullLoader)
    required_config = ['PORT', 'LOG']
    if config is None:
        sys.exit(f"Set {required_config} config.yaml")
    return config


if not Path('version_info.py').exists():
    write_version_py(file_name='version_info.py')
VERSION, GIT_REVISION, GIT_SHORT_REVISION, GIT_BRANCH, BUILD_DATE = get_version_info()
conf = read_config(conf_path='config.yaml')
# LOG_LEVEL: DEBUG(10), INFO(20)
LOG_LEVEL: str = logging.getLevelName(os.getenv('LOG_LEVEL', conf['LOG']['LEVEL']))  # type: ignore
JSON_LOGS: bool = True if os.environ.get("JSON_LOGS", "0") == "1" else False
