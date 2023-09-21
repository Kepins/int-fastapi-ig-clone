from fastapi.testclient import TestClient

from app.main import app


def test_status(app_test):
    client = TestClient(app_test)
    r = client.get(app.url_path_for("status"))
    assert r.status_code == 200  # 200 OK
