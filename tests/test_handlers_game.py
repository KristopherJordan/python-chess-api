from unittest.case import TestCase

from services.utils import WHITE, BLACK
from worker import app


class TestGameHandlers(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

        self.player1_name = "White Player"
        self.player2_name = "Black Player"

    def tearDown(self):
        pass

    def test_create_game(self):
        payload = {
            "player1": {"name": self.player1_name},
            "player2": {"name": self.player2_name},
        }

        resp = self.app.post('/game', json=payload)
        self._check_ok_resp(resp)
        self.assertIn('board', resp.json)
        self.assertIn('id', resp.json)
        self.assertIn('players', resp.json)
        self.assertIn('next_move', resp.json)

        self.assertEqual(resp.json['next_move'], WHITE)

    def test_first_move(self):
        game_id = self._create_game()
        # First move
        payload = {
            "player": self.player1_name,
            "position": "e2",
            "new_position": "e4",
        }
        resp = self.app.put(f'/game/{game_id}', json=payload)
        self._check_ok_resp(resp)
        self.assertEqual(resp.json['next_move'], BLACK)

        # Validate Move
        self.assertEqual(resp.json['board']['2']['e'], "None")
        self.assertEqual(resp.json['board']['4']['e'], "white Pawn")

    def test_get_game(self):
        game_id = self._create_game()
        resp = self.app.get(f'/game/{game_id}')
        self._check_ok_resp(resp)
        self.assertIn('board', resp.json)
        self.assertIn('id', resp.json)
        self.assertIn('next_move', resp.json)

    def test_get_game_not_found(self):
        fake_game_id = 12341
        resp = self.app.get(f'/game/{fake_game_id}')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json['error'], f"Game ID '{fake_game_id}' does not exist")

    def _check_ok_resp(self, resp):
        self.assertEqual(resp.status_code, 200)

    def _create_game(self):
        payload = {
            "player1": {"name": self.player1_name},
            "player2": {"name": self.player2_name},
        }

        resp = self.app.post('/game', json=payload)
        self._check_ok_resp(resp)
        return resp.json['id']
