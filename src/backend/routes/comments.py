from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Comment, User, DirectMessage, Conversation, ConversationParticipant
from extensions import db

comments_bp = Blueprint('comments', __name__)

def send_violation_notice(admin_id, user_id, content_type, content_preview):
    """Sends a direct message to the user about the violation."""
    if admin_id == user_id: return
    
    try:
        conv = Conversation.query.join(Conversation.participants).filter(
            ConversationParticipant.user_id.in_([admin_id, user_id])
        ).group_by(Conversation.id).having(db.func.count(ConversationParticipant.user_id) == 2).first()
        
        if not conv:
            conv = Conversation()
            db.session.add(conv)
            db.session.flush()
            p1 = ConversationParticipant(conversation_id=conv.id, user_id=admin_id)
            p2 = ConversationParticipant(conversation_id=conv.id, user_id=user_id)
            db.session.add_all([p1, p2])
            
        msg_content = f"**Hệ thống:** Nội dung của bạn ({content_type}) đã bị xóa do vi phạm quy tắc cộng đồng.\n\n> {content_preview[:50]}...\n\nVui lòng xem lại [quy tắc](/rules)."
        
        msg = DirectMessage(conversation_id=conv.id, sender_id=admin_id, content=msg_content)
        db.session.add(msg)
    except Exception as e:
        print(f"Failed to send violation notice: {e}")


@comments_bp.route('/<path:slug>', methods=['GET'])
def get_comments(slug):
    # Only get top-level comments (where parent_id is None)
    top_comments = Comment.query.filter_by(lesson_slug=slug, parent_id=None).order_by(Comment.created_at.desc()).all()
    
    def serialize_comment(c):
        return {
            "id": c.id,
            "content": c.content,
            "user_id": c.user.id,
            "username": c.user.username,
            "avatar_seed": c.user.avatar_seed or c.user.username,
            "avatar_url": c.user.avatar_url,
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
            "user_id": comment.user.id,
            "username": comment.user.username,
            "avatar_seed": comment.user.avatar_seed or comment.user.username,
            "avatar_url": comment.user.avatar_url,
            "parent_id": comment.parent_id,
            "created_at": comment.created_at.isoformat(),
            "replies": []
        }
    }), 201

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        comment = Comment.query.get_or_404(comment_id)
        
        if not user.is_admin and comment.user_id != user_id:
            return jsonify({"msg": "Unauthorized"}), 403
            
        is_admin_action = user.is_admin and comment.user_id != user_id
        
        if is_admin_action:
            send_violation_notice(user_id, comment.user_id, "Bình luận bài học", comment.content)
            
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"msg": "Comment deleted"}), 200
    except Exception as e:
        return jsonify({"msg": "Failed to delete", "error": str(e)}), 500
