from game import Game

class GameManager:
    def __init__(self):
        self.games = {}

    def create_game(self, game_id):
        self.games[game_id] = Game(game_id)

    def add_player_to_game(self, game_id, player):
        if game_id in self.games:
            self.games[game_id].players.append(player)
            return True, "Player added"
        return False, "Game not found"

    def get_game_status(self, game_id):
        if game_id in self.games:
            return self.games[game_id].get_status()
        return None

    def make_move(self, game_id, player_id, move):
        if game_id in self.games:
            game = self.games[game_id]
            # Assuming `move` is a number to be called in Bingo
            number = game.call_number()
            if number:
                if game.check_winner():
                    return True, {"status": game.get_status(), "winner": game.winner}
                return True, {"status": game.get_status()}
            return False, "No number called"
        return False, "Game not found"
