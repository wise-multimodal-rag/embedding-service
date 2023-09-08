from fastapi.testclient import TestClient

from app import SERVICE_CODE, X_TOKEN, Log
from app.main import app
from app.version import VERSION

client = TestClient(app)


def test_read_users():
    response = client.get("/users", headers={"x-token": X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(f"{SERVICE_CODE}200"),
        "message": f"API Response Success ({VERSION})" if Log.is_debug_enable() else "API Response Success",
        "result": {
            'users': [{'username': 'Rick'}, {'username': 'Morty'}]
        },
        "description": ""
    }


def test_read_user_me():
    response = client.get("/users/me", headers={"x-token": X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(f"{SERVICE_CODE}200"),
        "message": f"API Response Success ({VERSION})" if Log.is_debug_enable() else "API Response Success",
        "result": {
            "username": "fakecurrentuser"
        },
        "description": ""
    }


def test_read_user():
    user_name = "sally"
    response = client.get(f"/users/{user_name}", headers={"x-token": X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(f"{SERVICE_CODE}200"),
        "message": f"API Response Success ({VERSION})" if Log.is_debug_enable() else "API Response Success",
        "result": {
            "username": "sally"
        },
        "description": ""
    }
