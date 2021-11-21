from unittest import TestCase
from unittest.mock import patch
from game import add_to_inventory

class AddToInventory(TestCase):
    def test_add_to_inventory_new(self):
        game_info = {
            "Player": {
                "Inventory": {

                }
            }
        }
        expected = {
            "Player": {
                "Inventory": {
                    "TestItem": 1
                }
            }
        }
        add_to_inventory(game_info, "TestItem")
        self.assertEqual(expected, game_info)

    def test_add_to_inventory_existing(self):
        game_info = {
            "Player": {
                "Inventory": {
                    "TestItem": 1
                }
            }
        }
        expected = {
            "Player": {
                "Inventory": {
                    "TestItem": 2
                }
            }
        }
        add_to_inventory(game_info, "TestItem")
        self.assertEqual(expected, game_info)