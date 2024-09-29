from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from game import GameManager
import game
from auth import authenticate_user
from utils import newID

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize the game manager to handle multiple games
game_manager = GameManager()

@app.route('/create_game', methods=['POST'])
def create_game():
    game_id = newID("game")
    game_manager.create_game(game_id)
    return jsonify({'game_id': game_id})

@app.route('/join_room/<room_id>', methods=['POST'])
def join_room_api(room_id):
    if room_id in game.rooms:
        player_id = request.json['player_id']
        security_code = request.json['security_code']

        # Validate the security code here
        user = authenticate_user(player_id, security_code)
        if user is not None:
            if game.rooms[room_id].add_player(player_id):
                if game.rooms[room_id].is_full():
                    game.rooms[room_id].start_game()  # Start game if room is full
                return jsonify({'message': 'Joined room', 'room_id': room_id})
            else:
                return jsonify({'error': 'Room is full'}), 400
        else:
            return jsonify({'error': 'Invalid security code or player ID'}), 403
    return jsonify({'error': 'Room not found'}), 404



@app.route('/game_status/<game_id>', methods=['GET'])
def game_status(game_id):
    status = game_manager.get_game_status(game_id)
    if status:
        return jsonify(status)
    return jsonify({'error': 'Game not found'}), 404

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
