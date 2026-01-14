from flask import Blueprint, request, jsonify
from models import MockTest, Question
from extensions import db

tests_bp = Blueprint('tests', __name__)

@tests_bp.route('', methods=['GET'])
def list_tests():
    # Basic search functionality
    query = request.args.get('q', '')
    if query:
        tests = MockTest.query.filter(MockTest.title.ilike(f'%{query}%')).all()
    else:
        tests = MockTest.query.all()
        
    return jsonify([{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "category": t.category,
        "question_count": len(t.questions),
        "created_at": t.created_at.isoformat()
    } for t in tests])

@tests_bp.route('/<int:test_id>', methods=['GET'])
def get_test(test_id):
    test = MockTest.query.get_or_404(test_id)
    return jsonify({
        "id": test.id,
        "title": test.title,
        "description": test.description,
        "category": test.category,
        "questions": [{
            "id": q.id,
            "text": q.question_text,
            "image_url": q.image_url,
            "type": q.question_type,
            "options": q.options,
            # We don't send correct_answer here to prevent cheating 
            # OR we can have a separate 'check' endpoint. 
            # For simplicity in practice mode, we might need it, 
            # but let's send it for now since it's a practice app.
            "correct_answer": q.correct_answer
        } for q in test.questions]
    })
