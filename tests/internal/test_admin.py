from fastapi.testclient import TestClient

from app import SERVICE_CODE
from app.main import app
from app.dependencies import DEFAULT_X_TOKEN

client = TestClient(app)


def test_update_admin():
    response = client.post(url="/admin", headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(str(SERVICE_CODE) + "200"),
        "message": "Admin getting schwifty",
        "result": {},
        "description": ""
    }
