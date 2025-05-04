### 1. API SEDERHANA

| No  | Method | Endpoint       | Request Body (JSON)                         | Response (JSON)                             |
| --- | ------ | -------------- | ------------------------------------------- | ------------------------------------------- |
| 1   | GET    | `/halo`        | (tidak ada)                                 | `{ "message": "Belajar Flask" }`            |
| 2   | GET    | `/nama/<nama>` | (tidak ada)                                 | `{ "message": "Halo silmi" }`               |
| 3   | POST   | `/halo`        | `{ "nama": "Silmi", "alamat": "Semarang" }` | `{ "nama": "Silmi", "alamat": "Semarang" }` |

1. Request : GET /halo
   Response

```json
{ "message": "Belajar Flask" }
```

2. Request : GET /nama/<nama>
   Response

```json
{ "message": "Halo silmi" }
```

3. Request : POST /halo
   Request Body : content type json

```json
{ "nama": "Silmi", "alamat": "Semarang" }
```

Response

```json
{ "nama": "Silmi", "alamat": "Semarang" }
```

#### 1. VIRTUAL ENVIRONTMENT

```py
# 1. Membuat Virtual Environtment
python -m venv venv
source venv/bin/activate  #Linux / Macbook
venv\Scripts\activate # Windows

#2. Install Flask
pip install flask
```

#### 2. API GET /halo

Struktur Folder

```cmd
project-folder/
│
├── app.py
└── test_app.py
```

```py
#3. app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/halo', methods=['GET'])
def halo():
    return jsonify({"message": "Belajar Flask"})

if __name__ == '__main__':
    app.run(debug=True)
#Jika dengan docker : app.run(host='0.0.0.0', port=5000)

#4. Jalankan
python app.py

#5. Coba Di browser / Postman
http://127.0.0.1:5000/halo

{
    "message": "Belajar Flask"
}

```

#### 3. TEST GET /halo

```py
#6. Membuat Unit Test
pip install pytest

#7. test_app.py
import pytest
from app import app  # Import aplikasi Flask dari file app.py

@pytest.fixture
def client():
    # Setup Flask test client
    with app.test_client() as client:
        yield client

def test_hallo_endpoint(client):
    # Kirim request GET ke endpoint /hallo
    response = client.get('/halo')
    # Pastikan status kode adalah 200
    assert response.status_code == 200
    # Pastikan respon JSON sesuai
    assert response.get_json() == {"message": "Belajar Flask"}

#8. Jalankan Test
pytest
```

#### 4. DOCUMENTATION GET /halo

```py
#9. Swagger API Documentation
pip install flasgger

#10. Update app.py
from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)  # Inisialisasi Flasgger

@app.route('/halo', methods=['GET'])
def halo():
    """
    Endpoint untuk mendapatkan pesan Halo Flask
    ---
    tags:
      - Halo
    responses:
      200:
        description: Respon sukses
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Halo Flask
    """
    return jsonify({"message": "Halo Flask"})

if __name__ == '__main__':
    app.run(debug=True)

#11. Lihat documentation
http://127.0.0.1:5000/apidocs/
```

#### 5. CLEAN CODE

```cmd
project-folder/
│
├── app.py
├── routes/
│   └── belajar.py
├── docs/
│   └── halo.yml
└── test/
    ├──__init__.py
    └── test_belajar.py


pip install flask_cors
```

Flasgger mengharapkan struktur YAML eksternal yang sesuai dengan format dokumen Swagger 2.0 — bukan OpenAPI 3.0

```py
# # # app.py >> ketiga dg cleancode
from flask import Flask
from flasgger import Swagger
from routes.belajar import belajar_bp  # perbaikan import
from flask_cors import CORS  # ✅ Tambahkan ini

app = Flask(__name__)
CORS(app)  # ✅ Aktifkan CORS untuk semua route
app.config['SWAGGER'] = {
    'title': 'COBA API',
    'uiversion': 3
}
swagger = Swagger(app)

# Register blueprint
app.register_blueprint(belajar_bp)

if __name__ == '__main__':
    app.run(debug=True)

#/routes/belajar.py
from flask import Blueprint, jsonify
from flasgger import swag_from
import os

belajar_bp = Blueprint('belajar_bp', __name__)

@belajar_bp.route('/halo', methods=['GET'])
@swag_from('../docs/halo.yml')
def get_halo():
    return jsonify({"message": "Belajar Flask"})

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
```

- Cara menjalankan test `pytest` atau `pytest test/test_belajar.py`

- docs/halo.yml

```yml
---
tags:
  - Belajar API GET POST
responses:
  200:
    description: Respon sukses
    schema:
      type: object
      properties:
        message:
          type: string
          example: Belajar Flask
```

- File **init**.py berisi file kosong

- request.rest

```cmd
### GET halo
GET http://127.0.0.1:5000/halo HTTP/1.1
```

#### 6. API GET /nama/silmi

Request : GET /nama/<nama>
Response

