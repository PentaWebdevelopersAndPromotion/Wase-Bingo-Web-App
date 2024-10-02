import random

class Game:
    def __init__(self, game_id, players = []):
        self.game_id = game_id
        self.players = players
        self.called_numbers = set()
        self.winner = None
        self.state = "RUN"

    def call_number(self):
        if self.state == "RUN":
            number = random.randint(1, 75)
            while number in self.called_numbers:
                number = random.randint(1, 75)
            self.called_numbers.add(number)
            for player in self.players:
                player.mark_number(number)
            return number
        return None

    def check_winner(self):
        for player in self.players:
            if player.check_winner():
                self.winner = player.user_id
                self.state = "END"
                return True
        return False

    def end_game(self):
        self.state = "END"

    def get_status(self):
        return {
            "game_id": self.game_id,
            "players": [player.user_id for player in self.players],
            "called_numbers": list(self.called_numbers),
            "winner": self.winner,
            "state": self.state
        }
