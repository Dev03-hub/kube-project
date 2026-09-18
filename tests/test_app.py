import pytest

from app.app import app, users


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_users():
    users.clear()
    users.append({
        "id": 1,
        "name": "Debraj"
    })


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["application"] == "user-service"
    assert data["status"] == "running"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"


def test_get_users(client):
    response = client.get("/users")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert data[0]["name"] == "Debraj"


def test_add_user(client):
    response = client.post(
        "/users",
        json={"name": "Alice"}
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "User added"
    assert data["user"]["name"] == "Alice"


def test_add_user_without_name(client):
    response = client.post(
        "/users",
        json={}
    )

    assert response.status_code == 400