```json
{ "message": "Halo silmi" }
```

```cmd
project-folder/
│
├── app.py
├── routes/
│   └── belajar.py
├── docs/
│   ├── nama.yml
│   └── halo.yml
└── test/
    ├──__init__.py
    └── test_belajar.py
```

```py
# # # app.py >> ketiga dg cleancode
from flask import Flask
from flasgger import Swagger
from routes.belajar import belajar_bp  # perbaikan import
from flask_cors import CORS  # ✅ Tambahkan ini

app = Flask(__name__)
CORS(app)  # ✅ Aktifkan CORS untuk semua route
app.config['SWAGGER'] = {
    'title': 'COBA API',
    'uiversion': 3
}
swagger = Swagger(app)

# Register blueprint
app.register_blueprint(belajar_bp)

if __name__ == '__main__':
    app.run(debug=True)

#/routes/belajar.py
from flask import Blueprint, jsonify, request
from flasgger import swag_from
import os

belajar_bp = Blueprint('belajar_bp', __name__)

@belajar_bp.route('/halo', methods=['GET'])
@swag_from('../docs/halo.yml')
def get_halo():
    return jsonify({"message": "Belajar Flask"})

@belajar_bp.route('/nama/<nama>', methods=['GET'])
@swag_from('../docs/nama.yml')
def halo_nama(nama):
    return jsonify({"message": f"Halo {nama}"})
```

#### 7. TEST GET /nama/silmi

```py
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
```

```cmd
#/request.rest
### GET halo
GET http://127.0.0.1:5000/halo HTTP/1.1

###
GET http://127.0.0.1:5000/nama/silmi HTTP/1.1
```

#### 8. DOCUMENTATION GET /nama/silmi

```yml
---
tags:
  - Belajar API GET POST
parameters:
  - name: nama
    in: path
    type: string
    required: true
    description: Nama pengguna yang ingin disapa
responses:
  200:
    description: Respons sukses
    schema:
      type: object
      properties:
        message:
          type: string
          example: Halo silmi
```

#### 9. POST

Request : POST /halo

Request Body : content type json

```json
{ "nama": "Silmi", "alamat": "Semarang" }
```

Response

```json
{ "nama": "Silmi", "alamat": "Semarang" }
```

```cmd
project-folder/
│
├── app.py
├── routes/
│   └── belajar.py
├── docs/
│   ├── nama.yml
│   ├── halo_post.yml
│   └── halo.yml
└── test/
    ├──__init__.py
    └── test_belajar.py
```

```py
# tambahkan #/routes/belajar.py
@belajar_bp.route('/halo', methods=['POST'])
@swag_from('../docs/halo_post.yml')
def halo_post():
    from flask import request
    data = request.get_json()
    return jsonify({
        "nama": data.get("nama"),
        "alamat": data.get("alamat")
    })

#tambahkan #/test/test_belajar.py
def test_post_halo(client):
    payload = {"nama": "Silmi", "alamat": "Semarang"}
    response = client.post('/halo', json=payload)
    assert response.status_code == 200
    assert response.get_json() == payload

```

```yml
---
tags:
  - Belajar API GET POST
parameters:
  - in: body
    name: body
    required: true
    schema:
      type: object
      required:
        - nama
        - alamat
      properties:
        nama:
          type: string
          example: Silmi
        alamat:
          type: string
          example: Semarang
responses:
  200:
    description: Data berhasil diterima
    schema:
      type: object
      properties:
        nama:
          type: string
        alamat:
          type: string
```

```cmd
### POST /halo
POST http://127.0.0.1:5000/halo HTTP/1.1
content-type: application/json

{"nama": "Silmi", "alamat": "Semarang"}
```

### 2. API CRUD SISWA SQLITE

| No  | Method | Endpoint      | Request Body (JSON)                                | Response (JSON)                                               |
| --- | ------ | ------------- | -------------------------------------------------- | ------------------------------------------------------------- |
| 1   | POST   | `/siswa`      | `{ "nama": "Silmi", "alamat": "Semarang" }`        | `{ "message": "Siswa berhasil ditambahkan" }`                 |
| 2   | GET    | `/siswa`      | (tidak ada)                                        | `[ { "id": 1, "nama": "Silmi", "alamat": "Semarang" }, ... ]` |
| 3   | GET    | `/siswa/<id>` | (tidak ada)                                        | `{ "id": 1, "nama": "Silmi", "alamat": "Semarang" }`          |
| 4   | PUT    | `/siswa/<id>` | `{ "nama": "Silmi Updated", "alamat": "Jakarta" }` | `{ "message": "Siswa berhasil diperbarui" }`                  |
| 5   | DELETE | `/siswa/<id>` | (tidak ada)                                        | `{ "message": "Siswa berhasil dihapus" }`                     |

