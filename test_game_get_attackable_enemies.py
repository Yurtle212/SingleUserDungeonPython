import itertools
from unittest import TestCase
from unittest.mock import patch
from game import get_attackable_enemies


class GetAttackableEnemies(TestCase):
    def test_get_attackable_enemies_multiple(self):
        enemies = {
            "Enemy 1": {
                "Name": "Enemy 1"
            },
            "Enemy 2": {
                "Name": "Enemy 2"
            }
        }
        iterator = itertools.count()
        expected = [('0', "Attack Enemy 1"), ('1', "Attack Enemy 2")]
        actual = get_attackable_enemies(enemies, iterator)
        self.assertEqual(expected, actual)

    def test_get_attackable_enemies_one(self):
        enemies = {
            "Enemy 1": {
                "Name": "Enemy 1"
            }
        }
        iterator = itertools.count()
        expected = [('0', "Attack Enemy 1")]
        actual = get_attackable_enemies(enemies, iterator)
        self.assertEqual(expected, actual)

    def test_get_attackable_enemies_none(self):
        enemies = {}
        iterator = itertools.count()
        expected = []
        actual = get_attackable_enemies(enemies, iterator)
        self.assertEqual(expected, actual)