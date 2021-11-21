from unittest import TestCase
from unittest.mock import patch
from game import list_of_tuples_to_dictionary

class TestTuplesToDictionary(TestCase):
    def test_list_of_tuples_to_dictionary_multiple_tuples(self):
        input_list = [(0, 1), (1, 2), (2, 3)]
        expected = {
            0: 1,
            1: 2,
            2: 3
        }
        actual = list_of_tuples_to_dictionary(input_list)
        self.assertEqual(expected, actual)

    def test_list_of_tuples_to_dictionary_single_tuple(self):
        input_list = [(0, 1)]
        expected = {
            0: 1
        }
        actual = list_of_tuples_to_dictionary(input_list)
        self.assertEqual(expected, actual)

    def test_list_of_tuples_to_dictionary_no_tuples(self):
        input_list = []
        expected = {

        }
        actual = list_of_tuples_to_dictionary(input_list)
        self.assertEqual(expected, actual)
