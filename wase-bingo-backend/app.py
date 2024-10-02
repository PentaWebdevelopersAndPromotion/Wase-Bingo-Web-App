from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from game_manager import GameManager
from room_manager import RoomManager
from auth import authenticate_user
from utils import newID

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize the room manager to handle multiple rooms
room_manager = RoomManager()
game_manager = GameManager()

@app.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = list(room_manager.rooms.keys())
    return jsonify(rooms), 200

@app.route('/room_status/<room_id>', methods=['GET'])
def room_status(room_id):
    status = room_manager.get_room_status(room_id)
    if status:
        return jsonify(status), 200
    return jsonify({'error': 'Room not found'}), 404

@app.route('/join_room/<room_id>', methods=['POST'])
def join_room_api(room_id):
    try:
        player_id = request.json['player_id']
        security_code = request.json['security_code']

        # Validate the security code here
        user = authenticate_user(player_id, security_code)
        if user is not None:
            result, message = room_manager.add_player_to_room(room_id, user)
            if result:
                if room_manager.is_room_full(room_id):
                    room_manager.start_game(room_id)  # Start game if room is full
                return jsonify({'message': 'Joined room', 'room_id': room_id}), 200
            else:
                return jsonify({'error': message}), 400
        else:
            return jsonify({'error': 'Invalid security code or player ID'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('make_move')
def handle_move(data):
    try:
        game_id = data['game_id']
        player_id = data['player_id']
        move = data['move']

        result, response = game_manager.make_move(game_id, player_id, move)
        if result:
            socketio.emit('update', {'game_id': game_id, 'status': response}, room=game_id)
            if 'winner' in response:
                socketio.emit('winner_announcement', {'game_id': game_id, 'winner': response['winner']}, room=game_id)
        else:
            emit('error', {'message': response})
    except Exception as e:
        emit('error', {'message': str(e)})



@socketio.on('make_move')
def handle_move(data):
    game_id = data['game_id']
    player_id = data['player_id']
    move = data['move']

    result, response = game_manager.make_move(game_id, player_id, move)
    if result:
        socketio.emit('update', {'game_id': game_id, 'status': response}, room=game_id)
        if 'winner' in response:
            socketio.emit('winner_announcement', {'game_id': game_id, 'winner': response['winner']}, room=game_id)
    else:
        emit('error', {'message': response})

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

@socketio.on('join')
def on_join(data):
    game_id = data['game_id']
    join_room(game_id)
    emit('message', f'{request.sid} has joined the game {game_id}', room=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True)