```cmd
project-folder/
├── app.py
├── routes/
│   ├── siswa.py         ← Semua endpoint siswa
│   └── belajar.py       ← Endpoint halo dan nama
├── docs/                ← Swagger YAML
│   ├── siswa_create.yml
│   ├── siswa_delete.yml
│   ├── siswa_update.yml
│   ├── siswa_read_all.yml
│   ├── siswa_read_id.yml
│   ├── nama.yml
│   ├── halo_post.yml
│   └── halo.yml
├── test/
│   ├── __init__.py
│   ├── test_siswa.py
│   └── test_belajar.py
└── siswa.db             ← File SQLite (otomatis dibuat)
```

```py
# # # app.py >> ketiga dg cleancode
from flask import Flask
from flasgger import Swagger
from flask_cors import CORS  # ✅ Tambahkan ini
import sqlite3

app = Flask(__name__)
CORS(app)  # ✅ Aktifkan CORS untuk semua route
app.config['SWAGGER'] = {
    'title': 'COBA API',
    'uiversion': 3
}
swagger = Swagger(app)

# Inisialisasi DB
def init_db():
    with sqlite3.connect('siswa.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tb_siswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                alamat TEXT NOT NULL
            )
        ''')

init_db()

# Register Blueprint
from routes.belajar import belajar_bp
from routes.siswa import siswa_bp

app.register_blueprint(belajar_bp)
app.register_blueprint(siswa_bp)

if __name__ == '__main__':
    app.run(debug=True)


#routes/siswa.py
from flask import Blueprint, request, jsonify
from flasgger.utils import swag_from
import sqlite3

siswa_bp = Blueprint('siswa', __name__)

@siswa_bp.route('/siswa', methods=['POST'])
@swag_from('../docs/siswa_create.yml')
def create_siswa():
    data = request.get_json()
    with sqlite3.connect('siswa.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tb_siswa (nama, alamat) VALUES (?, ?)", (data['nama'], data['alamat']))
        conn.commit()
    return jsonify({"message": "Siswa berhasil ditambahkan"}), 201

@siswa_bp.route('/siswa', methods=['GET'])
@swag_from('../docs/siswa_read_all.yml')
def get_all_siswa():
    with sqlite3.connect('siswa.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tb_siswa")
        rows = cursor.fetchall()
    result = [{"id": row[0], "nama": row[1], "alamat": row[2]} for row in rows]
    return jsonify(result)

@siswa_bp.route('/siswa/<int:id>', methods=['GET'])
@swag_from('../docs/siswa_read_id.yml')
def get_siswa_by_id(id):
    with sqlite3.connect('siswa.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tb_siswa WHERE id=?", (id,))
        row = cursor.fetchone()
    if row:
        return jsonify({"id": row[0], "nama": row[1], "alamat": row[2]})
    return jsonify({"message": "Siswa tidak ditemukan"}), 404

@siswa_bp.route('/siswa/<int:id>', methods=['PUT'])
@swag_from('../docs/siswa_update.yml')
def update_siswa(id):
    data = request.get_json()
    with sqlite3.connect('siswa.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tb_siswa SET nama=?, alamat=? WHERE id=?", (data['nama'], data['alamat'], id))
        conn.commit()
    return jsonify({"message": "Siswa berhasil diperbarui"})

@siswa_bp.route('/siswa/<int:id>', methods=['DELETE'])
@swag_from('../docs/siswa_delete.yml')
def delete_siswa(id):
    with sqlite3.connect('siswa.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tb_siswa WHERE id=?", (id,))
        conn.commit()
    return jsonify({"message": "Siswa berhasil dihapus"})


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


```

```yml
#docs/siswa_create.yml
---
tags:
  - Siswa
parameters:
  - in: body
    name: body
    required: true
    schema:
      type: object
      required:
        - nama
        - alamat
      properties:
        nama:
          type: string
          example: Budi
        alamat:
          type: string
          example: Jakarta
responses:
  201:
    description: Siswa berhasil ditambahkan
responses:
  201:
    description: Siswa berhasil ditambahkan
    content:
      application/json:
        example:
          message: Siswa berhasil ditambahkan
  500:
    description: Gagal menambahkan siswa

#/docs/siswa_read_all
---
tags:
  - Siswa
responses:
  200:
    description: Daftar semua siswa
    schema:
      type: array
      items:
        type: object
        properties:
          id:
            type: integer
          nama:
            type: string
          alamat:
            type: string

#siswa_read_id.yml
---
tags:
  - Siswa
parameters:
  - name: id
    in: path
    type: integer
    required: true
    description: ID siswa
responses:
  200:
    description: Detail siswa berdasarkan ID
    schema:
      type: object
      properties:
        id:
          type: integer
        nama:
          type: string
        alamat:
          type: string
  404:
    description: Siswa tidak ditemukan

#siswa_update.yml
---
tags:
  - Siswa
parameters:
  - name: id
    in: path
    type: integer
    required: true
    description: ID siswa yang akan diupdate
  - in: body
    name: body
    required: true
    schema:
      type: object
      required:
        - nama
        - alamat
      properties:
        nama:
          type: string
          example: Update Nama
        alamat:
          type: string
          example: Update Alamat
responses:
  200:
    description: Siswa berhasil diperbarui
  404:
    description: Siswa tidak ditemukan

#docs/siswa_delete.yml
---
tags:
  - Siswa
parameters:
  - name: id
    in: path
    type: integer
    required: true
    description: ID siswa yang akan dihapus
responses:
  200:
    description: Siswa berhasil dihapus
  404:
    description: Siswa tidak ditemukan
```

