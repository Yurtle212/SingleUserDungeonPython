from unittest import TestCase
from unittest.mock import patch
from game import check_for_win, load_game_map

class CheckForWin(TestCase):
    def test_check_for_win_corner(self):
        game_map = load_game_map()
        player_position = [0, 0]
        expected = False
        actual = check_for_win(game_map, player_position)
        self.assertEqual(expected, actual)

    def test_check_for_win_middle(self):
        game_map = load_game_map()
        player_position = [5, 5]
        expected = False
        actual = check_for_win(game_map, player_position)
        self.assertEqual(expected, actual)

    def test_check_for_win_outside_left(self):
        game_map = load_game_map()
        player_position = [-1, 0]
        expected = True
        actual = check_for_win(game_map, player_position)
        self.assertEqual(expected, actual)

    def test_check_for_win_outside_right(self):
        game_map = load_game_map()
        player_position = [999, 0]
        expected = True
        actual = check_for_win(game_map, player_position)
        self.assertEqual(expected, actual)

    def test_check_for_win_outside_up(self):
        game_map = load_game_map()
        player_position = [0, -1]
        expected = True
        actual = check_for_win(game_map, player_position)
        self.assertEqual(expected, actual)

    def test_check_for_win_outside_bottom(self):
        game_map = load_game_map()
        player_position = [0, 999]
        expected = True
        actual = check_for_win(game_map, player_position)
        self.assertEqual(expected, actual)
