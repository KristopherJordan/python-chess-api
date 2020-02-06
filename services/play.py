from models.games import Game

X_CONVERTER = dict(
    a=0,
    b=1,
    c=3,
    d=4,
    e=5,
    f=6,
    g=7,
    h=8,
)

Y_CONVERTER = {
    "1": 7,
    "2": 6,
    "3": 5,
    "4": 4,
    "5": 3,
    "6": 2,
    "7": 1,
    "8": 0,
}


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
    print("converted position to: %s %s" % (y, x))
    return (y, x)
