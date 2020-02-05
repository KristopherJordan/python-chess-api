from flask import Flask, render_template

from services.play import start_game

app = Flask(__name__)


@app.route("/")
def hello():
    # results = start_game()
    return render_template("results.html")


if __name__ == "__main__":
    app.run(debug=True)
