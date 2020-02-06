import logging
from abc import ABCMeta

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

        self.colour = colour
        self.name = ""
        self.position = position
        self.abbreviation = None

        self.validate()

    def __repr__(self):
        return "%s %s" % (self.colour, self.abbreviation)

    def validate(self):
        logger.info("Not implemented")

    def is_movement_valid(self, board, position):
        """ [(Y, X)]"""
        logger.info("Not implemented")

    def remove(self):
        logger.info("removing %s", self)
        self.position = None

    def is_kill_valid(self, other_piece):
        pass


class King(Pieces):

    def validate(self):
        self.name = "King"
        self.abbreviation = "K"

        if self.colour == WHITE:
            self.position = [7, 4]
        else:
            self.position = [0, 4]

    def is_movement_valid(self, board, position):
        return


class Queen(Pieces):

    def validate(self):
        self.name = "Queen"
        self.abbreviation = "Q"

        if self.colour == WHITE:
            self.position = [7, 3]
        else:
            self.position = [0, 3]

    def is_movement_valid(self, board, position):
        return


class Pawn(Pieces):

    def validate(self):
        self.name = "Pawn"
        self.abbreviation = "P"

    def is_movement_valid(self, board, position):
        if position[1] - self.position[1] not in [-1, 0, 1]:
            logger.info("Cant move diagonally with %s", self.name)
            return False
        if self.colour == BLACK:
            if self.position[0] == 1:
                logger.info("First move Black")
                return position[0] - self.position[0] in [1, 2]
            return position[0] - self.position[0] == 1
        if self.position[0] == 6:
            logger.info("First move White")
            return self.position[0] - position[0] in [1, 2]
        return self.position[0] - position[0] == 1

    def is_kill_valid(self, other_piece):
        if self.colour == other_piece.colour:
            logger.info("Both pieces are %s" % self.colour)
            return False
        if self.position[1] - other_piece.position[1] not in [1, -1]:
            logger.info("%s can only kill diagonally", self)
            return False
        return True


class Bishop(Pieces):

    def validate(self):
        self.name = "Bishop"
        self.abbreviation = "B"

    def is_movement_valid(self, board, position):
        return


class Knight(Pieces):

    def validate(self):
        self.name = "Knight"
        self.abbreviation = "KN"

    def is_movement_valid(self, board, position):
        # TODO: hmm
        return


class Rook(Pieces):

    def validate(self):
        self.name = "Rook"
        self.abbreviation = "R"

    def is_movement_valid(self, board, position):
        return

