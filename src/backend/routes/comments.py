from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Comment, User
from extensions import db

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/<path:slug>', methods=['GET'])
def get_comments(slug):
    # Only get top-level comments (where parent_id is None)
    top_comments = Comment.query.filter_by(lesson_slug=slug, parent_id=None).order_by(Comment.created_at.desc()).all()
    
    def serialize_comment(c):
        return {
            "id": c.id,
            "content": c.content,
            "username": c.user.username,
            "avatar_seed": c.user.avatar_seed or c.user.username,
            "created_at": c.created_at.isoformat(),
            "replies": [serialize_comment(reply) for reply in c.replies.order_by(Comment.created_at.asc()).all()]
        }
        
    return jsonify([serialize_comment(c) for c in top_comments])

@comments_bp.route('', methods=['POST'])
@jwt_required()
def post_comment():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    content = data.get('content')
    slug = data.get('slug')
    parent_id = data.get('parent_id') # New field for replies

    if not content or not slug:
        return jsonify({"msg": "Content and slug are required"}), 400

    comment = Comment(content=content, lesson_slug=slug, user_id=user_id, parent_id=parent_id)
    db.session.add(comment)
    db.session.commit()

    return jsonify({
        "msg": "Comment posted",
        "comment": {
            "id": comment.id,
            "content": comment.content,
            "username": comment.user.username,
            "avatar_seed": comment.user.avatar_seed or comment.user.username,
            "parent_id": comment.parent_id,
            "created_at": comment.created_at.isoformat(),
            "replies": []
        }
    }), 201
