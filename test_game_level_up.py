import io
from unittest import TestCase
from unittest.mock import patch
from game import level_up

class LevelUp(TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_level_up_1_to_2(self, printed):
        game_info = {
            "Player": {
                "Exp": 151,
                "Level": 1,
                "MaxHP": 100
            },
            "Messages": {
                "LEVELUP": ["When you killed !ENEMY, you leveled up."]
            },
            "Replacements": {

            }
        }
        enemy = {
            "Name": "Test Enemy"
        }
        expected = "When you killed Test Enemy, you leveled up."
        level_up(game_info, enemy)
        actual = printed.getvalue()
        self.assertIn(expected, actual)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_level_up_2_to_3(self, printed):
        game_info = {
            "Player": {
                "Exp": 301,
                "Level": 2,
                "MaxHP": 150
            },
            "Messages": {
                "LEVELUP": ["When you killed !ENEMY, you leveled up."]
            },
            "Replacements": {

            }
        }
        enemy = {
            "Name": "Test Enemy"
        }
        expected = "When you killed Test Enemy, you leveled up."
        level_up(game_info, enemy)
        actual = printed.getvalue()
        self.assertIn(expected, actual)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_level_up_invalid(self, printed):
        game_info = {
            "Player": {
                "Exp": 100,
                "Level": 1,
                "MaxHP": 100
            },
            "Messages": {
                "LEVELUP": ["When you killed !ENEMY, you leveled up."]
            },
            "Replacements": {

            }
        }
        enemy = {
            "Name": "Test Enemy"
        }
        expected = ""
        level_up(game_info, enemy)
        actual = printed.getvalue()
        self.assertIn(expected, actual)