from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_1():
    response = client.get("/facebook")
    assert response.status_code == 200


def test_2():
    response = client.get("/facebook")
    assert response.status_code == 400


def test_3():
    response = client.get("/facebook")
    assert response.status_code == 404


    