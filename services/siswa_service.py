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