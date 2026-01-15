from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, ChatSession, ChatMessage, User
import google.generativeai as genai
import os

chat_bp = Blueprint('chat', __name__)

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-3-flash-preview')

@chat_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    current_user_id = int(get_jwt_identity())
    sessions = ChatSession.query.filter_by(user_id=current_user_id).order_by(ChatSession.created_at.desc()).all()
    return jsonify([{
        'id': s.id,
        'title': s.title,
        'created_at': s.created_at.isoformat()
    } for s in sessions]), 200

@chat_bp.route('/session', methods=['POST'])
@jwt_required()
def create_session():
    current_user_id = int(get_jwt_identity())
    new_session = ChatSession(user_id=current_user_id)
    db.session.add(new_session)
    db.session.commit()
    return jsonify({
        'id': new_session.id,
        'title': new_session.title,
        'created_at': new_session.created_at.isoformat(),
        'messages': []
    }), 201

@chat_bp.route('/session/<int:session_id>', methods=['GET'])
@jwt_required()
def get_session_messages(session_id):
    current_user_id = int(get_jwt_identity())
    session = ChatSession.query.get_or_404(session_id)
    
    if session.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at).all()
    return jsonify([{
        'role': m.role,
        'content': m.content,
        'created_at': m.created_at.isoformat()
    } for m in messages]), 200

@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    session_id = data.get('session_id')
    content = data.get('content')
    
    if not session_id or not content:
        return jsonify({'error': 'Missing session_id or content'}), 400
        
    session = ChatSession.query.get_or_404(session_id)
    if session.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    # Save user message
    user_msg = ChatMessage(session_id=session_id, role='user', content=content)
    db.session.add(user_msg)
    
    try:
        # Get chat history for context (limit to last 10 messages to avoid token limits)
        history_msgs = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at).all()
        
        # Build chat history in Gemini format
        history = []
        for m in history_msgs[-10:]:  # Only last 10 messages
            history.append({
                'role': m.role,
                'parts': [m.content]
            })
        
        # Create chat with Vietnamese instruction
        chat = model.start_chat(history=history)
        
        # Send message with Vietnamese instruction
        prompt = f"Trả lời câu hỏi sau bằng tiếng việt {content}"
        response = chat.send_message(prompt)
        ai_response_text = response.text
        
        # Save model message
        model_msg = ChatMessage(session_id=session_id, role='model', content=ai_response_text)
        db.session.add(model_msg)
        
        # Update session title if it's the first message and title is default
        if len(history_msgs) <= 1 and session.title == "New Chat":
            # Generate a short title based on the first message
            session.title = content[:30] + "..." if len(content) > 30 else content
            
        db.session.commit()
        
        return jsonify({
            'role': 'model',
            'content': ai_response_text
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/session/<int:session_id>', methods=['DELETE'])
@jwt_required()
def delete_session(session_id):
    current_user_id = int(get_jwt_identity())
    session = ChatSession.query.get_or_404(session_id)
    
    if session.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        db.session.delete(session)
        db.session.commit()
        return jsonify({'msg': 'Session deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