### 3. CLEAN CODE SISWA API

```cmd
project-folder/
│
├── app.py
├── routes/
│   ├── siswa.py
│   └── belajar.py
├── services/
│   └── siswa_service.py   ← 🆕 logika SQL dipindah ke sini
├── docs/
│   ├── siswa/
│   │   ├── create.yml
│   │   ├── read_all.yml
│   │   ├── read_id.yml
│   │   ├── update.yml
│   │   └──  delete.yml
│   └──(semua yaml tetap di sini)
└── test/
    └── (unit test tetap di sini)

```

```py
#services/siswa_service.py
import sqlite3

DATABASE = 'siswa.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_siswa(nama, alamat):
    conn = get_db_connection()
    conn.execute("INSERT INTO tb_siswa (nama, alamat) VALUES (?, ?)", (nama, alamat))
    conn.commit()
    conn.close()

def read_all_siswa():
    conn = get_db_connection()
    siswa = conn.execute("SELECT id, nama, alamat FROM tb_siswa").fetchall()
    conn.close()
    return [dict(row) for row in siswa]

def read_siswa_by_id(id):
    conn = get_db_connection()
    row = conn.execute("SELECT id, nama, alamat FROM tb_siswa WHERE id = ?", (id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_siswa(id, nama, alamat):
    conn = get_db_connection()
    cur = conn.execute("UPDATE tb_siswa SET nama = ?, alamat = ? WHERE id = ?", (nama, alamat, id))
    conn.commit()
    conn.close()
    return cur.rowcount

def delete_siswa(id):
    conn = get_db_connection()
    cur = conn.execute("DELETE FROM tb_siswa WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return cur.rowcount


#routes/siswa.py
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from services import siswa_service

siswa_bp = Blueprint('siswa', __name__)

@siswa_bp.route('/siswa', methods=['POST'])
@swag_from('docs/siswa_create.yml')
def create_siswa():
    try:
        data = request.get_json()
        siswa_service.create_siswa(data['nama'], data['alamat'])
        return jsonify({"message": "Siswa berhasil ditambahkan"}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Gagal menambahkan siswa"}), 500

@siswa_bp.route('/siswa', methods=['GET'])
@swag_from('docs/siswa_read_all.yml')
def read_all_siswa():
    try:
        data = siswa_service.read_all_siswa()
        return jsonify(data), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Gagal mengambil data"}), 500

@siswa_bp.route('/siswa/<int:id>', methods=['GET'])
@swag_from('docs/siswa_read_id.yml')
def read_siswa_by_id(id):
    try:
        data = siswa_service.read_siswa_by_id(id)
        if data:
            return jsonify(data), 200
        return jsonify({"error": "Siswa tidak ditemukan"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Gagal mengambil data"}), 500

@siswa_bp.route('/siswa/<int:id>', methods=['PUT'])
@swag_from('docs/siswa_update.yml')
def update_siswa(id):
    try:
        data = request.get_json()
        updated = siswa_service.update_siswa(id, data['nama'], data['alamat'])
        if updated:
            return jsonify({"message": "Siswa berhasil diperbarui"}), 200
        return jsonify({"error": "Siswa tidak ditemukan"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Gagal memperbarui siswa"}), 500

@siswa_bp.route('/siswa/<int:id>', methods=['DELETE'])
@swag_from('docs/siswa_delete.yml')
def delete_siswa(id):
    try:
        deleted = siswa_service.delete_siswa(id)
        if deleted:
            return jsonify({"message": "Siswa berhasil dihapus"}), 200
        return jsonify({"error": "Siswa tidak ditemukan"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Gagal menghapus siswa"}), 500


#test/test_siswa.py
import pytest
import sqlite3
from app import app

# Fixture untuk setup dan teardown database
@pytest.fixture(scope="function")
def client():
    # Ganti database dengan yang in-memory
    app.config['TESTING'] = True
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tb_siswa (id INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT, alamat TEXT)')
    conn.commit()

    # Inject connection ke service jika perlu (optional)

    with app.test_client() as client:
        # Setup data awal jika perlu
        client.post('/siswa', json={"nama": "Silmi", "alamat": "Semarang"})
        yield client

    # Teardown: tutup connection
    conn.close()

def test_create_siswa(client):
    response = client.post('/siswa', json={"nama": "Budi", "alamat": "Jogja"})
    assert response.status_code == 201
    assert response.json['message'] == "Siswa berhasil ditambahkan"

def test_read_all_siswa(client):
    response = client.get('/siswa')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_read_siswa_by_id(client):
    response = client.get('/siswa/1')
    assert response.status_code in [200, 404]

def test_update_siswa(client):
    response = client.put('/siswa/1', json={"nama": "Silmi Update", "alamat": "Bandung"})
    assert response.status_code in [200, 404]

def test_delete_siswa(client):
    response = client.delete('/siswa/1')
    assert response.status_code in [200, 404]


```

