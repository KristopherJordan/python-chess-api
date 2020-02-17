# Python Chess API

Work in Progress

## How to run:
1. Create a python virtual environment.
Example with `pyenv`:
- `brew install pyenv` ([pyenv Documentation](https://github.com/pyenv/pyenv))
- `brew install pyenv-virtualenv` ([pyenv-virtualenv Documentation](https://github.com/pyenv/pyenv-virtualenv))
- `pyenv virtualenv 3.7.3 chess`
- `pyenv activate chess`
- `make install`  to install the requirements
2. Start app with command `make start`
3. Open Postman, or other similar tools, and call http://127.0.0.1:5000/start with JSON data in following format:
```json
{
	"player1": {"name": "Namey"},
	"player2": {"name": "Mac Chessy"}
}
```

Returns an HTTP 200 OK. The payload contains the following keys: `game` and `id` and `players`.

Use the ID to continue to play using the `/move/<ID>` endpoint. Like http://127.0.0.1:5000/move/ID

The `move` payload should contain the player name, the position of the piece you want to move and the
position of where you want to move the piece to.

Example:

```json
{
	"player": "Namey",
	"position": "e2",
	"new_position": "e4"
}
```

## Run tests
`make test`
