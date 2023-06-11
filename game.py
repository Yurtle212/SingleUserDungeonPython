"""
Your name: Leslie Butler

All of your code must go in this file.
"""
import json
import random
import math
import sys
import time
import itertools


def load_game_info(path):
    """
    Load gameInfo.json into a python dictionary.

    :return: Dictionary
    :precondition: gameInfo.json exists and is formatted correctly.
    :postcondition: Will return gameInfo.json as a python dictionary.
    """
    with open(path, "r", encoding="utf8") as file:
        output = file.read()
        final_json = json.loads(output)
        return final_json


def load_game_map(path):
    """
    Load the gamemap into a 2d list.

    :return: 2d list
    :precondition: map.txt exists and is a rectangle with a blank line at the end.
    :postcondition: Will return map.txt as a 2d list of all the characters.
    """
    with open(path, "r", encoding="utf8") as file:
        output = file.readlines()
        for i in range(len(output)):
            output[i] = list(output[i])[:-1]

        final_map = []
        for i in range(len(output)):
            row = []
            for pos in range(len(output[i])):
                row.append(output[i][pos])
            final_map.append(row)
        return final_map


def populate_game_map(game_info, game_map, player_position):
    """
    Populates the game map with enemies and items.

    :param game_info: game_info dictionary.
    :param game_map: game_map list.
    :param player_position: player_position list.
    :return: game_info dictionary.
    :precondition: game_info, game_map, player_position are formatted correctly.
    :postcondition: Will return the game_info dictionary updated to have items and enemies in rooms.
    """
    for row in range(len(game_map)):
        game_info["Map"]["Game Map"][row] = {}
        for room in range(len(game_map[row])):
            game_info["Map"]["Game Map"][row][room] = {}
            game_info["Map"]["Game Map"][row][room]["Piece"] = game_map[row][room]
            game_info["Map"]["Game Map"][row][room]["Enemies"] = []
            game_info["Map"]["Game Map"][row][room]["Description"] = random.choice(game_info["Map"]["Descriptions"])
            populate_enemies(game_info, row, room, player_position, game_map)
            populate_items(game_info, row, room, player_position)
    return game_info


def populate_enemies(game_info, row, room, player_position, game_map):
    """
    Will decide what enemies (if any) will be placed in the room.

    :param game_info: game_info dictionary
    :param row: int
    :param room: int
    :param player_position: player_position list
    :param game_map: game_map list
    :return: None
    :precondition: game_info, player_position, game_map are formatted correctly. row and room are within the bounds of the map.
    :postcondition: Will update the game_info dictionary with the enemies in the room.
    """
    random_enemies = game_info["Map"]["Pieces"][game_map[row][room]]["Enemies"] == ["Random"]
    boss_enemy = game_info["Map"]["Pieces"][game_map[row][room]]["Enemies"] == ["Boss"]
    if random_enemies and random.randrange(0, 100) < 20 and [row, room] != player_position:
        for i in range(random.randrange(1, 3)):
            random_enemy = random.choice(list(game_info["Enemies"].keys()))
            while game_info["Enemies"][random_enemy]["Boss"] == "True":
                random_enemy = random.choice(list(game_info["Enemies"].keys()))
            game_info["Map"]["Game Map"][row][room]["Enemies"].append(random_enemy)
    elif boss_enemy:
        boss = random.choice(list(game_info["Enemies"].keys()))
        while game_info["Enemies"][boss]["Boss"] == "False":
            boss = random.choice(list(game_info["Enemies"].keys()))
        game_info["Map"]["Game Map"][row][room]["Enemies"].append(boss)


def populate_items(game_info, row, room, player_position):
    """
    Will decide what items (if any) will be placed in the room.

    :param game_info: game_info dictionary
    :param row: int
    :param room: int
    :param player_position: player_position list
    :return: None
    :precondition: game_info and player_position are formatted correctly. row and room are within the bounds of the map.
    """
    game_info["Map"]["Game Map"][row][room]["Item"] = ''
    item_can_place = (random.randrange(0, 100) < 40 or [row, room] == player_position)
    if game_info["Map"]["Game Map"][row][room]["Piece"] != "░" and item_can_place:
        random_item = random.choice(list(game_info["Items"].keys()))
        item_is_not_unique = game_info["Items"][random_item]["Unique"] != "True"
        if [row, room] == player_position:
            game_info["Map"]["Game Map"][row][room]["Item"] = "Medkit"
        elif item_is_not_unique or game_info["Items"][random_item]["Used"] == "False":
            game_info["Map"]["Game Map"][row][room]["Item"] = random_item
            game_info["Items"][random_item]["Used"] = "True"


