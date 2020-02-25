import logging
from abc import ABCMeta

from models.boards import create_empty_board
from services.utils import X_INVERTER, Y_INVERTER, WHITE, BLACK

logger = logging.getLogger(__name__)

move_patterns = {
    "up_left": [1, -1],
    "up_right": [1, 1],
    "down_left": [-1, -1],
    "down_right": [-1, 1],
}

POS_PIECES = {
    WHITE: {},
    BLACK: {},
}


class Pieces(metaclass=ABCMeta):
    piece_id = 1

    def __init__(self, colour="", position=None):
        colour = colour.lower()
        if colour not in [WHITE, BLACK]:
            logger.info("Wrong input colour: '%s'", colour)
            raise Exception("Wrong Colour Exception")

        self._colour = colour
        self._name = ""
        self._position = position
        self._abbreviation = None
        self.piece_id = Pieces.piece_id
        Pieces.piece_id += 1

        self.validate()
        POS_PIECES[self.get_colour()].update({self.get_position(): self})

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
        logger.info(f"removing {self}")
        self._position = None

    def is_kill_valid(self, other_piece):
        """
        Validate Kill for given piece
        :param other_piece: Piece object to eliminate
        :return: boolean
        """
        if self.get_colour() == other_piece.get_colour():
            logger.info(f"Both pieces are {self.get_colour()}")
            return False
        return True

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

    def get_position(self):
        return self._position

    def set_position(self, position):
        """
        Set position tuple to piece
        :param position: tuple, (y,x)
        """
        self._position = position

    def is_in_check(self, colour, board):
        return False

    def get_move_options(self, board, board_options):
        empty_board = create_empty_board()
        for row in empty_board.copy():
            for column in row:
                if self.is_movement_valid(board, (row, column)):





class King(Pieces):

    def validate(self):
        self._name = "King"
        self._abbreviation = "K"

        if self._colour == WHITE:
            self._position = [7, 4]
        else:
            self._position = [0, 4]

    def is_movement_valid(self, board, new_position):
        if self._position == new_position:
            return False
        if new_position[1] - self._position[1] not in [-1, 0, 1]:
            return False
        if new_position[0] - self._position[0] not in [-1, 0, 1]:
            return False
        # TODO: Check if new_position is in check
        return self.is_in_check(self.get_colour(), board)


class Queen(Pieces):

    def validate(self):
        self._name = "Queen"
        self._abbreviation = "Q"

        if self._colour == WHITE:
            self._position = [7, 3]
        else:
            self._position = [0, 3]

    def is_movement_valid(self, board, new_position):
        """
        Check first if movement is vertical/ horisontal. Then check diagonal movement
        """
        if self.get_y_pos() == new_position[0] or self.get_x_pos() == new_position[1]:
            return is_ver_hor_movement_valid(self, new_position, board)
        return is_diagonal_move_valid(self, new_position, board)


class Pawn(Pieces):

    def validate(self):
        self._name = "Pawn"
        self._abbreviation = "P"

    def is_movement_valid(self, board, new_position):
        if new_position[1] - self._position[1] not in [-1, 0, 1]:
            logger.info(f"Cant move diagonally with {self}")
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
            logger.info(f"Both pieces are {self.get_colour()}")
            return False
        if self.get_x_pos() - other_piece.get_x_pos() not in [1, -1]:
            logger.info(f"{self} can only kill diagonally")
            return False
        return True


class Bishop(Pieces):

    def validate(self):
        self._name = "Bishop"
        self._abbreviation = "B"

    def is_movement_valid(self, board, new_position):
        return is_diagonal_move_valid(self, new_position, board)


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
        return is_ver_hor_movement_valid(self, new_position, board)


def is_diagonal_move_valid(piece, new_position, board):
    """
    Check if diagonal movement is valid

    :param piece: Piece object
    :param new_position: End Position
    :param board: Board object
    :return: Boolean
    """
    logger.info("Checking if diagonal movement is valid")
    if piece._position == new_position:
        return False
    # Find length between the coordinates
    x_vec = piece.get_x_pos() - new_position[1]
    y_vec = piece.get_y_pos() - new_position[0]
    # x1 - x2 and y1 - y2 should be the same if the piece moves diagonally
    if abs(x_vec) != abs(y_vec):
        logger.warning("Bishop can only move diagonally")
        return False

    if new_position[1] > piece.get_x_pos():
        if new_position[0] > piece.get_y_pos():
            move = move_patterns["up_right"]
        else:
            move = move_patterns["down_right"]
    else:
        if new_position[0] > piece.get_y_pos():
            move = move_patterns["up_left"]
        else:
            move = move_patterns["down_left"]

    new_y = piece.get_y_pos()
    new_x = piece.get_x_pos()
    for pos in range(x_vec):
        # Move diagonally for each iteration in the range of the total x-axis movement
        new_y = move[0] + new_y
        new_x = move[1] + new_x
        if (new_y, new_x) == new_position:
            return True
        if board[new_y][new_x]:
            logger.warning(f"{piece} cant move over existing piece")
            return False

    return True


def is_ver_hor_movement_valid(piece, new_position, board):
    """
    Check if vertical or horisontal movement is valid

    :param piece: Piece object
    :param new_position: End Position
    :param board: Board object
    :return: Boolean
    """
    logger.info("Checking if vertical or horisontal movement is valid")
    if piece._position == new_position:
        return False

    if not (piece.get_y_pos() == new_position[0] or piece.get_x_pos() == new_position[1]):
        return False

    if piece.get_y_pos() == new_position[0]:
        # Move piece horisontally | Check if pieces in the way
        min_pos = min(piece.get_x_pos(), new_position[1])
        max_pos = max(piece.get_x_pos(), new_position[1])
        for pos in range(min_pos, max_pos):
            if (new_position[0], pos) == new_position:
                return True
            if board[new_position[0]][pos]:
                logger.warning(f"{piece} cant move over existing piece")
                return False

    else:
        # Move piece vertically | Check if pieces in the way
        min_pos = min(piece.get_y_pos(), new_position[0])
        max_pos = max(piece.get_y_pos(), new_position[0])
        for pos in range(min_pos, max_pos):
            if (new_position[0], pos) == new_position:
                return True
            if board[pos][new_position[1]]:
                logger.warning(f"{piece} cant move over existing piece")
                return False

    return True
