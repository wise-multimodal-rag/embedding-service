from fastapi.testclient import TestClient

from app import SERVICE_CODE, Log, X_TOKEN
from app.main import app
from app.version import VERSION

client = TestClient(app)


def test_read_items():
    response = client.get("/items", headers={"x-token": X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(f"{SERVICE_CODE}200"),
        "message": f"API Response Success ({VERSION})" if Log.is_debug_enable() else "API Response Success",
        "result": {
            "plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}
        },
        "description": ""
    }


def test_read_item():
    item_id = "gun"
    response = client.get(f"/items/{item_id}", headers={"x-token": X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(f"{SERVICE_CODE}200"),
        "message": f"API Response Success ({VERSION})" if Log.is_debug_enable() else "API Response Success",
        "result": {
            "name": "Portal Gun",
            "item_id": "gun"
        },
        "description": ""
    }


def test_update_item():
    item_id = "plumbus"
    response = client.put(f"/items/{item_id}", headers={"x-token": X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(f"{SERVICE_CODE}200"),
        "message": f"API Response Success ({VERSION})" if Log.is_debug_enable() else "API Response Success",
        "result": {
            "item_id": "plumbus",
            "name": "The great Plumbus"
        },
        "description": ""
    }


def test_create_item():
    item = {
        "name": "apple",
        "status": "in stock",
        "stock": 10
    }
    response = client.post(url="/items", headers={"x-token": X_TOKEN},
                           json=item)
    assert response.status_code == 200
    assert response.json()["result"]["item"]["name"] == item["name"]
    assert response.json()["result"]["item"]["status"] == item["status"]
    assert response.json()["result"]["item"]["stock"] == item["stock"]
