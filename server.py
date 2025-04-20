# server.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
import logging
import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Add a secret key for security
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS directly in SocketIO

# Keep track of connected users
connected_users = {}
message_read_status = {}

# Serve the main chat page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to get current online users
@app.route('/api/users', methods=['GET'])
def get_users():
    users_list = [{"id": uid, "username": data["username"], "avatar": data["avatar"]} 
                 for uid, data in connected_users.items()]
    return jsonify({"users": users_list})

# Handle user connections
@socketio.on('connect')
def handle_connect():
    logger.info(f"Client connected: {request.sid}")
    # Initial connection - we don't have a username yet

# Handle user disconnections
@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    if user_id in connected_users:
        username = connected_users[user_id]["username"]
        avatar = connected_users[user_id]["avatar"]
        logger.info(f"Client disconnected: {username} ({user_id})")
        # Notify other users about the disconnection
        del connected_users[user_id]
        emit('user_event', {
            'type': 'disconnect',
            'username': username,
            'avatar': avatar,
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
            'online_count': len(connected_users)
        }, broadcast=True)
        
        # Broadcast updated user list
        emit('user_list_update', {
            'users': list(connected_users.values()),
            'count': len(connected_users)
        }, broadcast=True)
    else:
        logger.info(f"Unknown client disconnected: {user_id}")

# Handle username registration
@socketio.on('register')
def handle_register(data):
    user_id = request.sid
    username = data.get('username')
    avatar = data.get('avatar', 'default.png')
    
    if not username:
        emit('error', {'message': 'Username cannot be empty'})
        return
    
    # Store user data
    connected_users[user_id] = {
        "id": user_id,
        "username": username,
        "avatar": avatar
    }
    
    logger.info(f"User registered: {username} ({user_id}) with avatar {avatar}")
    
    # Notify everyone about the new user
    emit('user_event', {
        'type': 'connect',
        'username': username,
        'avatar': avatar,
        'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
        'online_count': len(connected_users)
    }, broadcast=True)
    
    # Send the current user list to the new user
    emit('user_list_update', {
        'users': list(connected_users.values()),
        'count': len(connected_users)
    }, broadcast=True)

# Handle messages from clients
@socketio.on('message')
def handle_message(msg_data):
    try:
        user_id = request.sid
        if not isinstance(msg_data, dict):
            msg_data = {'text': str(msg_data)}
            
        text = msg_data.get('text', '').strip()
        
        if not text:
            emit('error', {'message': 'Message cannot be empty'})
            return
            
        # Get user data or use anonymous if not registered
        if user_id in connected_users:
            user_data = connected_users[user_id]
            username = user_data["username"]
            avatar = user_data["avatar"]
        else:
            username = 'Anonymous'
            avatar = 'default.png'
        
        logger.info(f"Message from {username}: {text}")
        
        # Create message ID
        message_id = f"{user_id}-{datetime.datetime.now().timestamp()}"
        
        # Create a structured message
        message = {
            'id': message_id,
            'text': text,
            'username': username,
            'avatar': avatar,
            'sender_id': user_id,
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
            'read_by': [user_id]  # Sender has read their own message
        }
        
        # Store message read status
        message_read_status[message_id] = [user_id]
        
        # Broadcast the message to all connected clients
        emit('chat_message', message, broadcast=True)
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
        emit('error', {'message': 'Error processing your message'})

# Handle read receipts
@socketio.on('message_read')
def handle_message_read(data):
    user_id = request.sid
    message_id = data.get('message_id')
    
    if message_id and message_id in message_read_status:
        if user_id not in message_read_status[message_id]:
            message_read_status[message_id].append(user_id)
            
            # Broadcast read status update
            emit('read_receipt', {
                'message_id': message_id,
                'read_by': message_read_status[message_id]
            }, broadcast=True)

# Handle typing indicators
@socketio.on('typing')
def handle_typing(data):
    user_id = request.sid
    is_typing = data.get('isTyping', False)
    
    if user_id in connected_users:
        user_data = connected_users[user_id]
        emit('typing_indicator', {
            'username': user_data["username"],
            'avatar': user_data["avatar"],
            'isTyping': is_typing
        }, broadcast=True, include_self=False)

# Run the server
if __name__ == '__main__':
    logger.info("Starting Flask-SocketIO chat server...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)