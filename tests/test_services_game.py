from unittest.case import TestCase

from models.games import Game
from models.players import Player
from services.play import start_game, do_move


class TestGameServices(TestCase):

    def setUp(self):
        self.player1 = Player("name1", "white")
        self.player2 = Player("name2", "black")

    def test_initiate_game(self):
        game = start_game(self.player1, self.player2)
        self.assertIsInstance(game, Game)
        self.assertEqual(len(game._moves), 0)
        self.assertEqual(game._next_colour, "white")

    def test_do_first_move(self):
        game = start_game(self.player1, self.player2)
        self.assertEqual(len(game._moves), 0)
        self.assertEqual(game._next_colour, "white")

        game = do_move(self.player1, game, "e2", "e4")
        self.assertIsInstance(game, Game)
        self.assertEqual(len(game._moves), 1)
        self.assertEqual(game._next_colour, "black")

    def test_counter_move(self):
        game = start_game(self.player1, self.player2)
        game = do_move(self.player1, game, "e2", "e4")

        self.assertEqual(game._next_colour, "black")
        game = do_move(self.player2, game, "d7", "d5")
        self.assertEqual(len(game._moves), 2)
        self.assertEqual(game._next_colour, "white")

    def test_kill_with_pawn(self):
        game = start_game(self.player1, self.player2)
        game = do_move(self.player1, game, "e2", "e4")
        game = do_move(self.player2, game, "d7", "d5")
        game = do_move(self.player1, game, "e4", "d5")

    def test_double_turn(self):
        """
        Invalid Turn: White two moves in a row
        """
        game = start_game(self.player1, self.player2)
        game = do_move(self.player1, game, "e2", "e4")

        with self.assertRaises(Exception):
            do_move(self.player1, game, "e4", "e5")

    def test_non_valid_move(self):
        """
        Invalid Move
        """
        game = start_game(self.player1, self.player2)
        with self.assertRaises(Exception):
            do_move(self.player1, game, "e2", "e5")

    def test_move_rook_through_piece(self):
        game = start_game(self.player1, self.player2)
        with self.assertRaises(Exception):
            do_move(self.player1, game, "a1", "a4")
