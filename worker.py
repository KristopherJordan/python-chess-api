from flask import Flask, render_template, request, jsonify

from models.players import Player
from models.pieces import WHITE, BLACK
from services.play import start_game, do_move

# Caching the players by name and games by id
GAMES = {}
PLAYERS = {}

app = Flask(__name__)


@app.route("/")
def hello():
    # results = start_game()
    return render_template("results.html")


@app.route("/start", methods=["POST"])
def start():
    data = request.json
    try:
        # Create players
        player1_name = data['player1']['name'].lower()
        player2_name = data['player2']['name'].lower()
        player1 = Player(player1_name, WHITE)
        player2 = Player(player2_name, BLACK)

        # Caching players
        PLAYERS[player1_name] = player1
        PLAYERS[player2_name] = player2

        game = start_game(player1, player2)

        GAMES[str(game.id)] = game
        return_data = {"game": game.board.print_board(), "id": game.id}
        return jsonify(return_data)
    except Exception as ex:
        print("Exception: %s" % ex)
        return jsonify("Error %s" % ex)


@app.route("/move/<path:game_id>", methods=["PUT"])
def move_piece(game_id):
    data = request.json
    print("Starting to move piece: %s | game: %s" % (data, game_id))
    try:
        name = data['player'].lower()
        position = data['position']
        new_position = data['new_position']
        player = PLAYERS[name]

        if game_id not in GAMES:
            raise Exception("Game ID not valid")

        game = GAMES[game_id]

        game = do_move(player, game, position, new_position)

        return_data = {"game": game.board.print_board(), "id": game.id}
        print("Finished moving piece: %s" % return_data)
        return jsonify(return_data)
    except Exception as ex:
        print("Exception: %s" % ex)
        return jsonify("Error: %s" % ex)


if __name__ == "__main__":
    app.run(debug=True)
