# Python Chess API

Work in Progress

This project works with Python 3.7 or higger version

## How to run locally:
1. Create a python virtual environment.
- Access to chess folder
- `sudo apt install virtualenv`
- `virtualenv -p python3 chessenv`
- `source chessenv/bin/activate`
- `make install`  to install the requirements
2. Start app with command `make start-worker`

## How to run in Docker:
1. Build docker image:
- `make build`
2. Start app:
- `make start`
3. Inspect logs:
- `make logs`

## Test app
Open Postman, or other similar tools, and call http://localhost:5000/game with JSON data in following format:
```json
{
	"player1": {"name": "Name-a"},
	"player2": {"name": "Name-b"}
}
```

Returns an HTTP 200 OK. The payload contains the following keys: `board` and `id` and `players`.

Use the ID to continue to play using the `/game/<ID>` endpoint. Like http://127.0.0.1:5000/game/ID

The `game` payload should contain the player name, the position of the piece you want to move and the
position of where you want to move the piece to.

Example:

```json
{
	"player": "Name",
	"position": "e2",
	"new_position": "e4"
}
```

## Run tests
`make test`