```cmd
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/edycoleee/flask1.git
git push -u origin main
```

### 4. AUTH

| No  | Method | URL       | Request JSON                                     | Response JSON (Berhasil)                          | Response JSON (Gagal)                                             |
| --- | ------ | --------- | ------------------------------------------------ | ------------------------------------------------- | ----------------------------------------------------------------- |
| 1   | POST   | /register | `{ "username": "user1", "password": "pass123" }` | `{ "message": "Registrasi berhasil" }`            | `409 Conflict`: `{ "error": "Username sudah digunakan" }`         |
| 2   | POST   | /login    | `{ "username": "user1", "password": "pass123" }` | `{ "message": "Login berhasil", "token": "..." }` | `401 Unauthorized`: `{ "error": "Username atau password salah" }` |
| 3   | POST   | /logout   | (Header: `Authorization: Bearer <token>`)        | `{ "message": "Logout berhasil" }`                | `401 Unauthorized`: `{ "error": "Token tidak valid" }`            |

```cmd

project-folder/
│
├── app.py
├── middleware/
│ └── auth_middleware.py ← 🆕 Di sini tempatnya token_required
├── routes/
│ ├── siswa.py
│ └── auth.py
├── services/
│ └── siswa_service.py
...
```

```py
#1. Tabel tb_user
#Tambahkan ini di init_db() di app.py:

conn.execute('''
    CREATE TABLE IF NOT EXISTS tb_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        token TEXT
    )
''')


#2. Folder routes/auth.py
from flask import Blueprint, request, jsonify
import sqlite3, uuid, hashlib

auth_bp = Blueprint('auth', __name__)
DB = 'siswa.db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = hash_password(data.get('password'))

    try:
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO tb_user (username, password) VALUES (?, ?)", (username, password))
        return jsonify({"message": "Registrasi berhasil"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username sudah digunakan"}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = hash_password(data.get('password'))

    with sqlite3.connect(DB) as conn:
        user = conn.execute("SELECT * FROM tb_user WHERE username = ? AND password = ?", (username, password)).fetchone()
        if user:
            token = str(uuid.uuid4())
            conn.execute("UPDATE tb_user SET token = ? WHERE username = ?", (token, username))
            return jsonify({"message": "Login berhasil", "token": token}), 200
        return jsonify({"error": "Username atau password salah"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token tidak ditemukan"}), 401

    with sqlite3.connect(DB) as conn:
        cur = conn.execute("UPDATE tb_user SET token = NULL WHERE token = ?", (token,))
        if cur.rowcount:
            return jsonify({"message": "Logout berhasil"}), 200
        return jsonify({"error": "Token tidak valid"}), 401


#3. Register Blueprint di app.py
from routes.auth import auth_bp
app.register_blueprint(auth_bp)

#4. Tambahkan Middleware Auth (Opsional) middleware/auth_middleware.py
#Untuk mengamankan endpoint siswa, bisa buat decorator @token_required:
from functools import wraps
from flask import request, jsonify
import sqlite3

DB = 'siswa.db'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token diperlukan'}), 401
        with sqlite3.connect(DB) as conn:
            user = conn.execute("SELECT * FROM tb_user WHERE token = ?", (token,)).fetchone()
            if not user:
                return jsonify({'error': 'Token tidak valid'}), 401
        return f(*args, **kwargs)
    return decorated


#5.route siswa seperti ini
@siswa_bp.route('/siswa', methods=['GET'])
@token_required
def read_all_siswa():
    ...

#6. File: test/test_auth.py
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

def test_read_all_siswa_with_token(client):
    headers = {"Authorization": TOKEN}
    response = client.get('/siswa', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_logout(client):
    headers = {"Authorization": TOKEN}
    response = client.post('/logout', headers=headers)
    assert response.status_code == 200
    assert response.get_json().get("message") == "Logout berhasil"

#python test/test_auth.py

```

- DOKUMENTASi

```
project-folder/
└── docs/
    └── auth/
        ├── register.yml
        ├── login.yml
        └── logout.yml

```

