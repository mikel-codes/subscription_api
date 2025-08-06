from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import User
from sqlalchemy import text

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """ Create a user with fresh new data """
    data = request.json or {}
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    exists = db.session.execute(
        text("SELECT 1 FROM users WHERE username = :username LIMIT 1"),
        {"username": username}
    ).fetchone()


    if exists:
        return jsonify({"error": "Username already exists"}), 400
    

    db.session.execute(
        text("""
            INSERT INTO users (username, password_hash, created_at)
            VALUES (:username, :password_hash, CURRENT_TIMESTAMP)
        """),
        {"username": username, "password_hash": generate_password_hash(password)}
    )
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = db.session.execute(
        text("SELECT *  FROM users WHERE username = :username LIMIT 1"),
        {"username": data['username']}
    ).fetchone()
    password = data['password']

    if user and check_password_hash(user.password_hash, password):
        return jsonify({'message': "Login is successful", "user_id": user.id})  # user account is valid so we log them in
    return jsonify({"error": "incorrect login data"}), 401 #unauthorized user