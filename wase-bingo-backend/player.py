import random
from bingo_board import BingoBoard

class Player:
    def __init__(self, user_id, balance):
        self.user_id = user_id
        self.balance = balance
        self.bingo_board = BingoBoard()
