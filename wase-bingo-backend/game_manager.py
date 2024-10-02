from game import Game

class GameManager:
    def __init__(self):
        self.games = {}

    def create_game(self, game_id):
        self.games[game_id] = Game(game_id)

    def add_player_to_game(self, game_id, player):
        if game_id in self.games:
            if self.games[game_id].add_player(player):
                return True, "Player added"
            else:
                return False, "Game is full"
        return False, "Game not found"

    def is_game_full(self, game_id):
        return self.games[game_id].is_full()

    def get_game_status(self, game_id):
        if game_id in self.games:
            return self.games[game_id].get_status()
        return None

    def make_move(self, game_id, player_id, move):
        if game_id in self.games:
            return self.games[game_id].make_move(player_id, move)
        return False, "Game not found"
