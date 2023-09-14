from ...conftest import client
from app.routers import status


def test_status(client):
    r = client.get(status.router.url_path_for("index"))
    assert r.status_code == 200  # 200 OK
