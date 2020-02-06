from models.games import Game
from services.utils import X_CONVERTER, Y_CONVERTER


def start_game(player1, player2):
    game = Game(player1, player2)
    game.start_game()
    return game


def do_move(player, game, position, new_position):
    position = convert_position(position)
    new_position = convert_position(new_position)
    game.do_move(player, position, new_position)
    return game


def convert_position(position):
    if len(position) != 2:
        raise Exception("Position in wrong format. Example 'e4'. Not: %s" % position)

    x = X_CONVERTER[position[0].lower()]
    y = Y_CONVERTER[position[1].lower()]
    return (y, x)
