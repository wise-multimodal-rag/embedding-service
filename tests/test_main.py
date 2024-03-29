from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/", headers={"x-token": settings.X_TOKEN})
    assert response.status_code == 200
    assert response.json()["title"] == app.title
    assert response.json()["summary"] == app.summary
    assert response.json()["version"] == app.version
    assert response.json()["docs_url"] == app.docs_url


def test_health():
    response = client.get("/health", headers={"x-token": settings.X_TOKEN})
    assert response.status_code == 200


def test_info():
    response = client.get("/info", headers={"x-token": settings.X_TOKEN})
    assert response.status_code == 200
