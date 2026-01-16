from flask import Blueprint, request, jsonify
from models import User, MockTest, Question
from extensions import db
from utils import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/tests', methods=['POST'])
@admin_required
def create_test():
    data = request.get_json()
    test = MockTest(
        title=data.get('title'), 
        description=data.get('description'),
        category=data.get('category', 'General')
    )
    db.session.add(test)
    db.session.flush()

    for q in data.get('questions', []):
        question = Question(
            test_id=test.id,
            question_text=q.get('text'),
            image_url=q.get('image_data'),
            question_type=q.get('type'),
            options=q.get('options'),
            correct_answer=q.get('correct_answer')
        )
        db.session.add(question)
    
    db.session.commit()
    return jsonify({"msg": "Test created successfully", "id": test.id}), 201

@admin_bp.route('/tests', methods=['GET'])
@admin_required
def list_tests():
    # Optimize query to avoid loading all questions (and potentially large images) just to count them
    # Use grouped query
    results = db.session.query(MockTest, db.func.count(Question.id).label('count')) \
        .outerjoin(Question) \
        .group_by(MockTest.id) \
        .all()
        
    return jsonify([{
        "id": t.id, 
        "title": t.title, 
        "description": t.description,
        "category": t.category,
        "question_count": count
    } for t, count in results])

@admin_bp.route('/tests/<int:test_id>', methods=['GET'])
@admin_required
def get_admin_test(test_id):
    test = MockTest.query.get_or_404(test_id)
    return jsonify({
        "id": test.id,
        "title": test.title,
        "description": test.description,
        "category": test.category,
        "questions": [{
            "id": q.id,
            "text": q.question_text,
            "image_data": q.image_url,
            "type": q.question_type,
            "options": q.options,
            "correct_answer": q.correct_answer
        } for q in test.questions]
    })

@admin_bp.route('/tests/<int:test_id>', methods=['PUT'])
@admin_required
def update_test(test_id):
    test = MockTest.query.get_or_404(test_id)
    data = request.get_json()
    
    test.title = data.get('title', test.title)
    test.description = data.get('description', test.description)
    test.category = data.get('category', test.category)
    
    # Simple replacement strategy for questions
    for q in test.questions:
        db.session.delete(q)
    
    for q in data.get('questions', []):
        question = Question(
            test_id=test.id,
            question_text=q.get('text'),
            image_url=q.get('image_data'),
            question_type=q.get('type'),
            options=q.get('options'),
            correct_answer=q.get('correct_answer')
        )
        db.session.add(question)

    db.session.commit()
    return jsonify({"msg": "Test updated successfully"})

@admin_bp.route('/tests/<int:test_id>', methods=['DELETE'])
@admin_required
def delete_test(test_id):
    test = MockTest.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    return jsonify({"msg": "Test deleted"})

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    print("DEBUG: list_users hit")
    users = User.query.all()
    print(f"DEBUG: Found {len(users)} users")
    return jsonify([{
        "id": u.id, 
        "username": u.username, 
        "email": u.email, 
        "is_admin": u.is_admin
    } for u in users])

@admin_bp.route('/users/<int:user_id>/promote', methods=['POST'])
@admin_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    return jsonify({"msg": f"User {user.username} promoted to admin"})
