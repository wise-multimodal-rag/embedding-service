# Embedding Service

![PythonVersion](https://img.shields.io/badge/python-3.9.13-blue)
![FastAPIVersion](https://img.shields.io/badge/fastapi-0.110.0-yellowgreen)
![loguru](https://img.shields.io/badge/loguru-0.7.2-orange)

## Index

- [Overview](#overview)
- [Getting Started](#getting-started)

## Overview

모델을 사용하여 텍스트 임베딩 결과를 제공하는 서비스
> **클러스터 환경에서 MiniO에 저장된 모델을 사용하여 텍스트 임베딩 결과를 제공**하는 것을 기본으로 한다.

- Embeddings
  - Doc2Vec
  - USE (Universal Sentence Encoder)
  - Sentence BERT

## Getting started

- local run
    - `$HOME/main.py`
        - `FileNotFoundError` or `ImportError` 발생시 _Working Directory_ (Working Directory = `$HOME`) 확인하기
    - _http :8000/openapi.json_ or _http://localhost:8000/docs_ 로 API 명세 확인 및 테스트
- docker run    
  `docker build ...` && `docker run -d -p ...` 로 컨테이너 빌드 & 구동
  ```shell
  # 도커 이미지 빌드
  docker build -t embedding-service:latest -f Dockerfile .
  # 컨테이너 구동
  docker run -d --name embedding-service -p 8000:8000 -e X_TOKEN=fake-super-secret-token embedding-service:latest
  ```

## Authors

- **Seoyeon Park** - <sally9476@wisenut.ac.kr>
- **Jungheon Jeong** - <legagain@wisenut.ac.kr>

## License

@Wisenut