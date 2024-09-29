import random

bingo_numbers = list(range(1, 76))

class Player:
    def __init__(self, user_id, balance):
        self.user_id = user_id
        self.balance = balance
        self.bingo_card = self.generate_bingo_card()

    def generate_bingo_card(self):
        return random.sample(bingo_numbers, 24)

class Game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.players = []
        self.state = "RUN"
        self.winner = None
        self.called_numbers = []
        self.pot = 0

    def add_player(self, player):
        if len(self.players) < 2:
            self.players.append(player)
            return True
        return False

    def is_full(self):
        return len(self.players) == 2

    def make_move(self, player_id, move):
        if self.state == "RUN" and player_id in [p.user_id for p in self.players]:
            if move.strip() == "BINGO":
                self.state = "END"
                self.winner = player_id
                return True, {'winner': player_id}
        return False, "Invalid move or game already over"

    def get_status(self):
        return {
            'game_id': self.game_id,
            'players': [p.user_id for p in self.players],
            'state': self.state,
            'winner': self.winner,
            'called_numbers': self.called_numbers,
            'pot': self.pot
        }

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
class Room:
    def __init__(self, room_id):
        self.game = Game(room_id)  # Initialize the Game
        self.players = []

    def add_player(self, player_id):
        if len(self.players) < 2:
            self.players.append(player_id)
            return True
        return False

    def is_full(self):
        return len(self.players) == 2

    def start_game(self):
        if self.is_full():
            self.game.start_game()  # Start the game if the room is full

    def get_status(self):
        return {
            'room_id': self.game.game_id,
            'players': self.players,
            'state': self.game.state,
            'winner': self.game.winner
        }
    
rooms = {f"room_{i}": Room(f"room_{i}") for i in range(1, 101)}