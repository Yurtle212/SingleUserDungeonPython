from unittest import TestCase
from unittest.mock import patch
import io
from game import print_items

class TestPrintItems(TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_items_item(self, printed):
        game_info = {
            "Items": {
                "TestItem": {
                    "Room Description": ["Test Description."]
                }
            }
        }
        expected = "Test Description.\n"
        print_items("TestItem", game_info)
        actual = printed.getvalue()
        self.assertEqual(expected, actual)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_items_item(self, printed):
        game_info = {
            "Items": {
                "TestItem": {
                    "Room Description": ["Test Description."]
                }
            }
        }
        expected = ""
        print_items("", game_info)
        actual = printed.getvalue()
        self.assertEqual(expected, actual)
