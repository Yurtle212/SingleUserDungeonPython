from unittest import TestCase
from unittest.mock import patch
from game import get_message

class GetMessage(TestCase):
    # I'm counting this as a unit test for replace_message() too, since one is never found without the other.
    def test_get_message_no_replacements(self):
        path = "Messages.TEST"
        game_info = {
            "Messages": {
                "TEST": ["This is a test."]
            },
            "Replacements": {

            }
        }
        expected = "This is a test."
        actual = get_message(path, game_info)
        self.assertEqual(expected, actual)

    def test_get_message_1_replacement(self):
        path = "Messages.TEST"
        game_info = {
            "Messages": {
                "TEST": ["This word has been !REPLACE."]
            },
            "Replacements": {
                "!REPLACE": "Test.thing"
            },
            "Test": {
                "thing": "replaced"
            }
        }
        expected = "This word has been replaced."
        actual = get_message(path, game_info)
        self.assertEqual(expected, actual)

    def test_get_message_multiple_replacements(self):
        path = "Messages.TEST"
        game_info = {
            "Messages": {
                "TEST": ["This word has been !FIRST. So has !SECOND one. When will !SECOND end?"]
            },
            "Replacements": {
                "!FIRST": "Test.first",
                "!SECOND": "Test.second"
            },
            "Test": {
                "first": "replaced",
                "second": "this"
            }
        }
        expected = "This word has been replaced. So has this one. When will this end?"
        actual = get_message(path, game_info)
        self.assertEqual(expected, actual)