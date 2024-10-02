import random

class BingoBoard:
    def __init__(self):
        self.board = self.generate_board()
        self.called_numbers = set()

    def generate_board(self):
        columns = {}
        ranges = {
            'B': range(1, 16),
            'I': range(16, 31),
            'N': range(31, 46),
            'G': range(46, 61),
            'O': range(61, 76)
        }
        for letter, number_range in ranges.items():
            columns[letter] = random.sample(number_range, 5 if letter != 'N' else 4)
        columns['N'].insert(2, 'FREE')  # Insert the free space in the middle of the 'N' column
        return columns

    def display_board(self):
        print(" B   I   N   G   O")
        for i in range(5):
            row = []
            for letter in 'BINGO':
                row.append(str(self.board[letter][i]).center(3))
            print(" ".join(row))

    def has_number(self, number):
        return any(number in self.board[letter] for letter in 'BINGO')

    def mark_number(self, number):
        if number in self.called_numbers:
            return False
        self.called_numbers.add(number)
        for letter in 'BINGO':
            if number in self.board[letter]:
                index = self.board[letter].index(number)
                self.board[letter][index] = 'X'
                return True
        return False

    def check_winner(self):
        # Check rows
        for i in range(5):
            if all(self.board[letter][i] == 'X' for letter in 'BINGO'):
                return True

        # Check columns
        for letter in 'BINGO':
            if all(self.board[letter][i] == 'X' for i in range(5)):
                return True

        # Check diagonals
        if all(self.board['BINGO'[i]][i] == 'X' for i in range(5)):
            return True
        if all(self.board['BINGO'[i]][4 - i] == 'X' for i in range(5)):
            return True

        return False
