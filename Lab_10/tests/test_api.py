from fastapi.testclient import TestClient

def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_and_get_student(client: TestClient):
    response = client.post("/students", json={"name": "Ivan Franko", "group_name": "IP-21"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Ivan Franko"
    assert "id" in data