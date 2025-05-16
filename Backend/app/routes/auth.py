from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"msg": "Missing email or password"}), 400
    
    if User.find_by_email(data['email']):
        return jsonify({"msg": "Email already exists"}), 409
    
    User.create(data['email'], data['password'])
    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_email(data.get('email'))
    
    if not user or not check_password_hash(user['password'], data.get('password', '')):
        return jsonify({"msg": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=str(user['_id']))
    return jsonify(access_token=access_token), 200