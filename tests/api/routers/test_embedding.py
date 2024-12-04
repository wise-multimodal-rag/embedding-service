import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from tests.conftest import sbert_default_model_name, doc2vec_default_model_name

client = TestClient(app)


def test_embedding_doc2vec(single_docs_example):
    request_body = {
        "input": single_docs_example,
        "model": doc2vec_default_model_name
    }
    response = client.post("/embeddings/doc2vec", json=request_body, headers={"x-token": settings.X_TOKEN})
    assert response.status_code == 200
    response_json = response.json()
    print(response_json)
    assert list(response_json.keys()) == ["code", "message", "result", "description"]
    assert response_json["code"] == int(f"{settings.SERVICE_CODE}200")


@pytest.mark.skip("모델 저장 이슈로 일단 스킵")
def test_embedding_use(single_docs_example):
    request_body = {
        "input": single_docs_example,
        "model": "use-model"
    }
    response = client.post("/embeddings/use", json=request_body, headers={"x-token": settings.X_TOKEN})
    assert response.status_code == 200
    response_json = response.json()
    print(response_json)
    assert list(response_json.keys()) == ["code", "message", "result", "description"]
    assert response_json["code"] == int(f"{settings.SERVICE_CODE}200")


def test_embedding_sbert(single_docs_example):
    request_body = {
        "input": single_docs_example,
        "model": sbert_default_model_name
    }
    response = client.post("/embeddings/sbert", json=request_body, headers={"x-token": settings.X_TOKEN})
    assert response.status_code == 200
    response_json = response.json()
    print(response_json)
    assert list(response_json.keys()) == ["code", "message", "result", "description"]
    assert response_json["code"] == int(f"{settings.SERVICE_CODE}200")
