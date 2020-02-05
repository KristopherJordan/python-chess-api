from abc import ABCMeta

WHITE = "white"
BLACK = "black"
DIAGONAL = "diagonal"
UP = "up"
DOWN = "down"
SIDE = "side"

cardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
diagonals = [(1, 1), (-1, 1), (1, -1), (-1, -1)]


class Pieces(metaclass=ABCMeta):

    def __init__(self, colour=""):
        colour = colour.lower()
        if colour not in [WHITE, BLACK]:
            print("Wrong input colour: '%s'" % colour)
            raise Exception("Wrong Colour Exception")

        self.colour = colour
        self.name = ""
        self.position = [0, 0]
        self.abbreviation = None

        self.validate()

    def __repr__(self):
        return "%s %s" % (self.colour, self.abbreviation)

    def validate(self):
        print("Not implemented")

    def legal_movement(self, board, position):
        """ [(X, Y)]"""
        print("Not implemented")


class King(Pieces):

    def validate(self):
        self.name = "King"
        self.abbreviation = "K"

        if self.colour == WHITE:
            self.position = [7, 4]
        else:
            self.position = [0, 4]

    def legal_movement(self, board, position):
        return [UP, DOWN, DIAGONAL, SIDE], 8


class Queen(Pieces):

    def validate(self):
        self.name = "Queen"
        self.abbreviation = "Q"

        if self.colour == WHITE:
            self.position = [7, 3]
        else:
            self.position = [0, 3]

    def legal_movement(self, board, position):
        return [UP, DOWN, DIAGONAL, SIDE], 1


class Pawn(Pieces):

    def validate(self):
        self.name = "Pawn"
        self.abbreviation = "P"

    def legal_movement(self, board, position):
        if position[1] - self.position[1] not in [-1, 0, 1]:
            print("Cant move diagonally with %s" % self.name)
            return False
        if self.colour == BLACK:
            if self.position[0] == 7:
                print("First move Black")
                return self.position[0] - position[0] in [1, 2]
            return self.position[0] - position[0] == 1
        if self.position[0] == 1:
            print("First move White")
            return position[0] - self.position[0] in [1, 2]
        return position[0] - self.position[0] == 1


class Bishop(Pieces):

    def validate(self):
        self.name = "Bishop"
        self.abbreviation = "B"

    def legal_movement(self, board, position):
        return [DIAGONAL], 8


class Knight(Pieces):

    def validate(self):
        self.name = "Knight"
        self.abbreviation = "KN"

    def legal_movement(self, board, position):
        # TODO: hmm
        return [UP, SIDE], 8


class Rook(Pieces):

    def validate(self):
        self.name = "Rook"
        self.abbreviation = "R"


    def legal_movement(self, board, position):
        return [UP, SIDE], 8

