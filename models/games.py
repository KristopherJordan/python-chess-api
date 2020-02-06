import logging
import random

from models.boards import Board
from models.pieces import WHITE, BLACK

logger = logging.getLogger(__name__)


class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.moves = []
        self.id = random.randint(1000, 9999)
        self.next_colour = WHITE

    def start_game(self):
        return self

    def do_move(self, player, position, new_position):
        if not self.validate_turn(player):
            raise Exception("Turn Not Valid")

        self.board.move_piece(position, new_position, player)
        self.moves.append({"player": player.name, "board": self.board})
        self.next_colour = WHITE if player.colour is BLACK else BLACK
        return self.board

    def validate_turn(self, player):
        if not self.moves:
            if player.colour != WHITE:
                logger.info("%s colour cant start the game", player.colour)
                return False
            return True

        if player.colour != self.next_colour:
            logger.info("Not %s's turn", player.name)
            return False

        return True
