from unittest import TestCase
from game import interperet_input

class TestInterperetInput(TestCase):
    def test_interperet_input_one_context_multiple_possible_valid_string(self):
        game_info = {
            "Inputs": {
                "MapView": {
                    "TestInput1Map": ["ti1cm_1", "ti1cm_2"],
                    "TestInput2Map": ["ti2cm_1", "ti2cm_2"]
                }
            }
        }
        player_input = "ti2cm_1"
        expected = ("TestInput2Map", "ti2cm_1")
        numeric = [('0', "TestInput1Map"), ('1', 'TestInput2Map')]
        actual = interperet_input(player_input, False, game_info, numeric)
        self.assertEqual(expected, actual)

    def test_interperet_input_one_context_multiple_possible_valid_string_not_first(self):
        game_info = {
            "Inputs": {
                "MapView": {
                    "TestInput1Map": ["ti1cm_1", "ti1cm_2"],
                    "TestInput2Map": ["ti2cm_1", "ti2cm_2"]
                }
            }
        }
        player_input = "ti2cm_2"
        expected = ("TestInput2Map", "ti2cm_2")
        numeric = [('0', "TestInput1Map"), ('1', 'TestInput2Map')]
        actual = interperet_input(player_input, False, game_info, numeric)
        self.assertEqual(expected, actual)

    def test_interperet_input_one_context_multiple_possible_valid_number(self):
        game_info = {
            "Inputs": {
                "MapView": {
                    "TestInput1Map": ["ti1cm_1", "ti1cm_2", "testinput1map"],
                    "TestInput2Map": ["ti2cm_1", "ti2cm_2", "testinput2map"]
                }
            }
        }
        player_input = "0"
        expected = ("TestInput1Map", "testinput1map")
        numeric = [('0', "Testinput1map"), ('1', 'Testinput2map')]
        actual = interperet_input(player_input, False, game_info, numeric)
        self.assertEqual(expected, actual)

    def test_interperet_input_one_context_multiple_possible_valid_number_not_first(self):
        game_info = {
            "Inputs": {
                "MapView": {
                    "TestInput1Map": ["ti1cm_1", "ti1cm_2", "testinput1map"],
                    "TestInput2Map": ["ti2cm_1", "ti2cm_2", "testinput2map"]
                }
            }
        }
        player_input = "1"
        expected = ("TestInput2Map", "testinput2map")
        numeric = [('0', "Testinput1map"), ('1', 'Testinput2map')]
        actual = interperet_input(player_input, False, game_info, numeric)
        self.assertEqual(expected, actual)

    def test_interperet_input_one_context_multiple_possible_invalid_string(self):
        game_info = {
            "Inputs": {
                "MapView": {
                    "TestInput1Map": ["ti1cm_1", "ti1cm_2", "testinput1map"],
                    "TestInput2Map": ["ti2cm_1", "ti2cm_2", "testinput2map"]
                }
            }
        }
        player_input = "bruh"
        expected = (None, "bruh")
        numeric = [('0', "Testinput1map"), ('1', 'Testinput2map')]
        actual = interperet_input(player_input, False, game_info, numeric)
        self.assertEqual(expected, actual)

    def test_interperet_input_one_context_multiple_possible_invalid_number(self):
        game_info = {
            "Inputs": {
                "MapView": {
                    "TestInput1Map": ["ti1cm_1", "ti1cm_2", "testinput1map"],
                    "TestInput2Map": ["ti2cm_1", "ti2cm_2", "testinput2map"]
                }
            }
        }
        player_input = "5"
        expected = (None, "5")
        numeric = [('0', "Testinput1map"), ('1', 'Testinput2map')]
        actual = interperet_input(player_input, False, game_info, numeric)
        self.assertEqual(expected, actual)