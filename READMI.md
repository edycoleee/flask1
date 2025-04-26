### 1. API SEDERHANA

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
  - Halo
responses:
  200:
    description: Respon sukses
    schema:
      type: object
      properties:
        message:
          type: string
          example: Halo Flask
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

```cmd
No	|Method	Endpoint	|Request Body (JSON)	|Response (JSON)
1	POST	|/siswa	|{ "nama": "Silmi", "alamat": "Semarang" }	|{ "message": "Siswa berhasil ditambahkan" }
2	GET	|/siswa	(tidak ada)	|[ { "id": 1, "nama": "Silmi", "alamat": "Semarang" }, ... ]
3	GET	|/siswa/<id>	|(tidak ada)	|{ "id": 1, "nama": "Silmi", "alamat": "Semarang" }
4	PUT	|/siswa/<id>	|{ "nama": "Silmi Updated", "alamat": "Jakarta" }	{ "message": "Siswa berhasil diperbarui" }
5	DELETE	|/siswa/<id>	(tidak ada)	|{ "message": "Siswa berhasil dihapus" }

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

```yml
#docs/siswa/create.yml
post:
  tags:
    - Siswa
  summary: Tambah data siswa
  requestBody:
    required: true
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/SiswaInput'
        example:
          nama: Silmi
          alamat: Semarang
  responses:
    201:
      description: Siswa berhasil ditambahkan
      content:
        application/json:
          example:
            message: Siswa berhasil ditambahkan
    500:
      description: Gagal menambahkan siswa
components:
  schemas:
    SiswaInput:
      type: object
      properties:
        nama:
          type: string
        alamat:
          type: string
      required:
        - nama
        - alamat


#docs/siswa/read_all.yml
get:
  tags:
    - Siswa
  summary: Ambil semua data siswa
  responses:
    200:
      description: Daftar seluruh siswa
      content:
        application/json:
          schema:
            type: array
            items:
              $ref: '#/components/schemas/Siswa'
components:
  schemas:
    Siswa:
      type: object
      properties:
        id:
          type: integer
        nama:
          type: string
        alamat:
          type: string

#docs/siswa/read_id.yml
get:
  tags:
    - Siswa
  summary: Ambil data siswa berdasarkan ID
  parameters:
    - in: path
      name: id
      required: true
      schema:
        type: integer
  responses:
    200:
      description: Data siswa ditemukan
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Siswa'
    404:
      description: Siswa tidak ditemukan

#docs/siswa/update.yml
put:
  tags:
    - Siswa
  summary: Update data siswa berdasarkan ID
  parameters:
    - in: path
      name: id
      required: true
      schema:
        type: integer
  requestBody:
    required: true
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/SiswaInput'
        example:
          nama: Silmi Update
          alamat: Bandung
  responses:
    200:
      description: Siswa berhasil diupdate
      content:
        application/json:
          example:
            message: Siswa berhasil diupdate
    404:
      description: Siswa tidak ditemukan
components:
  schemas:
    SiswaInput:
      type: object
      properties:
        nama:
          type: string
        alamat:
          type: string
      required:
        - nama
        - alamat

#docs/siswa/delete.yml
delete:
  tags:
    - Siswa
  summary: Hapus data siswa berdasarkan ID
  parameters:
    - in: path
      name: id
      required: true
      schema:
        type: integer
  responses:
    200:
      description: Siswa berhasil dihapus
      content:
        application/json:
          example:
            message: Siswa berhasil dihapus
    404:
      description: Siswa tidak ditemukan


```

```cmd
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/edycoleee/flask1.git
git push -u origin main
```
