from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_customer():
    response = client.post("/customers/", json={"name": "Test User", "code": "+123456789"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"

def test_create_order():
    response = client.post("/orders/", json={"customer_id": 1, "item": "Test Item", "amount": 10})
    assert response.status_code == 200
    assert response.json()["item"] == "Test Item"