```yml
#auth/register.yml
tags:
  - Auth
parameters:
  - in: body
    name: body
    required: true
    schema:
      type: object
      required:
        - username
        - password
      properties:
        username:
          type: string
          example: silmi
        password:
          type: string
          example: silmi123
responses:
  201:
    description: Registrasi berhasil
  409:
    description: Username sudah digunakan

#auth/login.yml
tags:
  - Auth
parameters:
  - in: body
    name: body
    required: true
    schema:
      type: object
      required:
        - username
        - password
      properties:
        username:
          type: string
          example: silmi
        password:
          type: string
          example: silmi123
responses:
  200:
    description: Login berhasil, token dikembalikan
    schema:
      type: object
      properties:
        message:
          type: string
        token:
          type: string
  401:
    description: Username atau password salah

#auth/logout.yml
tags:
  - Auth
summary: Logout user berdasarkan token
produces:
  - application/json
parameters:
  - name: Authorization
    in: header
    required: true
    type: string
    description: Token user
responses:
  200:
    description: Logout berhasil
  401:
    description: Token tidak valid atau tidak ditemukan

```

- routes/auth.py

```py
#/routes/auth.py
from flask import Blueprint, request, jsonify
import sqlite3, uuid, hashlib
from flasgger.utils import swag_from

auth_bp = Blueprint('auth', __name__)
DB = 'siswa.db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/register', methods=['POST'])
@swag_from('../docs/auth/register.yml')
def register():
    data = request.get_json()
    username = data.get('username')
    password = hash_password(data.get('password'))

    try:
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO tb_user (username, password) VALUES (?, ?)", (username, password))
        return jsonify({"message": "Registrasi berhasil"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username sudah digunakan"}), 409

@auth_bp.route('/login', methods=['POST'])
@swag_from('../docs/auth/login.yml')
def login():
    data = request.get_json()
    username = data.get('username')
    password = hash_password(data.get('password'))

    with sqlite3.connect(DB) as conn:
        user = conn.execute("SELECT * FROM tb_user WHERE username = ? AND password = ?", (username, password)).fetchone()
        if user:
            token = str(uuid.uuid4())
            conn.execute("UPDATE tb_user SET token = ? WHERE username = ?", (token, username))
            return jsonify({"message": "Login berhasil", "token": token}), 200
        return jsonify({"error": "Username atau password salah"}), 401

@auth_bp.route('/logout', methods=['POST'])
@swag_from('../docs/auth/logout.yml')
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token tidak ditemukan"}), 401

    with sqlite3.connect(DB) as conn:
        cur = conn.execute("UPDATE tb_user SET token = NULL WHERE token = ?", (token,))
        if cur.rowcount:
            return jsonify({"message": "Logout berhasil"}), 200
        return jsonify({"error": "Token tidak valid"}), 401
```

### 5. IMPLEMENTASI AUTH PADA API SISWA

- app.py

```py
from flask import Flask
from flasgger import Swagger
from flask_cors import CORS  # ✅ Tambahkan ini
import sqlite3

app = Flask(__name__)
CORS(app)  # ✅ Aktifkan CORS untuk semua route

app.config['SWAGGER'] = {
    'title': 'COBA API',
    'uiversion': 3,
    'securityDefinitions': {
        'ApiKeyAuth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
}
swagger = Swagger(app)

# Inisialisasi DB
def init_db():
    with sqlite3.connect('siswa.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tb_siswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                alamat TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tb_user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                token TEXT
            )
        ''')

init_db()

# Register Blueprint
from routes.belajar import belajar_bp
from routes.siswa import siswa_bp
from routes.auth import auth_bp

app.register_blueprint(auth_bp)
app.register_blueprint(belajar_bp)
app.register_blueprint(siswa_bp)

if __name__ == '__main__':
    app.run(debug=True)
```

- routes/siswa.py

```py
#routes/siswa.py
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from middleware.auth_middleware import token_required
from services import siswa_service

siswa_bp = Blueprint('siswa', __name__)

@siswa_bp.route('/siswa', methods=['POST'])
@token_required
@swag_from('../docs/siswa/create.yml')
def create_siswa():
    try:
        data = request.get_json()
        siswa_service.create_siswa(data['nama'], data['alamat'])
        return jsonify({"message": "Siswa berhasil ditambahkan"}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Gagal menambahkan siswa"}), 500

@siswa_bp.route('/siswa', methods=['GET'])
@token_required
@swag_from('../docs/siswa/read_all.yml')
def read_all_siswa():
    try:
        data = siswa_service.read_all_siswa()
        return jsonify(data), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Gagal mengambil data"}), 500

@siswa_bp.route('/siswa/<int:id>', methods=['GET'])
@token_required
@swag_from('../docs/siswa/read_id.yml')
def read_siswa_by_id(id):
    try:
        data = siswa_service.read_siswa_by_id(id)
        if data:
            return jsonify(data), 200
        return jsonify({"error": "Siswa tidak ditemukan"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Gagal mengambil data"}), 500

@siswa_bp.route('/siswa/<int:id>', methods=['PUT'])
@token_required
@swag_from('../docs/siswa/update.yml')
def update_siswa(id):
    try:
        data = request.get_json()
        updated = siswa_service.update_siswa(id, data['nama'], data['alamat'])
        if updated:
            return jsonify({"message": "Siswa berhasil diperbarui"}), 200
        return jsonify({"error": "Siswa tidak ditemukan"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Gagal memperbarui siswa"}), 500

@siswa_bp.route('/siswa/<int:id>', methods=['DELETE'])
@token_required
@swag_from('../docs/siswa/delete.yml')
def delete_siswa(id):
    try:
        deleted = siswa_service.delete_siswa(id)
        if deleted:
            return jsonify({"message": "Siswa berhasil dihapus"}), 200
        return jsonify({"error": "Siswa tidak ditemukan"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Gagal menghapus siswa"}), 500
```

