from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, db
from flask_login import login_user, logout_user, login_required
import uuid
import re

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return jsonify({"error": "Invalid email format!"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters!"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists!"}), 400

    user_id = str(uuid.uuid4())
    hashed_password = generate_password_hash(password)
    new_user = User(id=user_id, email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful!"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid credentials!"}), 401