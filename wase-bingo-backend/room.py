import threading
import time
from utils import newID

class Room:
    max_players = 100

    def __init__(self, room_id, game_manager, socketio):
        self.room_id = room_id
        self.game_id = None
        self.players = []
        self.timer = 30
        self.timer_thread = None
        self.timer_lock = threading.Lock()
        self.game_manager = game_manager
        self.socketio = socketio

    def add_player(self, player):
        if len(self.players) < Room.max_players:
            self.players.append(player)
            self.reset_timer()
            return True
        return False

    def reset_timer(self):
        with self.timer_lock:
            self.timer = 30
            if self.timer_thread is None or not self.timer_thread.is_alive():
                self.timer_thread = threading.Thread(target=self.start_timer)
                self.timer_thread.start()

    def start_timer(self):
        while self.timer > 0:
            time.sleep(1)
            with self.timer_lock:
                self.timer -= 1
                self.socketio.emit('timer_update', {'room_id': self.room_id, 'timer': self.timer}, room=self.room_id)
                if self.timer == 0:
                    self.start_game(newID("game_"))

    def is_ready(self):
        return len(self.players) >= 2

    def start_game(self, game_id):
        if self.is_ready():
            self.game_id = game_id
            self.game_manager.create_game(game_id)
            for player in self.players:
                self.game_manager.add_player_to_game(game_id, player)
            self.socketio.emit('game_start', {'room_id': self.room_id, 'game_id': self.game_id}, room=self.room_id)

    def get_status(self):
        return {
            'room_id': self.room_id,
            'players': [p.user_id for p in self.players],
            'game_id': self.game_id,
            'timer': self.timer
        }