- docs/siswa.py

```yml
#docs/siswa/delete.yml
---
tags:
  - Siswa
summary: Hapus siswa berdasarkan ID
security:
  - ApiKeyAuth: []
parameters:
  - name: Authorization
    in: header
    required: true
    type: string
    description: Token autentikasi
  - name: id
    in: path
    required: true
    type: integer
    description: ID siswa
responses:
  200:
    description: Siswa berhasil dihapus
    schema:
      type: object
      properties:
        message:
          type: string
  404:
    description: Siswa tidak ditemukan
  500:
    description: Gagal menghapus siswa

#docs/siswa/update.yml
---
tags:
  - Siswa
summary: Perbarui data siswa berdasarkan ID
security:
  - ApiKeyAuth: []
parameters:
  - name: Authorization
    in: header
    required: true
    type: string
    description: Token autentikasi
  - name: id
    in: path
    required: true
    type: integer
    description: ID siswa
  - in: body
    name: body
    required: true
    schema:
      type: object
      required:
        - nama
        - alamat
      properties:
        nama:
          type: string
        alamat:
          type: string
responses:
  200:
    description: Siswa berhasil diperbarui
    schema:
      type: object
      properties:
        message:
          type: string
  404:
    description: Siswa tidak ditemukan
  500:
    description: Gagal memperbarui siswa

#docs/siswa/read_id.yml
---
tags:
  - Siswa
summary: Ambil data siswa berdasarkan ID
security:
  - ApiKeyAuth: []
parameters:
  - name: Authorization
    in: header
    required: true
    type: string
    description: Token autentikasi
  - name: id
    in: path
    required: true
    type: integer
    description: ID siswa
responses:
  200:
    description: Data siswa ditemukan
    schema:
      type: object
      properties:
        id:
          type: integer
        nama:
          type: string
        alamat:
          type: string
  404:
    description: Siswa tidak ditemukan
  500:
    description: Gagal mengambil data

#docs/siswa/create.yml
---
tags:
  - Siswa
summary: Tambah siswa baru
security:
  - ApiKeyAuth: []
parameters:
  - name: Authorization
    in: header
    required: true
    type: string
    description: Token autentikasi
  - in: body
    name: body
    required: true
    schema:
      type: object
      required:
        - nama
        - alamat
      properties:
        nama:
          type: string
        alamat:
          type: string
responses:
  201:
    description: Siswa berhasil ditambahkan
    schema:
      type: object
      properties:
        message:
          type: string
  500:
    description: Gagal menambahkan siswa
    schema:
      type: object
      properties:
        error:
          type: string
```

- test/test_siswa.py

```py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers(client):
    # Register
    client.post('/register', json={"username": "testuser", "password": "testpass"})

    # Login
    response = client.post('/login', json={"username": "testuser", "password": "testpass"})
    token = response.get_json().get('token')

    return {
        "Authorization": token
    }

def test_create_siswa(client, auth_headers):
    response = client.post('/siswa', headers=auth_headers, json={
        "nama": "Test", "alamat": "Bandung"
    })
    assert response.status_code == 201
    assert b"Siswa berhasil ditambahkan" in response.data

def test_get_all_siswa(client, auth_headers):
    response = client.get('/siswa', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_siswa_by_id(client, auth_headers):
    # Buat siswa
    create = client.post('/siswa', headers=auth_headers, json={"nama": "Andi", "alamat": "Jogja"})
    assert create.status_code == 201

    # Ambil siswa terakhir
    siswa = client.get('/siswa', headers=auth_headers).get_json()[-1]
    id_siswa = siswa['id']

    # Test ambil berdasarkan ID
    response = client.get(f'/siswa/{id_siswa}', headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()['nama'] == "Andi"

def test_update_siswa(client, auth_headers):
    # Buat siswa
    client.post('/siswa', headers=auth_headers, json={"nama": "Budi", "alamat": "Solo"})
    siswa = client.get('/siswa', headers=auth_headers).get_json()[-1]
    id_siswa = siswa['id']

    # Update
    response = client.put(f'/siswa/{id_siswa}', headers=auth_headers, json={
        "nama": "Budi Update", "alamat": "Solo Baru"
    })
    assert response.status_code == 200
    assert b"Siswa berhasil diperbarui" in response.data

def test_delete_siswa(client, auth_headers):
    # Buat siswa
    client.post('/siswa', headers=auth_headers, json={"nama": "Citra", "alamat": "Bogor"})
    siswa = client.get('/siswa', headers=auth_headers).get_json()[-1]
    id_siswa = siswa['id']

    # Hapus siswa
    response = client.delete(f'/siswa/{id_siswa}', headers=auth_headers)
    assert response.status_code == 200
    assert b"Siswa berhasil dihapus" in response.data

    # Pastikan sudah dihapus
    check = client.get(f'/siswa/{id_siswa}', headers=auth_headers)
    assert check.status_code == 404
```

