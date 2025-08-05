from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """ Create a user with fresh new data """
    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400
    user = User(
        username=data["username"],
        password_hash=generate_password_hash(data["password"])
    )  
    db.session.add(user) 
    db.session.commit()  
    return jsonify({"message": "User registered successfully"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    password = data['password']
    if user and check_password_hash(user.password_hash, password):
        return jsonify({'message': "Login is successful", "user_id": user.id})  # user account is valid so we log them in
    return jsonify({"error": "incorrect login data"}), 401 #unauthorized user