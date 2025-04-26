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

@belajar_bp.route('/halo', methods=['POST'])
@swag_from('../docs/halo_post.yml')
def halo_post():
    from flask import request
    data = request.get_json()
    return jsonify({
        "nama": data.get("nama"),
        "alamat": data.get("alamat")
    })