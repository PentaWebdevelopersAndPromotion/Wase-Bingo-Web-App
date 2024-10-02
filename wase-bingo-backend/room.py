class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.game_id = None
        self.players = []

    def add_player(self, player):
        if len(self.players) < 100:
            self.players.append(player)
            return True
        return False

    def is_full(self):
        return len(self.players) == 2

    def start_game(self, game_id):
        if self.is_full():
            self.game_id = game_id

    def get_status(self):
        return {
            'room_id': self.room_id,
            'players': [p.user_id for p in self.players],
            'game_id': self.game_id
        }
