from unittest import mock

from fastapi import status
from fastapi.testclient import TestClient

from app.core.dependencies import get_current_user
from app.main import app
from app.schemas.photo import Photo
from app.schemas.user import User
from ...factories import PhotoDBFactory, UserDBFactory


class TestGetMetadataList:
    def test_empty(self, app_test):
        client = TestClient(app_test)

        r = client.get(app.url_path_for("Get photos metadata"))

        assert r.status_code == status.HTTP_200_OK
        assert r.json() == []

    def test_1_photo(self, app_test):
        client = TestClient(app_test)

        photo1 = PhotoDBFactory()

        r = client.get(app.url_path_for("Get photos metadata"))

        assert r.status_code == status.HTTP_200_OK
        assert len(r.json()) == 1

    def test_3_photos(self, app_test):
        client = TestClient(app_test)

        photo1 = PhotoDBFactory()
        photo2 = PhotoDBFactory()
        photo3 = PhotoDBFactory()

        r = client.get(app.url_path_for("Get photos metadata"))

        assert r.status_code == status.HTTP_200_OK
        assert len(r.json()) == 3


class TestGetMetadata:
    def test_not_found(self, app_test):
        client = TestClient(app_test)

        r = client.get(app.url_path_for("Get photo metadata", id=1))

        assert r.status_code == status.HTTP_404_NOT_FOUND

    def test_found(self, app_test):
        client = TestClient(app_test)

        photo = PhotoDBFactory()
        r = client.get(app.url_path_for("Get photo metadata", id=photo.id))

        assert r.status_code == status.HTTP_200_OK


class TestUpdateMetadata:
    def test_update(self, app_test):
        user = UserDBFactory()
        app_test.dependency_overrides[get_current_user] = lambda: User.model_validate(
            user
        )
        client = TestClient(app_test)
        new_data = {
            "description": "New description",
        }

        photo = PhotoDBFactory(owner=user)

        r = client.put(
            app.url_path_for("Update photo metadata", id=photo.id), json=new_data
        )

        assert r.status_code == status.HTTP_200_OK
        assert r.json()["description"] == new_data["description"]

    def test_not_found(self, app_test):
        user = UserDBFactory()
        app_test.dependency_overrides[get_current_user] = lambda: User.model_validate(
            user
        )
        client = TestClient(app_test)
        new_data = {
            "description": "New description",
        }

        r = client.put(app.url_path_for("Update photo metadata", id=1), json=new_data)

        assert r.status_code == status.HTTP_404_NOT_FOUND

    def test_unauthenticated(self, app_test):
        client = TestClient(app_test)
        new_data = {
            "description": "New description",
        }

        photo = PhotoDBFactory()

        r = client.put(
            app.url_path_for("Update photo metadata", id=photo.id), json=new_data
        )

        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unauthorized(self, app_test):
        user = UserDBFactory()
        app_test.dependency_overrides[get_current_user] = lambda: User.model_validate(
            user
        )
        client = TestClient(app_test)
        new_data = {
            "description": "New description",
        }

        photo = PhotoDBFactory()

        r = client.put(
            app.url_path_for("Update photo metadata", id=photo.id), json=new_data
        )

        assert r.status_code == status.HTTP_403_FORBIDDEN


class TestCreate:
    def test_create(self, app_test, test_file_jpg):
        user = UserDBFactory()
        app_test.dependency_overrides[get_current_user] = lambda: User.model_validate(
            user
        )
        client = TestClient(app_test)
        data = {
            "description": "Description",
        }

        r = client.post(
            app.url_path_for("Upload photo"), data=data, files={"file": test_file_jpg}
        )

        assert r.status_code == status.HTTP_201_CREATED

    def test_unauthenticated(self, app_test, test_file_jpg):
        client = TestClient(app_test)
        data = {
            "description": "Description",
        }

        r = client.post(
            app.url_path_for("Upload photo"), data=data, files={"file": test_file_jpg}
        )

        assert r.status_code == status.HTTP_401_UNAUTHORIZED


class TestDelete:
    @mock.patch("app.api.endpoints.photos.photo_service.delete_photo")
    def test_delete(self, delete_photo_mock, app_test):
        user = UserDBFactory()
        app_test.dependency_overrides[get_current_user] = lambda: User.model_validate(
            user
        )
        delete_photo_mock.return_value = None
        client = TestClient(app_test)

        photo = PhotoDBFactory(owner=user)

        r = client.delete(app.url_path_for("Delete photo", id=photo.id))

        assert r.status_code == status.HTTP_204_NO_CONTENT

    def test_unauthorized(self, app_test):
        client = TestClient(app_test)

        photo = PhotoDBFactory()

        r = client.delete(app.url_path_for("Delete photo", id=photo.id))

        assert r.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetFile:
    @mock.patch("app.api.endpoints.photos.photo_service.get_photo_filepath")
    def test_get(self, get_photo_filepath_mock, app_test):
        get_photo_filepath_mock.return_value = "tests/test_pictures/pict.jpg"
        client = TestClient(app_test)

        photo = PhotoDBFactory()

        r = client.get(app.url_path_for("Get photo file", id=photo.id))

        assert r.status_code == status.HTTP_200_OK

    def test_not_found(self, app_test):
        client = TestClient(app_test)

        r = client.get(app.url_path_for("Get photo file", id=1))

        assert r.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateFile:
    @mock.patch("app.api.endpoints.photos.photo_service.update_photo_file")
    def test_update(self, update_photo_file_mock, app_test, test_file_jpg):
        user = UserDBFactory()
        app_test.dependency_overrides[get_current_user] = lambda: User.model_validate(
            user
        )
        client = TestClient(app_test)

        photo = PhotoDBFactory(owner=user)
        update_photo_file_mock.return_value = Photo.model_validate(photo)

        r = client.put(
            app.url_path_for("Update photo file", id=photo.id),
            files={"file": test_file_jpg},
        )

        assert r.status_code == status.HTTP_200_OK

    def test_unauthenticated(self, app_test, test_file_jpg):
        client = TestClient(app_test)

        photo = PhotoDBFactory()

        r = client.put(
            app.url_path_for("Update photo file", id=photo.id),
            files={"file": test_file_jpg},
        )

        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authorized(self, app_test, test_file_jpg):
        user = UserDBFactory()
        app_test.dependency_overrides[get_current_user] = lambda: User.model_validate(
            user
        )
        client = TestClient(app_test)

        photo = PhotoDBFactory()

        r = client.put(
            app.url_path_for("Update photo file", id=photo.id),
            files={"file": test_file_jpg},
        )

        assert r.status_code == status.HTTP_403_FORBIDDEN
