#/test/test_siswa.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_siswa(client):
    response = client.post('/siswa', json={"nama": "Test", "alamat": "Bandung"})
    assert response.status_code == 201
    assert b"Siswa berhasil ditambahkan" in response.data

def test_get_all_siswa(client):
    response = client.get('/siswa')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_siswa_by_id(client):
    # Buat siswa terlebih dahulu
    create = client.post('/siswa', json={"nama": "Andi", "alamat": "Jogja"})
    assert create.status_code == 201

    # Ambil siswa terakhir
    siswa = client.get('/siswa').get_json()[-1]
    id_siswa = siswa['id']

    # Test ambil berdasarkan ID
    response = client.get(f'/siswa/{id_siswa}')
    assert response.status_code == 200
    assert response.get_json()['nama'] == "Andi"

def test_update_siswa(client):
    # Buat siswa terlebih dahulu
    create = client.post('/siswa', json={"nama": "Budi", "alamat": "Solo"})
    siswa = client.get('/siswa').get_json()[-1]
    id_siswa = siswa['id']

    # Update data
    response = client.put(f'/siswa/{id_siswa}', json={"nama": "Budi Update", "alamat": "Solo Baru"})
    assert response.status_code == 200
    assert b"Siswa berhasil diperbarui" in response.data

def test_delete_siswa(client):
    # Buat siswa terlebih dahulu
    create = client.post('/siswa', json={"nama": "Citra", "alamat": "Bogor"})
    siswa = client.get('/siswa').get_json()[-1]
    id_siswa = siswa['id']

    # Hapus siswa
    response = client.delete(f'/siswa/{id_siswa}')
    assert response.status_code == 200
    assert b"Siswa berhasil dihapus" in response.data

    # Pastikan sudah dihapus
    check = client.get(f'/siswa/{id_siswa}')
    assert check.status_code == 404
