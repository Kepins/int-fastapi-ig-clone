from fastapi import status

from app.main import app
from tests.conftest import client
from tests.factories import UserDBFactory


class TestGetList:
    def test_empty(self, client):
        r = client.get(app.url_path_for("Get all users"))

        assert r.status_code == status.HTTP_200_OK
        assert r.json() == []

    def test_1_user(self, client):
        user1 = UserDBFactory()

        r = client.get(app.url_path_for("Get all users"))

        assert r.status_code == status.HTTP_200_OK
        assert len(r.json()) == 1

    def test_3_users(self, client):
        user1 = UserDBFactory()
        user2 = UserDBFactory()
        user3 = UserDBFactory()

        r = client.get(app.url_path_for("Get all users"))

        assert r.status_code == status.HTTP_200_OK
        assert len(r.json()) == 3


class TestGet:
    def test_not_found(self, client):
        r = client.get(app.url_path_for("Get user", id=1))

        assert r.status_code == status.HTTP_404_NOT_FOUND

    def test_found(self, client):
        user = UserDBFactory()
        r = client.get(app.url_path_for("Get user", id=user.id))

        assert r.status_code == status.HTTP_200_OK


class TestCreate:
    def test_create(self, client):
        user_data = {
            "first_name": "Jan",
            "last_name": "Kowalski",
            "nickname": "Janex",
            "email": "jan.kowalski@example.com",
            "password": "password",
        }

        r = client.post(app.url_path_for("Create user"), json=user_data)

        assert r.status_code == status.HTTP_201_CREATED
        assert r.json()["first_name"] == user_data["first_name"]
        assert r.json()["last_name"] == user_data["last_name"]
        assert r.json()["nickname"] == user_data["nickname"]
        assert "id" in r.json()
        assert "email" not in r.json()
        assert "password" not in r.json()
