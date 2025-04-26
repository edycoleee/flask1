import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

username = "testuser"
password = "testpass"

def test_register(client):
    response = client.post('/register', json={
        "username": username,
        "password": password
    })
    assert response.status_code in [201, 409]  # 201 (baru), 409 (sudah ada)

def test_login(client):
    response = client.post('/login', json={
        "username": username,
        "password": password
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert "token" in json_data
    # Simpan token untuk test berikutnya
    global TOKEN
    TOKEN = json_data["token"]

# def test_read_all_siswa_with_token(client):
#     headers = {"Authorization": TOKEN}
#     response = client.get('/siswa', headers=headers)
#     assert response.status_code == 200
#     assert isinstance(response.get_json(), list)

def test_logout(client):
    headers = {"Authorization": TOKEN}
    response = client.post('/logout', headers=headers)
    assert response.status_code == 200
    assert response.get_json().get("message") == "Logout berhasil"
