from models.pieces import King, Queen, Pawn, Bishop, Rook, Knight, WHITE, BLACK


class Board:

    def __init__(self):
        self._board = []
        self._create_empty_board()

    def move_piece(self, position, new_position):
        if not isinstance(position, tuple):
            raise Exception("Position Needs To Be A Tuple")  # TODO: Raise 403

        if self._board[position[0]][position[1]] is None:
            raise Exception("No Piece in Position")  # TODO: Raise 404

        if not self.is_in_bounds(new_position):
            raise Exception("New Position: %s Not In Bounds" % new_position)

        piece = self._board[position[0]][position[1]]
        new_position = self.validate_move(piece, new_position)

    def validate_move(self, piece, new_position):
        if not piece.legal_movement(self._board, new_position):
            raise Exception("Not Legal Position: %s for piece: %s" % (new_position, piece))





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

        rook = Rook(colour)
        self._board[row][0] = rook

        rook = Rook(colour)
        self._board[row][7] = rook

        knight = Knight(colour)
        self._board[row][1] = knight

        knight = Knight(colour)
        self._board[row][6] = knight

        bishop = Bishop(colour)
        self._board[row][2] = bishop

        bishop = Bishop(colour)
        self._board[row][5] = bishop

    def _set_pawns(self, row, colour):
        for i in range(8):
            pawn = Pawn(colour)
            self._board[row][i] = pawn

    def print_board(self):
        headers = "   |   A  |  B  |  C  |  D  |  E  |  F  |  G  |  H  |"

        print(headers)
        for i, row in enumerate(self._board):
            print("%s | %s" % (i, row))
        print(headers)

#uniDict = {WHITE : {Pawn : "♙", Rook : "♖", Knight : "♘", Bishop : "♗", King : "♔", Queen : "♕" }, BLACK : {Pawn : "♟", Rook : "♜", Knight : "♞", Bishop : "♝", King : "♚", Queen : "♛" }}
