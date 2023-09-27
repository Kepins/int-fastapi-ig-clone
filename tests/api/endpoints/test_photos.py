from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from ...factories import PhotoDBFactory


class TestGetMetadataList:
    def test_empty(self, app_test):
        client = TestClient(app_test)

        r = client.get(app.url_path_for("Get photos metadata"))

        assert r.status_code == status.HTTP_200_OK
        assert r.json() == []

    def test_one(self, app_test):
        client = TestClient(app_test)

        photo1 = PhotoDBFactory()

        r = client.get(app.url_path_for("Get photos metadata"))

        assert r.status_code == status.HTTP_200_OK
        assert len(r.json()) == 1