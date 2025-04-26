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
