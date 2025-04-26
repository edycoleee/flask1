# # app.py >> pertama
# from flask import Flask, jsonify

# app = Flask(__name__)

# @app.route('/halo', methods=['GET'])
# def halo():
#     return jsonify({"message": "Belajar Flask"})

# if __name__ == '__main__':
#     app.run(debug=True)

# # # app.py >> kedua dg flasgger
# from flask import Flask, jsonify
# from flasgger import Swagger
# from flask_cors import CORS
# app = Flask(__name__)
# app.config['SWAGGER'] = {
#     'title': 'COBA API',
#     'uiversion': 3
# }
# Swagger(app)  # Inisialisasi Flasgger

# @app.route('/halo', methods=['GET'])
# def halo():
#     """
#     Endpoint untuk mendapatkan pesan Belajar Flask
#     ---
#     tags:
#       - Halo
#     responses:
#       200:
#         description: Respon sukses
#         content:
#           application/json:
#             schema:
#               type: object
#               properties:
#                 message:
#                   type: string
#                   example: Belajar Flask
#     """
#     return jsonify({"message": "Belajar Flask"})

# if __name__ == '__main__':
#     app.run(debug=True)

# # # app.py >> ketiga dg cleancode
from flask import Flask
from flasgger import Swagger
from flask_cors import CORS  # ✅ Tambahkan ini
import sqlite3

app = Flask(__name__)
CORS(app)  # ✅ Aktifkan CORS untuk semua route
# app.config['SWAGGER'] = {
#     'title': 'COBA API',
#     'uiversion': 3
# }
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