### 6. LATIHAN BUAT ULANG SEMUA >> API PRODUCT

API SEDERHANA >> CRUD API PRODUCT >> AUTH

- tb_product (id,kd_product,nm_product,price)

```python
#app.py

# Inisialisasi DB
def init_db():
    with sqlite3.connect('product.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tb_product (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              kd_product TEXT NOT NULL,
              nm_product TEXT NOT NULL,
              price REAL NOT NULL
            )
        ''')

init_db()

```

| No  | Method | Endpoint        | Request Body (JSON)                                                               | Response (JSON)                                                                              |
| --- | ------ | --------------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 1   | POST   | `/product`      | `{ "kd_product": "KMPT01", "nm_product": "Komputer Satu", "price": 1000 }`        | `{ "message": "Product berhasil ditambahkan" }`                                              |
| 2   | GET    | `/product`      | (tidak ada)                                                                       | `[ { "id": 1, "kd_product": "KMPT01", "nm_product": "Komputer Satu", "price": 1000 }, ... ]` |
| 3   | GET    | `/product/<id>` | (tidak ada)                                                                       | `{ "id": 1, "kd_product": "KMPT01", "nm_product": "Komputer Satu", "price": 1000 }`          |
| 4   | PUT    | `/product/<id>` | `{ "kd_product": "KMPT01 Updated", "nm_product": "Komputer Dua", "price": 2000 }` | `{ "message": "Product berhasil diperbarui" }`                                               |
| 5   | DELETE | `/product/<id>` | (tidak ada)                                                                       | `{ "message": "Product berhasil dihapus" }`                                                  |

```py

project-folder/
├── app.py
├── routes/
│   ├── product.py         ← Semua endpoint product
│   └── belajar.py       ← Endpoint halo dan nama
├── docs/                ← Swagger YAML
│   ├── product_create.yml
│   ├── product_delete.yml
│   ├── product_update.yml
│   ├── product_read_all.yml
│   ├── product_read_id.yml
│   ├── nama.yml
│   ├── halo_post.yml
│   └── halo.yml
├── test/
│   ├── __init__.py
│   ├── test_product.py
│   └── test_belajar.py
└── product.db             ← File SQLite (otomatis dibuat)
```

### 7. LATIHAN BUAT ULANG SEMUA >> API BOOK

API SEDERHANA >> CRUD API PRODUCT >> AUTH

- tb_book (id,kd_book,nm_book,price)

```python
#app.py

# Inisialisasi DB
def init_db():
    with sqlite3.connect('book.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tb_book (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              kd_book TEXT NOT NULL,
              nm_book TEXT NOT NULL,
              price REAL NOT NULL
            )
        ''')

init_db()

```

| No  | Method | Endpoint     | Request Body (JSON)                                                     | Response (JSON)                                                                    |
| --- | ------ | ------------ | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 1   | POST   | `/book`      | `{ "kd_book": "BOOK01", "nm_book": "Buku Satu", "price": 1000 }`        | `{ "message": "Buku berhasil ditambahkan" }`                                       |
| 2   | GET    | `/book`      | (tidak ada)                                                             | `[ { "id": 1, "kd_book": "BOOK01", "nm_book": "Buku Satu", "price": 1000 }, ... ]` |
| 3   | GET    | `/book/<id>` | (tidak ada)                                                             | `{ "id": 1, "kd_book": "BOOK01", "nm_book": "Buku Satu", "price": 1000 }`          |
| 4   | PUT    | `/book/<id>` | `{ "kd_book": "BOOK01 Updated", "nm_book": "Buku Dua", "price": 2000 }` | `{ "message": "Buku berhasil diperbarui" }`                                        |
| 5   | DELETE | `/book/<id>` | (tidak ada)                                                             | `{ "message": "Buku berhasil dihapus" }`                                           |

```py

project-folder/
├── app.py
├── routes/
│   ├── book.py         ← Semua endpoint book
│   └── belajar.py       ← Endpoint halo dan nama
├── docs/                ← Swagger YAML
│   ├── book_create.yml
│   ├── book_delete.yml
│   ├── book_update.yml
│   ├── book_read_all.yml
│   ├── book_read_id.yml
│   ├── nama.yml
│   ├── halo_post.yml
│   └── halo.yml
├── test/
│   ├── __init__.py
│   ├── test_book.py
│   └── test_belajar.py
└── book.db             ← File SQLite (otomatis dibuat)
```

### 8. FRONT END REACTJS
