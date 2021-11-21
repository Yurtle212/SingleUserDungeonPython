from unittest import TestCase
from game import enemy_flee

class TestEnemyFlee(TestCase):
    def test_enemy_flee_multiple_enemies(self):
        current_battle = {
            "TestEnemy": {
                "Name": "TestEnemy",
                "TEXT": {
                    "FLEE": ["Test Flee"]
                },
                "Exp": 5
            },
            "TestEnemy2": {
                "Name": "TestEnemy2",
                "TEXT": {
                    "FLEE": ["Test Flee"]
                },
                "Exp": 5
            }
        }
        game_info = {
            "Enemies": {
                "TestEnemy": {
                    "Name": "TestEnemy",
                    "TEXT": {
                        "FLEE": ["Test Flee"]
                    },
                    "Exp": 5
                },
                "TestEnemy2": {
                    "Name": "TestEnemy2",
                    "TEXT": {
                        "FLEE": ["Test Flee"]
                    },
                    "Exp": 5
                }
            },
            "Player": {
                "Exp": 0
            },
            "Replacements": {

            }
        }
        expectedCB = {
            "TestEnemy2": {
                "Name": "TestEnemy2",
                "TEXT": {
                    "FLEE": ["Test Flee"]
                },
                "Exp": 5
            }
        }
        expectedGI = {
            "Enemies": {
                "TestEnemy": {
                    "Name": "TestEnemy",
                    "TEXT": {
                        "FLEE": ["Test Flee"]
                    },
                    "Exp": 5
                },
                "TestEnemy2": {
                    "Name": "TestEnemy2",
                    "TEXT": {
                        "FLEE": ["Test Flee"]
                    },
                    "Exp": 5
                }
            },
            "Player": {
                "Exp": 5
            },
            "Replacements": {

            }
        }
        enemy_flee(game_info, current_battle, "TestEnemy")
        current_battle_equal = expectedCB == current_battle
        game_info_equal = expectedGI == game_info
        self.assertTrue(current_battle_equal and game_info_equal)

    def test_enemy_flee_single_enemy(self):
        current_battle = {
            "TestEnemy": {
                "Name": "TestEnemy",
                "TEXT": {
                    "FLEE": ["Test Flee"]
                },
                "Exp": 5
            }
        }
        game_info = {
            "Enemies": {
                "TestEnemy": {
                    "Name": "TestEnemy",
                    "TEXT": {
                        "FLEE": ["Test Flee"]
                    },
                    "Exp": 5
                },
                "TestEnemy2": {
                    "Name": "TestEnemy2",
                    "TEXT": {
                        "FLEE": ["Test Flee"]
                    },
                    "Exp": 5
                }
            },
            "Player": {
                "Exp": 0
            },
            "Replacements": {

            }
        }
        expectedCB = {

        }
        expectedGI = {
            "Enemies": {
                "TestEnemy": {
                    "Name": "TestEnemy",
                    "TEXT": {
                        "FLEE": ["Test Flee"]
                    },
                    "Exp": 5
                },
                "TestEnemy2": {
                    "Name": "TestEnemy2",
                    "TEXT": {
                        "FLEE": ["Test Flee"]
                    },
                    "Exp": 5
                }
            },
            "Player": {
                "Exp": 5
            },
            "Replacements": {

            }
        }
        enemy_flee(game_info, current_battle, "TestEnemy")
        current_battle_equal = expectedCB == current_battle
        game_info_equal = expectedGI == game_info
        self.assertTrue(current_battle_equal and game_info_equal)
