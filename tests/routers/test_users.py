from fastapi.testclient import TestClient

from app import SERVICE_CODE
from app.main import app
from app.dependencies import DEFAULT_X_TOKEN

client = TestClient(app)


def test_read_users():
    response = client.get("/users", headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(str(SERVICE_CODE) + "200"),
        "message": "API response success",
        "result": {
            'users': [{'username': 'Rick'}, {'username': 'Morty'}]
        },
        "description": ""
    }


def test_read_user_me():
    response = client.get("/users/me", headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(str(SERVICE_CODE) + "200"),
        "message": "API response success",
        "result": {
            "username": "fakecurrentuser"
        },
        "description": ""
    }


def test_read_user():
    user_name = "sally"
    response = client.get(f"/users/{user_name}", headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(str(SERVICE_CODE) + "200"),
        "message": "API response success",
        "result": {
            "username": "sally"
        },
        "description": ""
    }
