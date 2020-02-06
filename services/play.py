from models.games import Game
from services.utils import convert_position


def start_game(player1, player2):
    game = Game(player1, player2)
    game.start_game()
    return game


def do_move(player, game, position, new_position):
    position = convert_position(position)
    new_position = convert_position(new_position)
    game.do_move(player, position, new_position)
    return game
