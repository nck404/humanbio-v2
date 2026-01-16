from flask import Blueprint, jsonify
from models import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_public_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    return jsonify({
        "id": user.id,
        "username": user.username,
        "avatar_url": user.avatar_url,
        "avatar_seed": user.avatar_seed or user.username,
        "bio": user.bio,
        "social_links": user.social_links or {},
        "is_admin": user.is_admin
    })
