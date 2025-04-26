#/test/test_belajar.py
import pytest
from app import app  # Import aplikasi Flask dari file app.py

@pytest.fixture
def client():
    # Setup Flask test client
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hallo_endpoint(client):
    # Kirim request GET ke endpoint /hallo
    response = client.get('/halo')
    # Pastikan status kode adalah 200
    assert response.status_code == 200
    # Pastikan respon JSON sesuai
    assert response.get_json() == {"message": "Belajar Flask"}

def test_halo_nama(client):
    response = client.get('/nama/silmi')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Halo silmi"}

def test_post_halo(client):
    payload = {"nama": "Silmi", "alamat": "Semarang"}
    response = client.post('/halo', json=payload)
    assert response.status_code == 200
    assert response.get_json() == payload