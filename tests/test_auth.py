import pytest
from myapp import create_app
from myapp.extensions import db


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SECRET_KEY": "test",
    })
    with app.test_client() as c:
        yield c
    with app.app_context():
        db.drop_all()


def register(client, email="budi@example.com"):
    return client.post("/register", data={
        "username": "budi", "email": email,
        "password": "rahasia123", "confirm": "rahasia123",
    }, follow_redirects=True)


def login(client, password="rahasia123", url="/login"):
    return client.post(url, data={
        "email": "budi@example.com", "password": password,
    })


def test_dashboard_requires_login(client):
    r = client.get("/dashboard")
    assert r.status_code == 302
    assert "/login?next=%2Fdashboard" in r.headers["Location"]


def test_register_and_duplicate(client):
    assert b"Registrasi berhasil" in register(client).data
    assert b"Email sudah terdaftar" in register(client).data


def test_login_success_and_access(client):
    register(client)
    r = login(client)
    assert r.status_code == 302 and r.headers["Location"].endswith("/dashboard")
    assert b"budi" in client.get("/dashboard").data


def test_login_wrong_password(client):
    register(client)
    r = login(client, password="salah-banget")
    assert b"Email atau password salah" in r.data
    assert client.get("/dashboard").status_code == 302


def test_logout(client):
    register(client)
    login(client)
    client.post("/logout")
    assert client.get("/dashboard").status_code == 302


def test_next_redirect_internal(client):
    register(client)
    r = login(client, url="/login?next=/dashboard")
    assert r.headers["Location"].endswith("/dashboard")


def test_open_redirect_blocked(client):
    register(client)
    r = login(client, url="/login?next=https://evil.example.com")
    assert "evil.example.com" not in r.headers["Location"]
    r2 = login(client, url="/login?next=//evil.example.com")
    assert "evil.example.com" not in r2.headers["Location"]
