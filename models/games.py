import logging
import random

from models.boards import Board
from services.utils import WHITE, BLACK

logger = logging.getLogger(__name__)


class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self._moves = []
        self.id = random.randint(1000, 9999)
        self._next_colour = WHITE

    def start_game(self):
        return self

    def get_next_move(self):
        return self._next_colour

    def do_move(self, player, position, new_position):
        if not self.validate_turn(player):
            raise Exception("Turn Not Valid")

        self.board.move_piece(position, new_position, player)

        self._moves.append({"player": player.get_name(), "board": self.board})
        self._next_colour = WHITE if player.get_colour() is BLACK else BLACK

    def validate_turn(self, player):
        if not self._moves:
            if player.get_colour() != WHITE:
                logger.info("%s colour cant start the game", player.get_colour())
                return False
            return True

        if player.get_colour() != self._next_colour:
            logger.info("Not %s's turn", player.get_name())
            return False

        return True
