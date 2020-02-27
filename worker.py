import logging
import os

from flask import Flask, render_template, jsonify, request

from models.players import Player
from services.play import do_move, start_game
from services.utils import WHITE, BLACK

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Caching the players by name and games by id
GAMES = {}
PLAYERS = {}

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("results.html")


@app.route("/game", methods=["POST"])
def start():
    data = request.json
    logger.info("Starting new game | Data: %s", data)
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

        return_data = {
            "board": game.board.to_dict(),
            "id": game.id,
            "players":
                {
                    "white": player1.get_name(),
                    "black": player2.get_name(),
                },
            "next_move": game.get_next_move(),
        }
        logger.info(f"New game started | White: '{player1.get_name()}' | Black: '{player2.get_name()}' | ID: {game.id}")
        return jsonify(return_data)
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)  # TODO: Raise HTTP error


@app.route("/game/<path:game_id>", methods=["PUT"])
def move_piece(game_id):
    data = request.json
    logger.info(f"Starting to move piece: {data} | game ID: {game_id}")
    try:
        name = data['player'].lower()
        position = data['position']
        new_position = data['new_position']
        if name not in PLAYERS:
            raise Exception(f"{name} is not a player with a running game")

        player = PLAYERS[name]

        if game_id not in GAMES:
            logger.error(f"Game ID '{game_id}' does not exist")
            return resource_not_found(f"Game ID '{game_id}' does not exist")

        game = GAMES[game_id]

        game = do_move(player, game, position, new_position)

        return_data = {
            "board": game.board.to_dict(),
            "id": game.id,
            "next_move": game.get_next_move(),
        }
        logger.info(f"Finished moving piece: {return_data}")
        return jsonify(return_data)
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error: %s" % ex)  # TODO: Raise HTTP error


@app.route("/game/<path:game_id>", methods=["GET"])
def get_game_info(game_id):
    logger.info(f"getting game info | ID: {game_id}")
    try:
        if game_id not in GAMES:
            logger.error(f"Game ID '{game_id}' does not exist")
            return resource_not_found(f"Game ID '{game_id}' does not exist")

        game = GAMES[game_id]
        return_data = {
            "board": game.board.to_dict(),
            "id": game.id,
            "next_move": game.get_next_move(),
        }
        logger.info(f"Finished getting game data: {return_data}")
        return jsonify(return_data)

    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error: %s" % ex)  # TODO: Raise HTTP error


@app.route("/games", methods=["GET"])
def get_games():
    logger.info("Get all games")
    try:
        return_data = []
        for game_id, game in GAMES.items():
            return_data.append(
                {
                    "board": game.board.to_dict(),
                    "id": game.id,
                    "next_move": game.get_next_move(),
                }
            )
        logger.info(f"Get games returned {len(return_data)} games")
        return jsonify(return_data)
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error: %s" % ex)  # TODO: Raise HTTP error


@app.route("/game/<path:game_id>", methods=["DELETE"])
def delete_game(game_id):
    try:
        logger.info(f"Trying to delete game {game_id}")
        if game_id not in GAMES:
            logger.error(f"Game ID '{game_id}' does not exist")
            return resource_not_found(f"Game ID '{game_id}' does not exist")
        GAMES.pop(game_id)
        logger.info(f"deleted game {game_id}")
        return jsonify({}), 204
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error: %s" % ex)  # TODO: Raise HTTP error


@app.route("/games", methods=["DELETE"])
def delete_games():
    logger.info("Deleting all games")
    try:
        [GAMES.pop(game) for game in GAMES.copy()]
        logger.info("all games deleted")
        return jsonify({}), 204
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error: %s" % ex)  # TODO: Raise HTTP error


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


if __name__ == "__main__":
    logger.info("Starting Flask App")
    app.run(debug=True, host='0.0.0.0', port=os.environ.get("HTTP_PORT", "5000"))
