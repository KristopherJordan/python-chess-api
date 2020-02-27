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
        # Delete all games between tests
        self.app.delete(f'/games')

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

    def test_get_all_games(self):
        game_id1 = self._create_game()
        game_id2 = self._create_game()
        resp = self.app.get(f'/games')
        self._check_ok_resp(resp)
        self.assertEqual(len(resp.json), 2)
        self.assertIsInstance(resp.json, list)
        self.assertEqual(resp.json[0]['id'], game_id1)
        self.assertEqual(resp.json[1]['id'], game_id2)

    def test_delete_game(self):
        game_id = self._create_game()
        resp = self.app.delete(f'/game/{game_id}')
        self.assertEqual(resp.status_code, 204)

    def test_delete_all_games(self):
        game_id1 = self._create_game()
        game_id2 = self._create_game()
        resp = self.app.delete(f'/games')
        self.assertEqual(resp.status_code, 204)

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
