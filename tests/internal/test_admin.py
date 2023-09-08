from fastapi.testclient import TestClient

from app import SERVICE_CODE, X_TOKEN
from app.main import app

client = TestClient(app)


def test_update_admin():
    response = client.post(url="/admin", headers={"x-token": X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(str(SERVICE_CODE) + "200"),
        "message": "Admin getting schwifty",
        "result": {},
        "description": ""
    }
