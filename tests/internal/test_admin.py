from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

client = TestClient(app)


def test_update_admin():
    response = client.post(url="/admin", headers={"x-token": settings.X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(str(settings.SERVICE_CODE) + "200"),
        "message": "Admin getting schwifty",
        "result": {},
        "description": ""
    }
