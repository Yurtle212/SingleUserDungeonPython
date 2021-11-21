import io
from unittest import TestCase
from unittest.mock import patch
from game import regenerate_health

class RegenerateHealth(TestCase):
    def test_regenerate_health_far_under_max(self):
        game_info = {
            "Player": {
                "HP": 5,
                "MaxHP": 100
            }
        }
        expected = {
            "Player": {
                "HP": 10,
                "MaxHP": 100
            }
        }
        regenerate_health(game_info)
        self.assertEqual(game_info, expected)

    def test_regenerate_health_5_under_max(self):
        game_info = {
            "Player": {
                "HP": 95,
                "MaxHP": 100
            }
        }
        expected = {
            "Player": {
                "HP": 100,
                "MaxHP": 100
            }
        }
        regenerate_health(game_info)
        self.assertEqual(game_info, expected)

    def test_regenerate_health_barely_under_max(self):
        game_info = {
            "Player": {
                "HP": 98,
                "MaxHP": 100
            }
        }
        expected = {
            "Player": {
                "HP": 100,
                "MaxHP": 100
            }
        }
        regenerate_health(game_info)
        self.assertEqual(game_info, expected)

    def test_regenerate_health_at_max(self):
        game_info = {
            "Player": {
                "HP": 100,
                "MaxHP": 100
            }
        }
        expected = {
            "Player": {
                "HP": 100,
                "MaxHP": 100
            }
        }
        regenerate_health(game_info)
        self.assertEqual(game_info, expected)