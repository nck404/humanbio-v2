from flask import Blueprint, request, jsonify
from extensions import db
from models import ForumPost, ForumComment, User, ForumPostReaction, ForumCommentReaction
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/posts', methods=['GET'])
def get_posts():
    try:
        topic = request.args.get('topic')
        query = ForumPost.query
        if topic:
            query = query.filter_by(topic=topic)
            
        posts = query.order_by(ForumPost.created_at.desc()).all()
        return jsonify([{
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'topic': post.topic,
            'created_at': post.created_at.isoformat(),
            'author': {
                'username': post.author.username,
                'avatar_seed': post.author.avatar_seed
            },
            'comment_count': len(post.comments),
            'reaction_count': len(post.reactions)
        } for post in posts]), 200
    except Exception as e:
        return jsonify({"msg": "Failed to fetch posts", "error": str(e)}), 500

@forum_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    try:
        data = request.get_json()
        current_user_id = int(get_jwt_identity())
        
        if not data.get('title') or not data.get('content'):
            return jsonify({"msg": "Title and content are required"}), 400

        new_post = ForumPost(
            title=data['title'],
            content=data['content'],
            topic=data.get('topic', 'General'),
            user_id=current_user_id
        )
        
        db.session.add(new_post)
        db.session.commit()
        
        return jsonify({"msg": "Post created successfully", "id": new_post.id}), 201
    except Exception as e:
        return jsonify({"msg": "Failed to create post", "error": str(e)}), 500

@forum_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post_details(post_id):
    try:
        post = ForumPost.query.get_or_404(post_id)
        current_user_id = None
        try:
            verify_jwt_in_request(optional=True)
            current_user_id = int(get_jwt_identity())
        except:
            pass
        
        # Recursive function to serialize comments
        def serialize_comment(comment):
            reaction_count = len(comment.reactions)
            user_reaction = None
            if current_user_id:
                # Inefficient for large datasets but ok for MVP
                reaction = next((r for r in comment.reactions if r.user_id == current_user_id), None)
                if reaction: user_reaction = reaction.type
                
            return {
                'id': comment.id,
                'content': comment.content,
                'created_at': comment.created_at.isoformat(),
                'author': {
                    'username': comment.author.username,
                    'avatar_seed': comment.author.avatar_seed
                },
                'reaction_count': reaction_count,
                'user_reaction': user_reaction,
                'replies': [serialize_comment(reply) for reply in comment.replies]
            }

        # Fetch top-level comments
        comments = ForumComment.query.filter_by(post_id=post.id, parent_id=None).order_by(ForumComment.created_at.desc()).all()
        
        post_reaction_count = len(post.reactions)
        post_user_reaction = None
        if current_user_id:
             reaction = next((r for r in post.reactions if r.user_id == current_user_id), None)
             if reaction: post_user_reaction = reaction.type
        
        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'topic': post.topic,
            'created_at': post.created_at.isoformat(),
            'author': {
                'username': post.author.username,
                'avatar_seed': post.author.avatar_seed
            },
            'reaction_count': post_reaction_count,
            'user_reaction': post_user_reaction,
            'comments': [serialize_comment(c) for c in comments]
        }), 200
    except Exception as e:
        return jsonify({"msg": "Failed to fetch post details", "error": str(e)}), 500

@forum_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    try:
        data = request.get_json()
        current_user_id = int(get_jwt_identity())
        
        if not data.get('content'):
            return jsonify({"msg": "Content is required"}), 400

        # Verify post exists
        post = ForumPost.query.get_or_404(post_id)
        
        new_comment = ForumComment(
            content=data['content'],
            post_id=post.id,
            user_id=current_user_id,
            parent_id=data.get('parent_id') # Optional for nested comments
        )
        
        db.session.add(new_comment)
        db.session.commit()
        
        return jsonify({"msg": "Comment added successfully", "id": new_comment.id}), 201
    except Exception as e:
        return jsonify({"msg": "Failed to add comment", "error": str(e)}), 500

@forum_bp.route('/posts/<int:post_id>/react', methods=['POST'])
@jwt_required()
def react_to_post(post_id):
    try:
        data = request.get_json()
        reaction_type = data.get('type', 'like')
        current_user_id = int(get_jwt_identity())
        
        existing = ForumPostReaction.query.filter_by(user_id=current_user_id, post_id=post_id).first()
        
        if existing:
            if existing.type == reaction_type:
                # Toggle off if same type
                db.session.delete(existing)
                msg = "Reaction removed"
            else:
                # Change type
                existing.type = reaction_type
                msg = "Reaction updated"
        else:
            new_reaction = ForumPostReaction(user_id=current_user_id, post_id=post_id, type=reaction_type)
            db.session.add(new_reaction)
            msg = "Reaction added"
            
        db.session.commit()
        return jsonify({"msg": msg}), 200
    except Exception as e:
        return jsonify({"msg": "Failed to react", "error": str(e)}), 500

@forum_bp.route('/comments/<int:comment_id>/react', methods=['POST'])
@jwt_required()
def react_to_comment(comment_id):
    try:
        data = request.get_json()
        reaction_type = data.get('type', 'like')
        current_user_id = int(get_jwt_identity())
        
        existing = ForumCommentReaction.query.filter_by(user_id=current_user_id, comment_id=comment_id).first()
        
        if existing:
            if existing.type == reaction_type:
                # Toggle off
                db.session.delete(existing)
                msg = "Reaction removed"
            else:
                existing.type = reaction_type
                msg = "Reaction updated"
        else:
            new_reaction = ForumCommentReaction(user_id=current_user_id, comment_id=comment_id, type=reaction_type)
            db.session.add(new_reaction)
            msg = "Reaction added"
            
        db.session.commit()
        return jsonify({"msg": msg}), 200
    except Exception as e:
        return jsonify({"msg": "Failed to react", "error": str(e)}), 500
