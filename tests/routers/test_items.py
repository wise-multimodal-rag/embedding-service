from fastapi.testclient import TestClient

from app import SERVICE_CODE
from app.main import app
from app.dependencies import DEFAULT_X_TOKEN

client = TestClient(app)


def test_read_items():
    response = client.get("/items", headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(str(SERVICE_CODE) + "200"),
        "message": "API response success",
        "result": {
            "plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}
        },
        "description": ""
    }


def test_read_item():
    item_id = "gun"
    response = client.get(f"/items/{item_id}", headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(str(SERVICE_CODE) + "200"),
        "message": "API response success",
        "result": {
            "name": "Portal Gun",
            "item_id": "gun"
        },
        "description": ""
    }


def test_update_item():
    item_id = "plumbus"
    response = client.put(f"/items/{item_id}", headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": int(str(SERVICE_CODE) + "200"),
        "message": "API response success",
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
    response = client.post(url="/items", headers={"x-token": DEFAULT_X_TOKEN},
                           json=item)
    assert response.status_code == 200
    assert response.json()["result"]["item"]["name"] == item["name"]
    assert response.json()["result"]["item"]["status"] == item["status"]
    assert response.json()["result"]["item"]["stock"] == item["stock"]
