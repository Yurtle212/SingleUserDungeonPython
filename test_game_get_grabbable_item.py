from unittest import TestCase
from unittest.mock import patch
from game import get_grabbable_item

class GetGrabbableItem(TestCase):
    def test_get_grabbable_item_item(self):
        game_info = {
            "Map": {
                "Game Map": {
                    0: {
                        0: {
                            "Item": "testItem"
                        }
                    }
                }
            }
        }
        expected = 'Take testItem'
        actual = get_grabbable_item(game_info, [0, 0])
        self.assertEqual(expected, actual)

    def test_get_grabbable_item_no_item(self):
        game_info = {
            "Map": {
                "Game Map": {
                    0: {
                        0: {
                            "Item": ""
                        }
                    }
                }
            }
        }
        expected = ''
        actual = get_grabbable_item(game_info, [0, 0])
        self.assertEqual(expected, actual)
