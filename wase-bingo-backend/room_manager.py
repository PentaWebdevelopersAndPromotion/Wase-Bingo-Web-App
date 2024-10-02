from room import Room

class RoomManager:
    def __init__(self, game_manager, socketio, num_rooms=100):
        self.game_manager = game_manager
        self.socketio = socketio
        self.rooms = {f"room_{i}": Room(f"room_{i}", self.game_manager, self.socketio) for i in range(1, num_rooms + 1)}

    def create_room(self, room_id):
        self.rooms[room_id] = Room(room_id, self.game_manager, self.socketio)

    def add_player_to_room(self, room_id, player):
        if room_id in self.rooms:
            if self.rooms[room_id].add_player(player):
                return True, "Player added"
            else:
                return False, "Room is full"
        return False, "Room not found"

    def is_room_full(self, room_id):
        if room_id in self.rooms:
            return len(self.rooms[room_id].players) >= Room.max_players
        return False

    def get_room_status(self, room_id):
        if room_id in self.rooms:
            return self.rooms[room_id].get_status()
        return None

    def start_game(self, room_id):
        if room_id in self.rooms:
            self.rooms[room_id].start_game(newID())
