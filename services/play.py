from models.board import Board


def start_game():
    headers = "   |   A  |  B  |  C  |  D  |  E  |  F  |  G  |  H  |"
    board = Board()
    results = """
    %s
    %s
    """ % (headers, headers)
    return results
