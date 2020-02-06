import random

from models.boards import Board


class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.moves = []
        self.id = random.randint(1000, 9999)

    def start_game(self):
        return self

    def do_move(self, player, position, new_position):
        if not self.validate_turn(player):
            raise Exception("Turn Not Valid")

        self.board.move_piece(position, new_position)
        self.moves.append({"player": player, "board": self.board})  # TODO: Assure its current board
        return self.board

    def validate_turn(self, player):
        if not self.moves:
            return True

        if self.moves[-1]["player"] == player:
            print("Not %s's turn" % player)
            return False

        return True