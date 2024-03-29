from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from tests.conftest import embedding_model_name

client = TestClient(app)


def test_embeddings(single_docs_example):
    request_body = {
        "input": single_docs_example,
        "model": embedding_model_name
    }
    response = client.post("/embeddings", json=request_body, headers={"x-token": settings.X_TOKEN})
    assert response.status_code == 200
    response_json = response.json()
    print(response_json)
    assert list(response_json.keys()) == ["code", "message", "result", "description"]
    assert response_json["code"] == int(f"{settings.SERVICE_CODE}200")
