"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

def add_jackson(first_name, age, lucky_numbers):
    member = {
        "first_name": first_name,
        "age": age,
        "lucky_numbers": lucky_numbers
    }
    jackson_family.add_member(member)

add_jackson(first_name="John", age=33, lucky_numbers=[7, 13, 22])
add_jackson(first_name="Jane", age=35, lucky_numbers=[10, 14, 3])
add_jackson(first_name="Jimmy", age=5, lucky_numbers=[1])

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# SACAR TODOS LOS USERS
@app.route('/members', methods=['GET'])
def handle_get_members():
    members = jackson_family.get_all_members()

    if members:
        return jsonify(members), 200
    else:
        return jsonify({"error": "No members found"}), 404

# SACAR UN USER  
@app.route('/member/<int:id>', methods=['GET'])
def handle_get_member(id):
    member = jackson_family.get_member(id)

    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404

# CREAR NUEVO USER
@app.route('/member', methods=['POST'])
def handle_add_member():
    body = request.get_json()

    if not body:
        return jsonify({"error": "Request body is missing"}), 400

    if "first_name" not in body or "age" not in body or "lucky_numbers" not in body:
        return jsonify({"error": "Missing required fields"}), 400

    new_member = {
        "id": body.get("id", jackson_family._generateId()),
        "first_name": body["first_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"]
    }

    jackson_family.add_member(new_member)
    return jsonify({"message": "Member added successfully"}), 200

# ELIMINAR UN USER
@app.route('/member/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    result = jackson_family.delete_member(id)

    if result:
        return jsonify({"done": "Successfull delete"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)