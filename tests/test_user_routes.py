from fastapi.testclient import TestClient

from user_module.main import app


def test_return_name():
    with TestClient(app) as client:
        response = client.get("/api/users/name")

    assert response.status_code == 200
    assert response.json() == {"name": "John Doe"}