def print_map(game_map, player_position, game_info):
    """
    Prints the map to the screen so the player can see it.

    :param game_map: game_map list
    :param player_position: player_position list
    :param game_info: game_info dictionary
    :return: None
    :precondition: game_map, player_position, game_info are formatted correctly.
    :postcondition: Will print the map to the terminal window.
    """
    final_map = ""
    view_range = [2, 4]  # Vertical, Horizontal
    for row in range(len(game_map)):
        if abs(player_position[0] - row) <= view_range[0]:  # Check vertical distance
            for room in range(len(game_map[row])):
                if abs(player_position[1] - room) <= view_range[1]:  # Check horizontal distance
                    final_map += add_piece(game_info, player_position, row, room, game_map)
            final_map += "\n"
    print(final_map)
    print('(n)orth, (s)outh, (e)ast, (w)est to move')
    print(game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Description"])
    print_items(game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Item"], game_info)


def add_piece(game_info, player_position, row, room, game_map):
    """
    Decides how each piece of the map will look when printed.

    :param game_info: game_info dictionary
    :param player_position: player_position list
    :param row: int
    :param room: int
    :param game_map: game_map list
    :return: string
    :precondition: game_info, player_position, game_map are formatted correctly. row, room are within the bounds of the map.
    :postcondition: Will return the map piece with correct formatting (colouring)
    """
    final_piece = ''
    if [row, room] == player_position:
        final_piece = f'\033[{game_info["Colours"]["Player"]}m' + game_map[row][
            room] + f'\033[{game_info["Colours"]["Normal"]}m'
    elif len(game_info["Map"]["Game Map"][row][room]["Enemies"]) > 0:
        final_piece = f'\033[{game_info["Colours"]["Enemy"]}m' + game_map[row][
            room] + f'\033[{game_info["Colours"]["Normal"]}m'
    else:
        final_piece = f'\033[{game_info["Colours"][game_info["Map"]["Pieces"][game_map[row][room]]["Colour"]]}m' + \
                     game_map[row][room] + f'\033[{game_info["Colours"]["Normal"]}m'
    return final_piece


def print_items(room_item, game_info):
    """
    Print the item in the room.

    :param room_item: item name string
    :param game_info: game_info dictionary
    :return: None
    :precondition: item name is a key in the game_info dictionary. game_info is formatted correctly.
    :postcondition: Prints the room description of the item to the terminal window.
    """
    if room_item != "":
        print(random.choice(game_info["Items"][room_item]["Room Description"]))


def check_level(game_map, new_position, game_info):
    """
    Verifies the player is allowed to pass the room.

    :param game_map: game_map list
    :param new_position: new_position list
    :param game_info: game_info dictionary
    :return: Bool
    :precondition: game_map, new_position, game_info are formatted correctly. new_position is within the bounds of the map.
    :postcondition: Will return True if the player's level is high enough to pass. False otherwise, printing a message to the player.
    """
    if game_map[new_position[0]][new_position[1]] == "2":
        if int(game_info["Player"]["Level"]) >= 2:
            return True
    elif game_map[new_position[0]][new_position[1]] == "3":
        if int(game_info["Player"]["Level"]) >= 3:
            return True
    else:
        return True
    print(get_message("Messages.LEVELMESSAGE", game_info))
    time.sleep(2)
    return False


def move_player(game_map, player_position, move_direction, game_info, last_player_position):
    """
    Changes the player's position.

    :param game_map: game_map list
    :param player_position: player_position list
    :param move_direction: move_direction string
    :param game_info: game_info dictionary
    :param last_player_position: last_player_position list
    :return: player_position list, last_player_position list
    :precondition: All params are formatted correctly.
    :postcondition: Will return the player's new position, as well as their old position. Both as lists.
    """
    possible_directions = game_info["Map"]["Pieces"][game_map[player_position[0]][player_position[1]]]["Dir"]
    if move_direction in possible_directions:
        last_player_position = player_position.copy()
        if move_direction.lower() == "north" or move_direction.lower() == "n":
            if check_level(game_map, [player_position[0] - 1, player_position[1]], game_info):
                player_position[0] = player_position[0] - 1
        elif move_direction.lower() == "south" or move_direction.lower() == "s":
            if check_level(game_map, [player_position[0] + 1, player_position[1]], game_info):
                player_position[0] = player_position[0] + 1
        elif move_direction.lower() == "east" or move_direction.lower() == "e":
            if check_level(game_map, [player_position[0], player_position[1] + 1], game_info):
                player_position[1] = player_position[1] + 1
        elif move_direction.lower() == "west" or move_direction.lower() == "w":
            if check_level(game_map, [player_position[0], player_position[1] - 1], game_info):
                player_position[1] = player_position[1] - 1
        regenerate_health(game_info)
    return player_position, last_player_position


def initiate_battle(game_info, player_position, last_player_position):
    """
    Will initialize a battle and start the battle loop, if an enemy is present in the room.

    :param game_info: game_info dictionary
    :param player_position: player_position list
    :param last_player_position: last_player_position list
    :return: player_position list
    :precondition: All params are formatted correctly. player_position and last_player_position are within the bounds of the map.
    :postcondition: returns the player_position if the battle is won or no enemies. Otherwise will return last_player_position. game_info will have been updated.
    """
    enemies = game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"]
    current_battle = {}
    battle_message = "In the room you find "
    for enemy in range(len(enemies)):
        if type(game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"]) is not dict:
            battle_message += add_enemy(current_battle, game_info, enemies, enemy)
        else:
            current_battle = game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"]
            battle_message = "So, you've come back to finish the fight. They are still......"
            break
    if len(current_battle) > 0:
        print(battle_message[:-6] + " blocking your path.")
        return battle(game_info, current_battle, player_position, last_player_position)
    return player_position


def add_enemy(current_battle, game_info, enemies, enemy):
    """
    Adds an enemy to the battle.

    :param current_battle: current_battle dictionary
    :param game_info: game_info dictionary
    :param enemies: enemies list
    :param enemy: enemy dictionary
    :return: string
    :precondition: Params are formatted correctly.
    :postcondition: Will edit current_battle to contain a new enemy. Will return a string for the battle_message.
    """
    current_battle[enemy] = game_info["Enemies"][enemies[enemy]].copy()
    if current_battle[enemy]["Vengeful"] == "True":
        current_battle[enemy]["Atk"] = 0
    if current_battle[enemy]["Speed"] > game_info["Player"]["Speed"]:
        print(get_message("Messages.SPEED_PRE_ATTACK", game_info).replace("!ENEMY", current_battle[enemy]["Name"]))
        attacked(game_info, current_battle[enemy], False)
    return f"an {current_battle[enemy]['Name']}, and "


def battle(game_info, current_battle, player_position, last_player_position):
    """
    Main battle loop.

    :param game_info: game_info dictionary
    :param current_battle: current_battle dictionary
    :param player_position: player_position list
    :param last_player_position: last_player_position list
    :return: list
    :precondition: All params are formatted correctly.
    :postcondition: Will update the game_info dictionary, and return the player's position.
    """
    while len(current_battle) > 0:
        time.sleep(1)
        if game_info['Player']['HP'] <= 0:
            time.sleep(1)
            die(game_info)
        has_attacked = False
        numbered_input = get_possible_moves(game_info, "Battle", player_position, current_battle)
        player_input = input(get_message("Messages.BATTLEPROMPT", game_info))
        input_type, player_input = interperet_input(player_input, True, game_info, numbered_input)
        if input_type == "Attack":
            for enemy in current_battle:
                if ((len(player_input.split(" ")) > 1) and (
                        player_input.split(" ")[1] in current_battle[enemy]["Name"])) or (
                        len(player_input.split(" ")) == 1):
                    current_battle[enemy] = attack(game_info, current_battle[enemy])
                    has_attacked = True
                    kill_enemy(game_info, current_battle, enemy)
                    break
            if not has_attacked:
                print("I can't find that enemy.")
        elif input_type == "Inventory":
            display_inventory(game_info)
        elif input_type == "Info":
            check_enemies(current_battle)
        elif input_type == "Flee":
            flee_from_battle(current_battle, game_info)
            game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"] = current_battle
            return last_player_position
        elif input_type == "Use":
            item = player_input.split(" ")[1]
            use_item(game_info, item)
        elif input_type == "Pass":
            has_attacked = True
        elif input_type == "Quit":
            quit()
        if has_attacked:
            for enemy in current_battle.copy():
                if random.randrange(0, 100) < 25 and current_battle[enemy]["Boss"] == "False":
                    enemy_flee(game_info, current_battle, enemy)
                    continue
                attacked(game_info, current_battle[enemy], False)
    game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"] = []
    return player_position


def kill_enemy(game_info, current_battle, enemy):
    """
    Kills an enemy and removes it from the battle.

    :param game_info: game_info dictionary
    :param current_battle: current_battle dictionary
    :param enemy: enemy dictionary
    :return: None
    :precondition: all params are formatted correctly.
    :postcondition: Enemy will be removed from the battle after printing the death message.
    """
    if current_battle[enemy]["HP"] <= 0:
        game_info['Player']['Kills'] += 1
        game_info['Player']['Exp'] += current_battle[enemy]["Exp"]
        print(get_message(f'Enemies.{current_battle[enemy]["Name"]}.TEXT.DEATH', game_info))
        level_up(game_info, current_battle[enemy])
        del (current_battle[enemy])


def check_enemies(current_battle):
    """
    Prints the stats of the enemies.

    :param current_battle: current_battle dictionary
    :return: None
    :precondition: current_battle is formatted correctly
    :postcondition: prints the stats of all the enemies in the current battle.
    """
    ignore_stats = ["TEXT", "Exp", "Boss"]
    for enemy in current_battle:
        print("\n")
        for key, value in current_battle[enemy].items():
            if key not in ignore_stats:
                print(key + ": " + str(value))


def enemy_flee(game_info, current_battle, enemy):
    """
    Make the enemy flee from battle.

    :param game_info: game_info dictionary
    :param current_battle: current_battle dictionary.
    :param enemy: string
    :return: None
    :precondition: all params are formatted correctly.
    :postcondition: Will print the flee message, and remove the enemy from the battle.
    """
    print(get_message(f'Enemies.{current_battle[enemy]["Name"]}.TEXT.FLEE', game_info))
    time.sleep(1)
    game_info['Player']['Exp'] += current_battle[enemy]["Exp"]
    level_up(game_info, current_battle[enemy])
    del(current_battle[enemy])


def flee_from_battle(current_battle, game_info):
    """
    Exit from the current battle before winning.

    :param current_battle: current_battle dictionary.
    :param game_info: game_info dictionary.
    :return: None
    :precondition: all params are formatted correctly.
    :postcondition: Decides whether the any enemies will attack you as you flee.
    """
    for enemy in current_battle:
        if random.randrange(0, 100) < 20:
            attacked(game_info, current_battle[enemy], True)
            time.sleep(1)


def display_inventory(game_info):
    """
    Print all the stuff in your inventory to the screen.

    :param game_info: game_info dictionary.
    :return: None
    :precondition: game_info is formatted correctly
    :postcondition: Will print all the stuff in your inventory to the terminal window.
    """
    print("\nItem \t\t| Count \t| \tDescription")
    for item, count in game_info["Player"]["Inventory"].items():
        print(item, "\t\t", count, "\t\t\t", game_info["Items"][item]["Description"])
    print('\n')
    time.sleep(1)


def attack(game_info, enemy):
    """
    Attack an enemy.

    :param game_info: game_info dictionary
    :param enemy: enemy dictionary
    :return: enemy dictionary
    :precondition: All params are formatted correctly.
    :postcondition: Will update the game_info dictionary, and return the changed enemy dictionary.
    """
    time.sleep(1)
    random_number = random.randrange(0, 100)
    if random_number >= 20:
        damage = math.ceil((game_info["Player"]["Atk"] * 5) * (random_number / 100))
        damage -= enemy["Def"]
        if enemy["Vengeful"] == "True":
            enemy["Atk"] = game_info["Enemies"][enemy["Name"]]["Atk"]
        if damage <= 0:
            print(get_message(f'Enemies.{enemy["Name"]}.TEXT.DEF', game_info))
            return enemy
        enemy["HP"] -= damage
        print(get_message(f'Enemies.{enemy["Name"]}.TEXT.HIT', game_info).replace("!DMG", str(damage)))
    else:
        print(get_message(f'Enemies.{enemy["Name"]}.TEXT.MISS', game_info))
    return enemy


def attacked(game_info, enemy, player_fleeing):
    """
    Enemy attack the player.

    :param game_info: game_info dictionary
    :param enemy: enemy dictionary
    :param player_fleeing: bool
    :return: None
    :precondition: all params are formatted correctly.
    :postcondition: game_info dictionary will be updated.
    """
    time.sleep(1)
    random_number = random.randrange(0, 100)
    if random_number >= 20:
        damage = math.ceil((enemy["Atk"] * 5) * (random_number / 100))
        damage -= game_info["Player"]["Def"]
        if damage <= 0:
            print(get_message(f"Enemies.{enemy['Name']}.TEXT.ATKDEF", game_info))
            return enemy
        game_info["Player"]["HP"] -= damage
        if player_fleeing:
            print(get_message(f"Enemies.{enemy['Name']}.TEXT.FLEEATK", game_info).replace("!DMG", str(damage)))
        else:
            print(get_message(f"Enemies.{enemy['Name']}.TEXT.ATKHIT", game_info).replace("!DMG", str(damage)))
    else:
        print(get_message(f"Enemies.{enemy['Name']}.TEXT.ATKMISS", game_info))


def interperet_input(player_input, in_battle, game_info, numbered_input):
    """
    Interpret the player's input.

    :param player_input: string
    :param in_battle: bool
    :param game_info: game_info dictionary
    :param numbered_input: list of tuples with 2 values
    :return: string, string
    :precondition: all params are formatted correctly.
    :postcondition: Will return the type of the input, as well as the full input string.
    """
    if player_input.isnumeric():
        numeric_inputs = list_of_tuples_to_dictionary(numbered_input)
        if player_input in numeric_inputs:
            player_input = list_of_tuples_to_dictionary(numbered_input)[player_input]
        player_input = player_input[0].lower() + player_input[1:]
    if in_battle:
        for key, value in game_info["Inputs"]["Battle"].items():
            if player_input.split(" ")[0] in value:
                return key, player_input
    else:
        for key, value in game_info["Inputs"]["MapView"].items():
            if player_input.split(" ")[0] in value:
                return key, player_input
    return None, player_input


def list_of_tuples_to_dictionary(input_list):
    """
    Convert a list of tuples to a dictionary.

    :param input_list: list of tuples with 2 values.
    :return: Dictionary
    :precondition: each tuple in the list always has 2 values.
    :postcondition: returns a dictionary created from the list of tuples. {tuple1[0]: tuple1[1], tuple2[0]: tuple2[1]}
    >>> list_of_tuples_to_dictionary([(0,1), (1,2), (2,3)])
    {0: 1, 1: 2, 2: 3}
    >>> list_of_tuples_to_dictionary([(0,1)])
    {0: 1}
    """
    dictionary = {}
    for pair in input_list:
        dictionary[pair[0]] = pair[1]
    return dictionary


def regenerate_health(game_info):
    """
    Add 5 health each time the function is called.

    :param game_info: game_info dictionary
    :return: None
    :precondition: game_info dictionary is formatted correctly.
    :postcondition: game_info will be updated with the new health.
    """
    if game_info["Player"]["HP"] < game_info["Player"]["MaxHP"]:
        game_info["Player"]["HP"] += 5
        if game_info["Player"]["HP"] > game_info["Player"]["MaxHP"]:
            game_info["Player"]["HP"] = game_info["Player"]["MaxHP"]


def level_up(game_info, enemy):
    """
    Decide whether to level up the player.

    :param game_info: game_info dictionary.
    :param enemy: enemy dictionary
    :return: None
    :precondition: all params are formatted correctly.
    :postcondition: Player will be leveled up if they meet the requirements, updating game_info.
    """
    if (game_info['Player']['Exp'] > 150 and game_info['Player']['Level'] == 1) or (
            game_info['Player']['Exp'] > 300 and game_info['Player']['Level'] == 2):
        game_info["Player"]["Level"] += 1
        game_info["Player"]["MaxHP"] += int(game_info["Player"]["MaxHP"] * 0.5)

        print(get_message("Messages.LEVELUP", game_info).replace("!ENEMY", enemy["Name"]))
        time.sleep(2)


def show_player_stats(game_info):
    """
    Prints the player's stats to the screen.

    :param game_info: game_info dictionary
    :return: None
    :precondition: game_info is formatted correctly.
    :postcondition: will print all the attributes to the screen, except the ignored ones.
    """
    ignore_keys = ["MaxHP", "Inventory", "Equipped"]
    for key, value in game_info["Player"].items():
        if key not in ignore_keys:
            print(key + ": " + str(value))
            time.sleep(0.2)


def die(game_info):
    """
    Prints the deaths messages and ends the program.

    :param game_info: game_info dictionary
    :return: None
    :precondition: game_info is formatted correctly.
    :postcondition: program will end.
    """
    print(get_message("Art.Death", game_info))
    time.sleep(1)
    print(get_message("Messages.DEATH_1", game_info))
    time.sleep(2)
    print(get_message("Messages.DEATH_2", game_info))
    time.sleep(2)
    quit()


def grab_item(game_info, player_position):
    """
    Put the item in the current room into the player's inventory.

    :param game_info: game_info dictionary
    :param player_position: player_position list
    :return: None
    :precondition: all params are formatted correctly. player_position is within the bounds of the game.
    :postcondition: item will be added to the player's inventory in game_info.
    """
    item = game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Item"]
    game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Item"] = ''
    print(get_message(f"Items.{item}.TakeText", game_info))
    add_to_inventory(game_info, item)
    time.sleep(1)


def add_to_inventory(game_info, item):
    """
    Add an item to the player's inventory.

    :param game_info: game_info dictionary
    :param item: item string
    :return: None
    :precondition: all params are formatted correctly
    :postcondition: game_info player inventory will be updated
    """
    if item not in game_info["Player"]["Inventory"]:
        game_info["Player"]["Inventory"][item] = 1
    else:
        game_info["Player"]["Inventory"][item] += 1


def use_item(game_info, item):
    """
    Use an item from the player's inventory.

    :param game_info: game_info dictionary.
    :param item: item string
    :return: None
    :precondition: all params are formatted correctly.
    :postcondition: Will update the player with the item's effects.
    """
    if item in game_info["Player"]["Inventory"]:
        if "HP" in game_info["Items"][item]:
            print(get_message(f"Items.{item}.UseText", game_info))
            game_info["Player"]["HP"] += int(game_info["Items"][item]["HP"])
            if game_info["Player"]["HP"] > game_info["Player"]["MaxHP"]:
                game_info["Player"]["HP"] = game_info["Player"]["MaxHP"]
        elif "ATK" in game_info["Items"][item]:
            equip_item(game_info, item, "ATK")
        elif "DEF" in game_info["Items"][item]:
            equip_item(game_info, item, "DEF")
        game_info["Player"]["Inventory"][item] -= 1
        if game_info["Player"]["Inventory"][item] <= 0:
            del (game_info["Player"]["Inventory"][item])
    else:
        print(get_message("Messages.INVALIDITEM", game_info))


def equip_item(game_info, item, stat):
    """
    Equip an item.

    :param game_info: game_info dictionary.
    :param item: item string
    :param stat: string
    :return: None
    :precondition: all params are formatted correctly. item and stat are valid options.
    :postcondition: Item will be equipped.
    """
    if game_info["Player"]["Equipped"][game_info["Items"][item]["Slot"]] != "":
        slot_item = game_info["Player"]["Equipped"][game_info["Items"][item]["Slot"]]
        print(get_message("Messages.UNEQUIP", game_info).replace("!ITEM", slot_item))
        game_info["Player"][stat.title()] -= game_info["Items"][slot_item][stat]
        add_to_inventory(game_info, item)
    game_info["Player"]["Equipped"][game_info["Items"][item]["Slot"]] = item
    print(get_message(f"Items.{item}.UseText", game_info))
    game_info["Player"][stat.title()] += game_info["Items"][item][stat]


def get_message(path, game_info):
    """
    Get a value from the game_info dictionary.

    :param path: string
    :param game_info: game_info dictionary
    :return: string or int
    :precondition: all params are formatted correctly. path is a valid location in the dictionary. E.g. Messages.UNEQUIP
    :postcondition: Will return the value of the specified path, as well as making any replacements needed.
    """
    current_item = game_info
    for turn in path.split("."):
        current_item = current_item[turn]
    if isinstance(current_item, list):
        message = random.choice(current_item)
        message = replace_message(message, game_info)
        return message
    return current_item


def replace_message(message, game_info):
    """
    Replace all values in a message with proper values.

    :param message: string
    :param game_info: game_info dictionary
    :return: string
    :precondition: all params are formatted correctly.
    :postcondition: will have replaced any parts of the string that needed replacement.
    """
    for key, value in game_info["Replacements"].items():
        message = message.replace(key, str(get_message(value, game_info)))
    return message


def get_possible_moves(game_info, context, player_position, enemies=[]):
    """
    Will create a numbered list of all the moves you can make.

    :param game_info: game_info dictionary
    :param context: string
    :param player_position: player_position list
    :param enemies: (optional) enemies list
    :return: List of tuples
    :precondition: all params are formatted correctly.
    :postcondition: Will return a list of tuples, formatted as (number, possible move).
    """
    output_list = []
    ignore = ["Move", "Use", "Take", "Quit"]
    move_number = itertools.count()
    possible_inputs = game_info["Inputs"][context]
    for move in possible_inputs:
        if move not in ignore:
            output_list.append((str(next(move_number)), move))
    for item in get_usable_items(game_info):
        output_list.append((str(next(move_number)), item))
    if context == "MapView" and get_grabbable_item(game_info, player_position) != '':
        output_list.append((str(next(move_number)), get_grabbable_item(game_info, player_position)))
    elif context == "Battle":
        output_list.extend(get_attackable_enemies(enemies, move_number))
    print('\n' + '\n'.join(map(': '.join, output_list)))
    return output_list


def get_attackable_enemies(enemies, iterator):
    """
    Create a numbered list of all the enemies.

    :param enemies: enemies dictionary
    :param iterator: iterable
    :return: list of tuples
    :precondition: all params are formatted correctly.
    :postcondition: Will return a list of tuples, formatted as (number, possible move).
    """
    all_enemies = []
    for enemy in enemies:
        all_enemies.append((str(next(iterator)), f'Attack {enemies[enemy]["Name"]}'))
    return all_enemies


def get_usable_items(game_info):
    """
    Get a list of all the items the player can use.

    :param game_info: game_info dictionary
    :return: list
    :precondition: game_info is formatted correctly.
    :postcondition: will return a list of all the items you can use
    """
    usable_items = []
    for item in game_info["Player"]["Inventory"]:
        usable_items.append(f"Use {item}")
    return usable_items


def get_grabbable_item(game_info, player_position):
    """
    Get the item you can grab in the room.

    :param game_info: game_info dictionary
    :param player_position: player_position list
    :return: string
    :precondition: all params are formatted correctly
    :postcondition: will return a string formatted as 'Take {item}'
    """
    item = game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Item"]
    if item != '':
        return f"Take {item}"
    return ''


def choose_class(game_info):
    """
    Get the player to choose their class

    :param game_info: game_info dictionary
    :return: list
    :precondition: game_info is formatted correctly.
    :postcondition: will return the starting position of the selected class, and update the game_info dictionary.
    """
    classes = {}
    iterable = itertools.count()
    for possible_class in game_info["Classes"]:
        classes[next(iterable)] = possible_class
    while True:
        for key, value in classes.items():
            print(f"{key}: {value}")
        player_class = input(get_message("Messages.WELCOME_3", game_info))
        if player_class.isnumeric() and int(player_class) in classes:
            for stat, value in game_info["Classes"][classes[int(player_class)]].items():
                if stat not in ["Starting Pos"]:
                    print(f"{stat}: {value}")
            if input(get_message("Messages.CONFIRMATION", game_info)).lower() == 'y':
                apply_class(game_info, classes[int(player_class)])
                return game_info["Classes"][classes[int(player_class)]]["Starting Pos"]


def apply_class(game_info, chosen_class):
    """
    Set the player's stats to the chosen class.

    :param game_info: game_info dictionary
    :param chosen_class: string
    :return: None
    :precondition: all params are formatted correctly. chosen_class is a valid class.
    :postcondition: player stats will be changed to the class's base stats.
    """
    game_info["Player"]["Class"] = chosen_class
    for attribute in game_info["Player"].keys():
        if attribute in game_info["Classes"][chosen_class].keys():
            game_info["Player"][attribute] = game_info["Classes"][chosen_class][attribute]


def win(game_info):
    """
    Print the win messages and exit the program.

    :param game_info: game_info dictionary
    :return: None
    :precondition: game_info is formatted correctly.
    :postcondition: Program will end.
    """
    print(get_message("Art.Win", game_info))
    print(get_message("Messages.WIN_1", game_info))
    time.sleep(3)
    print(get_message("Messages.WIN_2", game_info))
    time.sleep(3)
    print(get_message("Messages.WIN_3", game_info))
    time.sleep(3)
    quit()


def check_for_win(game_map, player_position):
    """
    Check to see if the player has exited the board.

    :param game_map: game_map list
    :param player_position: player_position list
    :return: bool
    :precondition: all params are formatted correctly.
    :postcondition: Returns True if player has left the board, False otherwise.
    """
    out_of_bounds_negative = player_position[0] < 0 or player_position[1] < 0
    out_of_bounds_positive = player_position[0] > len(game_map) or player_position[1] > len(game_map[0])
    return out_of_bounds_positive or out_of_bounds_negative


def game(game_info_path="./gameInfo.json", map_path="./map.txt"):
    """
    Drives the game

    :return: None
    """
    game_info = load_game_info(game_info_path)
    game_map = load_game_map(map_path)

    print(get_message("Messages.WELCOME_1", game_info))
    time.sleep(2)
    game_info["Player"]["Name"] = input(get_message("Messages.WELCOME_2", game_info))
    time.sleep(2)
    player_position = choose_class(game_info)
    time.sleep(2)
    print(get_message("Messages.INTRODUCTION", game_info))
    time.sleep(2)
    game_info["Player"]["MaxHP"] = game_info["Player"]["HP"]

    last_player_position = [24, 16]
    game_info = populate_game_map(game_info, game_map, player_position)
    while True:
        player_position = initiate_battle(game_info, player_position, last_player_position)
        print_map(game_map, player_position, game_info)
        numbered_input = get_possible_moves(game_info, "MapView", player_position)
        player_input = input(get_message("Messages.MAPPROMPT", game_info))
        input_type, player_input = interperet_input(player_input, False, game_info, numbered_input)
        if input_type != "Error":
            if input_type == "Move":
                player_position, last_player_position = move_player(game_map, player_position, player_input, game_info,
                                                                    last_player_position)
                if player_position[0] < 0:
                    win(game_info)
                print('\n' * 50)
            elif input_type == "Info":
                show_player_stats(game_info)
            elif input_type == "Take":
                grab_item(game_info, player_position)
            elif input_type == "Inventory":
                display_inventory(game_info)
            elif input_type == "Use":
                item = player_input.split(" ", 1)[1]
                use_item(game_info, item)
                time.sleep(1)
            elif input_type == "Quit":
                quit()
        else:
            print(get_message("Messages.INVALIDCOMMAND"), game_info)


def get_kwargs(args):
    final_args = {}
    for arg in args:
        if arg.split('=')[0] == "game_info":
            final_args['game_info_path'] = arg.split('=')[1]
        elif arg.split('=')[0] == "map":
            final_args['map_path'] = arg.split('=')[1]
    return final_args


if __name__ == "__main__":
    kwargs = get_kwargs(sys.argv)
    game(**kwargs)
