from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User
from extensions import db
from utils import verify_recaptcha

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    recaptcha_token = data.get('recaptcha_token')

    if not all([username, email, password]):
        return jsonify({"msg": "Missing required fields"}), 400

    if not verify_recaptcha(recaptcha_token):
        return jsonify({"msg": "Invalid reCAPTCHA"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    recaptcha_token = data.get('recaptcha_token')

    if not all([email, password]):
        return jsonify({"msg": "Missing field"}), 400

    if not verify_recaptcha(recaptcha_token):
        return jsonify({"msg": "Invalid reCAPTCHA"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(
            access_token=access_token, 
            user={
                "id": user.id, 
                "username": user.username, 
                "email": user.email,
                "is_admin": user.is_admin,
                "settings": user.settings or {"primaryColor": "#6366f1", "fontSize": 16, "fontFamily": "sans"}
            }
        ), 200

    return jsonify({"msg": "Bad email or password"}), 401

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(
        id=user.id, 
        username=user.username, 
        email=user.email, 
        is_admin=user.is_admin,
        settings=user.settings or {"primaryColor": "#6366f1", "fontSize": 16, "fontFamily": "sans"}
    )

@auth_bp.route('/me/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    data = request.get_json()
    new_settings = data.get('settings')
    
    if new_settings is None:
        return jsonify({"msg": "No settings provided"}), 400
        
    # Merge settings if it's already a dict, or replace
    current_settings = user.settings or {"primaryColor": "#6366f1", "fontSize": 16, "fontFamily": "sans"}
    current_settings.update(new_settings)
    
    user.settings = current_settings
    db.session.commit()
    
    return jsonify({"msg": "Settings updated", "settings": user.settings}), 200
