# Python FastAPI Template

![PythonVersion](https://img.shields.io/badge/python-3.9.13-blue)
![FastAPIVersion](https://img.shields.io/badge/fastapi-0.95.2-yellowgreen)
![loguru](https://img.shields.io/badge/loguru-0.7.0-orange)

### DE팀 전용 FastAPI 개발 템플릿 

> API 명세는 와이즈넛 [Restful API 디자인 가이드](https://docs.google.com/document/d/1tSniwfrVaTIaTT4MxhBRAmv-S_ECcoSFAXlYrsg4K0Y/edit#heading=h.60fu2rc04bck)를 따른다.

Python FastAPI Template은 아래와 같은 특징을 갖고 있다.
1. Python 3.9: 높은 호환성
2. MSA 구조에 적합한 FastAPI 템플릿
3. setuptools를 사용한 의존성 (`pyproject.toml`으로 한 번에 관리)
4. 내부망 환경 구성
5. 도커 환경 구성 (개발 및 배포용 Dockerfile 구성)
6. gitlab-ci로 _build, unit test (pytest), lint test (flake8), deploy_ 수행

## Getting started

### 1. Create Project
1. GitLab **Create new project** 을 통해 새로운 프로젝트 생성
2. **Create from template** 선택
3. **Group** 선택
4. **wisenut/DE/테스트베드:Python FastAPI Template** 에서 **Use template** 선택
5. _Project name, Project description (optional)_ 등을 작성하고 **Create project** 선택
6. 🔴 **gitlab-ci Container Registry Deploy**를 위해 프로젝트 생성시 무조건 `Settings > Repository > Deploy tokens`에 **Name: gitlab+deploy-token** 으로 토큰 생성하기 🔴

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
        - `UnicodeError` 발생 할 경우, **Settings > Editor > Global Encoding, Project Encoding, Properties Files** 모두 'UTF-8' 로 설정 
        - 🐛 해결이 안 될 경우, 체크 표시 해제하고 poetry 가상환경 생성한 후 poetry venv 터미널에 `poetry install`로 직접 Installs the project dependencies
     7. **OK** 선택


### 3. Extra Setting
- ❗ 도커 빌드 및 실행할 경우, `version.py` 실행 사전 작업 필수 ❗    
  👉 `version_info.py` 정보 생성 과정
  ```python
  version: str = 'V1.9e33312'
  git_branch: str = 'minimal-refactoring'
  git_revision: str = '9e333123aa56235bb0dc81f0a11e53d204cbe68f'
  git_short_revision: str = '9e33312'
  build_date: str = '2023-05-02 11:09:51'
  ```
- `pyproject.toml` 작성 (참고: [Declaring project metadata](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/))
   - project 메타데이터 작성 (_name_, _version_, ... etc)
   - 의존성 작성: _dependencies_
   - 개발 의존성 작성: _project.optional-dependencies_
- `config.yaml` 파일 작성
  - `PORT`: fastapi server port
  - `LOG`: [loguru](https://github.com/Delgan/loguru) 사용하여 로그 세팅
    - `SAVE`: 로그 파일 저장 여부 (1 = 저장, 0 = 저장하지 않음)
    - `ROTATION`: 매일 `mm:ss`시에 새로운 로그 파일 생성
    - `RETENTION`: 설정한 시간 이후에 제거 (ex. "1 month 2 weeks", "10h")
    - `COMPRESSION`: 압축 형식 ("gz", "bz2", "xz", "lzma", "tar", "tar.gz", "tar.bz2", "tar.xz", "zip" 등의 형식 지원)
    - `ROTATION`, `RETENTION`, `COMPRESSION` 모두 loguru에 있는 파라미터로 자세한 파라미터 정보는 [공식 문서](https://loguru.readthedocs.io/en/stable/api/logger.html#file:~:text=See%20datetime.datetime-,The%20time%20formatting,-To%20use%20your) 확인
    - `PATH`: 디렉토리명까지 설정, (default = `YYYY/MM/*.log` 디렉토리 생성)
- **Project Major Version**은 `pyproject.toml`의 [project.version]에서 설정한다.
  - 해당 설정은 project version, FastAPI version 설정에 영향을 미친다.


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

### 📚 참고 사항 📚   
- 해당 템플릿은 크게 **msa**와 **monlith** 두 가지로 나뉜다. (@TODO: monolith)
- Default는 **msa**(`$HOME/app`)로 해당 템플릿을 그대로 사용하면 된다.
- 📌 **monolith**를 사용할 경우, msa (`$HOME/app`, `$HOME/tests`)는 삭제하고 최상위 디렉터리인 monolith를 삭제 후 사용한다.
- 📌 DB를 사용하지 않을 경우, 관련된 코드는 모두 삭제한다. (`crud.py`, `database.py`, `schemas.py` 등)


## MSA
> @tiangolo(FastAPI 개발자)가 제공하는 유형(ex. api, crud, 모델, 스키마)별로 파일을 구분하는 프로젝트 구조
- 출처: https://fastapi.tiangolo.com/tutorial/bigger-applications/
```
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # 
│   ├── main.py          # 
│   ├── dependencies.py  # 
│   ├── exceptions.py  # custom exception
│   ├── models.py  # 
│   ├── schemas.py  # 데이터베이스를 사용할 경우
│   ├── database.py  # 데이터베이스를 사용할 경우
│   ├── crud.py  # 데이터베이스를 사용할 경우
│   └── routers          # (API Endpoints) "routers" is a "Python subpackage" 
│   │   ├── __init__.py  # 
│   │   ├── items.py     # 
│   │   └── users.py     # 
│   └── internal         # 
│       ├── __init__.py  # 
│       └── admin.py     # 
│   └── src         # (Main Functions) "src" is a "Python subpackage"
│       ├── __init__.py  # 
├── tests                  # app directory architecture 에 맞게 unit test 구성
│   ├── __init__.py      # 
│   └── routers          # 
│   │   ├── __init__.py  # 
│   │   ├── test_items.py     # 
│   │   └── test_users.py     # 
│   └── internal         # 
│       ├── __init__.py  # 
│       └── test_admin.py     # 
│   └── src         # 
│       ├── __init__.py  #
```

- **routers**: API Endpoint. 작성한 API들은 `$HOME/app/main.py`에 router를 추가한다. (ex. `app.include_router(users.router)`)
- **src**: 모듈 메인 기능
- unit test
  - 👉 유닛 테스트는 기본적으로 `$HOME/app`의 디렉토리 구조에 맞게 구성한다.
  - 유닛 테스트 종류로는 기능 테스트, API 엔드포인트 테스트, Pydantic 모델 유효성 테스트, 보안 테스트가 있다.
- **Dockerfile**
  - `Dockerfile`(=Dockerfile.dev 역할): 개발을 위해 필요한 도구 및 라이브러리와 같은 추가적인 종속성을 설치하기 위한 라이브러리들이 설치된 환경
  - `product.Dockerfile`: 최종 제품을 배포하기 위해 필요한 것들만 포함한 환경


## MSA: 내부망
### 배포 가이드
1. `pyproject.toml` 작성 (참고: [Declaring project metadata](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/))
   - project 메타데이터 작성 (_name_, _version_, ... etc)
   - 의존성 작성: _dependencies_
   - 개발 의존성 작성: _project.optional-dependencies_
2. 패키지 whl 파일 내려받기
   1. 내부망과 동일한 운영체제, 아키텍처, 파이썬 버전으로 `pip download $HOME[pyproject.toml이 위치한 경로] --dest [다운로드 받은 wheel파일 경로]` 진행
       - (ex) `pip download . --dest .\pypi\package\`
   2. 파이썬 모듈 내부에 아래와 같은 구조로 준비 완료

### 실행가이드
1. 가상 환경 구성 및 진입
   1. 가상 환경 구성: `python -m venv venv`
   2. 가상 환경 진입: `.\venv\Scripts\activate` or `source .venv/bin/activate`
2. 의존성 설치: `pip install $HOME[pyproject.toml이 위치한 경로] --no-index --find-links [wheel 파일 경로]`
   - (ex) `pip install . --no-index --find-links $HOME\pypi\package\*.whl`
3. `python app/main.py` 실행


## Monolith @TODO
> @tiangolo 가 제공하는 유형(예: api, crud, 모델, 스키마)별로 파일을 구분하는 프로젝트 구조는 범위가 적은 마이크로 서비스 또는 프로젝트에 적합하지만 많은 도메인이 있는 모놀리식에는 맞출 수 없다.
> 더 확장 가능하고 진화할 수 있는 구조는 Netflix의 Dispatch 에서 영감을 얻었다.
- 출처: https://github.com/zhanymkanov/fastapi-best-practices


## 🚀 TODO
- [ ] **monolith** 개발 (현재 디렉터리만 생성되어있어 사용 불가능) 
- [ ] DB 적용한 API 동작 테스트
- [ ] Restful API 디자인 가이드: API token을 JWT token으로 설정
- [ ] Restful API 디자인 가이드: filtering, sorting, searching 기능을 query string으로 적용하기
- [ ] Restful API 디자인 가이드: 버전 관리 (버전별 URL 표기)
- [ ] Restful API 디자인 가이드: 링크 처리시 HATEOS를 이용한 링크 처리
- [ ] 에러 처리
- [ ] ELK 로그