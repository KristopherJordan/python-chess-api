import logging
from abc import ABCMeta

from services.utils import X_INVERTER, Y_INVERTER

logger = logging.getLogger(__name__)

WHITE = "white"
BLACK = "black"

cardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
diagonals = [(1, 1), (-1, 1), (1, -1), (-1, -1)]


class Pieces(metaclass=ABCMeta):

    def __init__(self, colour="", position=None):
        colour = colour.lower()
        if colour not in [WHITE, BLACK]:
            logger.info("Wrong input colour: '%s'", colour)
            raise Exception("Wrong Colour Exception")

        self._colour = colour
        self._name = ""
        self._position = position
        self._abbreviation = None

        self.validate()

    def __repr__(self):
        return "%s %s" % (self._colour, self._abbreviation)

    def validate(self):
        logger.info("Not implemented")

    def is_movement_valid(self, board, new_position):
        """ [(Y, X)]"""
        logger.info("Not implemented")

    def remove(self):
        """
        Remove position for Piece
        """
        logger.info("removing %s", self)
        self._position = None

    def is_kill_valid(self, other_piece):
        """
        Validate Kill for given piece
        :param other_piece: Piece object to eliminate
        :return: boolean
        """
        pass

    def get_colour(self):
        """
        Get piece colour
        """
        return self._colour

    def get_name(self):
        """
        Get Piece Name
        """
        return self._name

    def get_y_pos(self):
        """
        Get Piece Y Position
        """
        return self._position[0]

    def get_x_pos(self):
        """
        Get Piece X Position
        """
        return self._position[1]

    def get_hr_pos(self):
        """
        Human Readable Position. Ex: 'e2'
        """
        return "%s%s" % (X_INVERTER[str(self.get_x_pos())], Y_INVERTER[str(self.get_y_pos())])

    def set_position(self, position):
        """
        Set position tuple to piece
        :param position: tuple, (y,x)
        """
        self._position = position


class King(Pieces):

    def validate(self):
        self._name = "King"
        self._abbreviation = "K"

        if self._colour == WHITE:
            self._position = [7, 4]
        else:
            self._position = [0, 4]

    def is_movement_valid(self, board, new_position):
        return


class Queen(Pieces):

    def validate(self):
        self._name = "Queen"
        self._abbreviation = "Q"

        if self._colour == WHITE:
            self._position = [7, 3]
        else:
            self._position = [0, 3]

    def is_movement_valid(self, board, new_position):
        return


class Pawn(Pieces):

    def validate(self):
        self._name = "Pawn"
        self._abbreviation = "P"

    def is_movement_valid(self, board, new_position):
        if new_position[1] - self._position[1] not in [-1, 0, 1]:
            logger.info("Cant move diagonally with %s", self._name)
            return False
        if self._colour == BLACK:
            if self._position[0] == 1:
                logger.info("First move Black")
                return new_position[0] - self._position[0] in [1, 2]
            return new_position[0] - self._position[0] == 1
        if self._position[0] == 6:
            logger.info("First move White")
            return self._position[0] - new_position[0] in [1, 2]
        return self._position[0] - new_position[0] == 1

    def is_kill_valid(self, other_piece):
        if self.get_colour() == other_piece.get_colour():
            logger.info("Both pieces are %s" % self.get_colour())
            return False
        if self.get_x_pos() - other_piece.get_x_pos() not in [1, -1]:
            logger.info("%s can only kill diagonally", self)
            return False
        return True


class Bishop(Pieces):

    def validate(self):
        self._name = "Bishop"
        self._abbreviation = "B"

    def is_movement_valid(self, board, new_position):
        return


class Knight(Pieces):

    def validate(self):
        self._name = "Knight"
        self._abbreviation = "KN"

    def is_movement_valid(self, board, new_position):
        # TODO: hmm
        return


class Rook(Pieces):

    def validate(self):
        self._name = "Rook"
        self._abbreviation = "R"

    def is_movement_valid(self, board, new_position):
        if not (self.get_y_pos() == new_position[0] or self.get_x_pos() == new_position[1]):
            return False

        if self.get_y_pos() == new_position[0]:
            # Move piece horisontally | Check if pieces in the way
            min_pos = min(self.get_x_pos(), new_position[1])
            max_pos = max(self.get_x_pos(), new_position[1])
            for pos in range(min_pos, max_pos):
                if board[new_position[0]][pos]:
                    logger.warning("%s cant move over existing piece", self._abbreviation)
                    return False

        else:
            # Move piece vertically | Check if pieces in the way
            min_pos = min(self.get_y_pos(), new_position[0])
            max_pos = max(self.get_y_pos(), new_position[0])
            for pos in range(min_pos, max_pos):
                if board[pos][new_position[1]]:
                    logger.warning("%s cant move over existing piece", self._abbreviation)
                    return False

        return True
