# Embedding Service

![PythonVersion](https://img.shields.io/badge/python-3.9.13-blue)
![FastAPIVersion](https://img.shields.io/badge/fastapi-0.110.0-yellowgreen)
![loguru](https://img.shields.io/badge/loguru-0.7.2-orange)

## Index

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Authors](#authors)
- [License](#license)

## Overview

모델을 사용하여 텍스트 임베딩 결과를 제공하는 서비스
> **클러스터 환경에서 MiniO에 저장된 모델을 사용하여 텍스트 임베딩 결과를 제공**하는 것을 기본으로 한다.

## Getting started

### 1. Create Project

1. GitLab **Create new project** 을 통해 새로운 프로젝트 생성
2. **Create from template** 선택
3. **Group** 선택
4. **wisenut/DE/테스트베드:Python FastAPI Template** 에서 **Use template** 선택
5. _Project name, Project description (optional)_ 등을 작성하고 **Create project** 선택
6. 🔴 **gitlab-ci Container Registry Deploy**를 위해 프로젝트 생성시 무조건 `Settings > Repository > Deploy tokens`에 **Name:
   gitlab+deploy-token** 으로 토큰 생성하기 🔴

### 2. Development Environment Setting

1. 로컬 개발 환경에 `git clone ...`
2. Pycharm 을 열고 `open project ...`
3. Interpreter Setting
    - **Virtualenv**
        1. **Add New Interpreter** 선택
        2. **Add Local Interpreter** 선택
        3. **Virtualenv Environment** 선택
        4. 로컬에 설치된 Python 3.10 경로를 Base Interpreter로 설정
        5. `pip install .` (`pyproject.toml`에 작성한 의존성 설치, 아래 **3. Extra Setting** 참고)
    - Poetry (보류)
        1. Poetry 설치 ([poetry docs](https://python-poetry.org/docs/#installation) 참고)
        2. **Add New Interpreter** 선택
        3. **Add Local Interpreter** 선택
        4. **Poetry Environment** 선택
        5. Python version에 맞게 환경 설정 (현재는 3.10 사용중)
        6. **Install packages from pyproject.toml** 체크
            - `UnicodeError` 발생 할 경우, **Settings > Editor > Global Encoding, Project Encoding, Properties Files** 모두 '
              UTF-8' 로 설정
            - 🐛 해결이 안 될 경우, 체크 표시 해제하고 poetry 가상환경 생성한 후 poetry venv 터미널에 `poetry install`로 직접 Installs the project
              dependencies
        7. **OK** 선택

### 3. Extra Setting

- ❗ 실행 전 `.env` 파일에 필요한 환경변수 주입 ❗
    - 환경변수 없이도 동작하지만 디폴트값으로 설정돼서 동작하기 때문에 환경변수 설정 권장
    - `.env` 로그 관련 설정 작성
        - > [loguru](https://github.com/Delgan/loguru) 사용하여 로그 세팅
        - `SAVE`: 로그 파일 저장 여부 (1 = 저장, 0 = 저장하지 않음)
        - `ROTATION`: 매일 `mm:ss`시에 새로운 로그 파일 생성
        - `RETENTION`: 설정한 시간 이후에 제거 (ex. "1 month 2 weeks", "10h")
        - `COMPRESSION`: 압축 형식 ("gz", "bz2", "xz", "lzma", "tar", "tar.gz", "tar.bz2", "tar.xz", "zip" 등의 형식 지원)
        - `ROTATION`, `RETENTION`, `COMPRESSION` 모두 loguru에 있는 파라미터로 자세한 파라미터
          정보는 [공식 문서](https://loguru.readthedocs.io/en/stable/api/logger.html#file:~:text=See%20datetime.datetime-,The%20time%20formatting,-To%20use%20your)
          확인
        - `PATH`: 디렉토리명까지 설정, (default = `YYYY/MM/*.log` 디렉토리 생성)
- ❗ 도커 빌드 및 실행할 경우, `version.py` 실행 사전 작업 필수 ❗
  (없을 경우에도 정상작동 되지만 필요한 정보를 볼 수 없음)
  👉 `version_info.py` 정보 생성 과정
  ```python
  service: str = 'FastAPI Sample'
  version: str = 'v1.6a6b8b0'
  git_branch: str = '21-refectoring-intialize'
  git_revision: str = '6a6b8b01cffcb7519013317f052dd104e1c39e56'
  git_short_revision: str = '6a6b8b0'
  build_date: str = '2024-03-20 09:16:40'
  ```
- `pyproject.toml` 작성 (
  참고: [Declaring project metadata](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/))
    - project 메타데이터 작성 (_name_, _version_, ... etc)
    - 의존성 작성: _dependencies_
    - 개발 의존성 작성: _project.optional-dependencies_

### 4. Run

- local run
    - `$HOME/main.py`
        - `FileNotFoundError` or `ImportError` 발생시 _Working Directory_ (Working Directory = `$HOME`) 확인하기
    - _http :8000/openapi.json_ or _http://localhost:8000/docs_ 로 API 명세 확인 및 테스트
- docker run    
  `docker build ...` && `docker run -d -p ...` 로 컨테이너 빌드 & 구동
  ```shell
  # 도커 이미지 빌드
  docker build -t python-fastapi-template:0.1.5-dev -f Dockerfile .
  # 컨테이너 구동
  docker run -d --name python-fastapi-template -p 8000:8000 -e DEFAULT_X_TOKEN=fake-super-secret-token -e DEFAULT_TOKEN=default-token python-fastapi-template:0.1.5-dev
  ```

## Authors

- **Seoyeon Park** - <sally9476@wisenut.ac.kr>
- **Jungheon Jeong** - <legagain@wisenut.ac.kr>

## License

@Wisenut