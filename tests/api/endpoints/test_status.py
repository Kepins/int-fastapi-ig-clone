from ...conftest import client
from app.main import app


def test_status(client):
    r = client.get(app.url_path_for("status"))
    assert r.status_code == 200  # 200 OK
