from fastapi import status
from fastapi.testclient import TestClient

from app.core.dependencies import get_current_user
from app.core.security import Hasher
from app.main import app
from app.schemas.user import User
from tests.factories import UserDBFactory


class TestAccountUpdate:
    def test_update(self, app_test):
        user = UserDBFactory()
        app_test.dependency_overrides[get_current_user] = lambda: User.model_validate(
            user
        )
        client = TestClient(app_test)
        new_data = {
            "first_name": "Jacek",
            "last_name": " Kowalski",
        }

        r = client.put(app.url_path_for("Update account"), json=new_data)

        # Test response
        assert r.status_code == status.HTTP_200_OK
        assert r.json()["first_name"] == new_data["first_name"]
        assert r.json()["last_name"] == new_data["last_name"]

    def test_unauthenticated(self, app_test):
        client = TestClient(app_test)
        new_data = {
            "first_name": "Jacek",
            "last_name": " Kowalski",
        }

        r = client.put(app.url_path_for("Update account"), json=new_data)

        # Test response
        assert r.status_code == status.HTTP_401_UNAUTHORIZED


class TestAccountLogin:
    def test_login(self, app_test):
        pass


class TestAccountResetPassword:
    def test_reset_password(self, app_test):
        user = UserDBFactory(pass_hash=Hasher.get_password_hash("password123"))
        app_test.dependency_overrides[get_current_user] = lambda: User.model_validate(
            user
        )
        client = TestClient(app_test)
        passwords = {
            "old_password": "password123",
            "new_password": " Password1234",
        }

        r = client.post(app.url_path_for("Reset account password"), json=passwords)

        assert r.status_code == status.HTTP_200_OK

    def test_invalid_old_password(self, app_test):
        user = UserDBFactory(pass_hash=Hasher.get_password_hash("password123"))
        app_test.dependency_overrides[get_current_user] = lambda: User.model_validate(
            user
        )
        client = TestClient(app_test)
        passwords = {
            "old_password": "password1234",
            "new_password": " Password1234",
        }

        r = client.post(app.url_path_for("Reset account password"), json=passwords)

        assert r.status_code == status.HTTP_400_BAD_REQUEST

    def test_unauthenticated(self, app_test):
        client = TestClient(app_test)
        passwords = {
            "old_password": "password1234",
            "new_password": " Password1234",
        }

        r = client.post(app.url_path_for("Reset account password"), json=passwords)

        assert r.status_code == status.HTTP_401_UNAUTHORIZED


class TestAccountDelete:
    def test_delete(self, app_test):
        user = UserDBFactory()
        app_test.dependency_overrides[get_current_user] = lambda: User.model_validate(
            user
        )
        client = TestClient(app_test)

        r = client.delete(app.url_path_for("Delete account"))

        assert r.status_code == status.HTTP_204_NO_CONTENT

    def test_unauthenticated(self, app_test):
        client = TestClient(app_test)

        r = client.delete(app.url_path_for("Delete account"))

        assert r.status_code == status.HTTP_401_UNAUTHORIZED
