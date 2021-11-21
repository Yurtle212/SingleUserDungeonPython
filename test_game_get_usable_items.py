from unittest import TestCase
from unittest.mock import patch
from game import get_usable_items

class GetUsableItems(TestCase):
    def test_get_usable_items_multiple_items(self):
        game_info = {
            "Player": {
                "Inventory": {
                    "Item 1": 1,
                    "Item 2": 1
                }
            }
        }
        expected = ["Use Item 1", "Use Item 2"]
        actual = get_usable_items(game_info)
        self.assertEqual(expected, actual)

    def test_get_usable_items_one_item(self):
        game_info = {
            "Player": {
                "Inventory": {
                    "Item 1": 1
                }
            }
        }
        expected = ["Use Item 1"]
        actual = get_usable_items(game_info)
        self.assertEqual(expected, actual)

    def test_get_usable_items_no_items(self):
        game_info = {
            "Player": {
                "Inventory": {}
            }
        }
        expected = []
        actual = get_usable_items(game_info)
        self.assertEqual(expected, actual)