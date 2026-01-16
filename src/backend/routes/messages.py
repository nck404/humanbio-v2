from flask import Blueprint, request, jsonify, Response, stream_with_context
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Conversation, ConversationParticipant, DirectMessage
import json
import time
from queue import Queue

messages_bp = Blueprint('messages', __name__)

# Real-time message distribution
user_queues = {}

def get_user_queue(user_id):
    if user_id not in user_queues:
        user_queues[user_id] = []
    return user_queues[user_id]

def notify_user(user_id, data):
    if user_id in user_queues:
        for q in user_queues[user_id]:
            q.put(data)

@messages_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    current_user_id = int(get_jwt_identity())
    
    # Find all conversations the user is part of
    participants = ConversationParticipant.query.filter_by(user_id=current_user_id).all()
    conv_ids = [p.conversation_id for p in participants]
    
    conversations = Conversation.query.filter(Conversation.id.in_(conv_ids)).order_by(Conversation.updated_at.desc()).all()
    
    result = []
    for conv in conversations:
        # Find the other participant
        other_participant = ConversationParticipant.query.filter(
            ConversationParticipant.conversation_id == conv.id,
            ConversationParticipant.user_id != current_user_id
        ).first()
        
        if not other_participant:
            continue
            
        other_user = other_participant.user
        last_message = DirectMessage.query.filter_by(conversation_id=conv.id).order_by(DirectMessage.created_at.desc()).first()
        
        result.append({
            'id': conv.id,
            'other_user': {
                'id': other_user.id,
                'username': other_user.username,
                'avatar_url': other_user.avatar_url,
                'avatar_seed': other_user.avatar_seed
            },
            'last_message': {
                'content': last_message.content if last_message else None,
                'created_at': last_message.created_at.isoformat() if last_message else conv.created_at.isoformat(),
                'sender_id': last_message.sender_id if last_message else None
            },
            'updated_at': conv.updated_at.isoformat()
        })
        
    return jsonify(result), 200

@messages_bp.route('/conversation', methods=['POST'])
@jwt_required()
def start_conversation():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    other_user_id = data.get('user_id')
    
    if not other_user_id:
        return jsonify({'error': 'User ID required'}), 400
        
    if current_user_id == int(other_user_id):
        return jsonify({'error': 'Cannot chat with yourself'}), 400

    # Check if user exists
    other_user = User.query.get(other_user_id)
    if not other_user:
        return jsonify({'error': 'User not found'}), 404

    # Check if conversation already exists between these two
    conversations = db.session.query(Conversation.id).join(ConversationParticipant).filter(
        ConversationParticipant.user_id.in_([current_user_id, other_user_id])
    ).group_by(Conversation.id).having(db.func.count(Conversation.id) == 2).all()
    
    if conversations:
        conv_id = conversations[0][0]
    else:
        # Create new conversation
        new_conv = Conversation()
        db.session.add(new_conv)
        db.session.flush()
        
        p1 = ConversationParticipant(conversation_id=new_conv.id, user_id=current_user_id)
        p2 = ConversationParticipant(conversation_id=new_conv.id, user_id=other_user_id)
        db.session.add_all([p1, p2])
        db.session.commit()
        conv_id = new_conv.id
        
    return jsonify({'id': conv_id}), 201

@messages_bp.route('/conversation/<int:conv_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(conv_id):
    current_user_id = int(get_jwt_identity())
    
    # Verify participation
    participant = ConversationParticipant.query.filter_by(
        conversation_id=conv_id, user_id=current_user_id
    ).first()
    
    if not participant:
        return jsonify({'error': 'Unauthorized'}), 403
        
    messages = DirectMessage.query.filter_by(conversation_id=conv_id).order_by(DirectMessage.created_at.asc()).all()
    
    return jsonify([{
        'id': m.id,
        'sender_id': m.sender_id,
        'content': m.content,
        'created_at': m.created_at.isoformat(),
        'is_read': m.is_read
    } for m in messages]), 200

@messages_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    conv_id = data.get('conversation_id')
    content = data.get('content')
    
    if not conv_id or not content:
        return jsonify({'error': 'Missing fields'}), 400
        
    # Verify participant
    participant = ConversationParticipant.query.filter_by(conversation_id=conv_id, user_id=current_user_id).first()
    if not participant:
        return jsonify({'error': 'Unauthorized'}), 403
        
    # Save message
    new_msg = DirectMessage(conversation_id=conv_id, sender_id=current_user_id, content=content)
    db.session.add(new_msg)
    
    # Update conversation timestamp
    conv = Conversation.query.get(conv_id)
    conv.updated_at = db.func.current_timestamp()
    
    db.session.commit()
    
    # Notify other participants
    other_participants = ConversationParticipant.query.filter(
        ConversationParticipant.conversation_id == conv_id,
        ConversationParticipant.user_id != current_user_id
    ).all()
    
    msg_data = {
        'type': 'new_message',
        'conversation_id': conv_id,
        'message': {
            'id': new_msg.id,
            'sender_id': new_msg.sender_id,
            'content': new_msg.content,
            'created_at': new_msg.created_at.isoformat()
        }
    }
    
    for p in other_participants:
        notify_user(p.user_id, msg_data)
        
    return jsonify(msg_data['message']), 201

@messages_bp.route('/stream')
def stream_messages():
    # Manual JWT check because EventSource doesn't support headers easily
    token = request.args.get('token')
    from flask_jwt_extended import decode_token
    try:
        if not token:
            # Fallback to header if exists
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Unauthorized'}), 401
            
        decoded = decode_token(token)
        current_user_id = int(decoded['sub'])
    except Exception as e:
        return jsonify({'error': 'Invalid token'}), 401
    
    def event_stream():
        q = Queue()
        if current_user_id not in user_queues:
            user_queues[current_user_id] = []
        user_queues[current_user_id].append(q)
        
        try:
            # Send initial keepalive
            yield f"data: {json.dumps({'type': 'connected'})}\n\n"
            
            while True:
                data = q.get()
                yield f"data: {json.dumps(data)}\n\n"
        except GeneratorExit:
            if current_user_id in user_queues and q in user_queues[current_user_id]:
                user_queues[current_user_id].remove(q)
                
    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")
