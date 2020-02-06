from models.pieces import King, Queen, Pawn, Bishop, Rook, Knight, WHITE, BLACK


class Board:

    def __init__(self):
        self._board = []
        self._create_empty_board()
        self.print_board()

    def move_piece(self, position, new_position):
        if not (isinstance(position, tuple) or isinstance(new_position, tuple)):
            raise Exception("Position Needs To Be A Tuple")  # TODO: Raise 403

        if self._board[position[0]][position[1]] is None:
            raise Exception("No Piece in Position")  # TODO: Raise 404

        if not self.is_in_bounds(new_position):
            raise Exception("New Position: %s Not In Bounds" % new_position)

        piece = self._board[position[0]][position[1]]
        print(piece)

        if not self._is_move_valid(piece, new_position):
            raise Exception("Move %s to %s is not valid" % (piece, new_position))

        self._place_piece(piece, new_position)
        print(self.print_board())

    def _place_piece(self, piece, new_position):
        existing_piece = self._board[new_position[0]][new_position[1]]
        if existing_piece:
            print("Existing piece: %s  | taken by: %s" % (existing_piece, piece))
            existing_piece.remove()
            self._board[piece.position[0]][piece.position[1]] = None
            self._board[new_position[0]][new_position[1]] = piece
            piece.position = new_position
        else:
            print("placing piece %s to %s" % (piece, new_position))
            self._board[piece.position[0]][piece.position[1]] = None
            self._board[new_position[0]][new_position[1]] = piece
            piece.position = new_position

        print("Moved %s to %s" % (piece, piece.position))

    def _is_move_valid(self, piece, new_position):
        if not piece.is_movement_valid(self._board, new_position):
            print("Not Legal Movement: %s for piece: %s" % (new_position, piece))
            return False
        existing_piece = self._board[new_position[0]][new_position[1]]
        if existing_piece:
            print("%s is occupied by %s" % (new_position, existing_piece))
            if not piece.is_kill_valid(existing_piece):
                return False

        print("valid move")
        return True

    @staticmethod
    def is_in_bounds(position):
        if 0 <= position[0] <= 7 and 0 <= position[1] <= 7:
            return True
        return False

    def _create_empty_board(self):
        for i in range(8):
            column = [None] * 8
            self._board.append(column)
            if i == 0:
                self._set_pieces(i, BLACK)
            elif i == 1:
                self._set_pawns(i, BLACK)
            elif i == 6:
                self._set_pawns(i, WHITE)
            elif i == 7:
                self._set_pieces(i, WHITE)

    def _set_pieces(self, row, colour):
        king = King(colour)
        self._board[row][king.position[1]] = king

        queen = Queen(colour)
        self._board[row][queen.position[1]] = queen

        rook = Rook(colour, (row, 0))
        self._board[row][0] = rook

        rook = Rook(colour, (row, 7))
        self._board[row][7] = rook

        knight = Knight(colour, (row, 1))
        self._board[row][1] = knight

        knight = Knight(colour, (row, 6))
        self._board[row][6] = knight

        bishop = Bishop(colour, (row, 2))
        self._board[row][2] = bishop

        bishop = Bishop(colour, (row, 5))
        self._board[row][5] = bishop

    def _set_pawns(self, row, colour):
        for i in range(8):
            pawn = Pawn(colour, (row, i))
            self._board[row][i] = pawn

    def print_board(self):
        headers = "\n   |   A  |  B  |  C  |  D  |  E  |  F  |  G  |  H  |\n "
        return_string = """%s""" % headers
        return_string += '\n'.join(["%s | %s" % (i, row) for i, row in enumerate(self._board)])
        return_string += headers
        return return_string


# {WHITE : {Pawn : "♙", Rook : "♖", Knight : "♘", Bishop : "♗", King : "♔", Queen : "♕" }, BLACK : {Pawn : "♟", Rook : "♜", Knight : "♞", Bishop : "♝", King : "♚", Queen : "♛" }}