"""
Your name: Lachlan Butler
Your student number: A01266963

All of your code must go in this file.
"""
import json
import random
import math
import time


def load_game_info():
    with open("gameInfo.json", "r", encoding="utf8") as file:
        output = file.read()
        final_json = json.loads(output)
        return final_json


def load_game_map():
    with open("map.txt", "r", encoding="utf8") as file:
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
    for row in range(len(game_map)):
        game_info["Map"]["Game Map"][row] = {}
        for room in range(len(game_map[row])):
            game_info["Map"]["Game Map"][row][room] = {}
            game_info["Map"]["Game Map"][row][room]["Piece"] = game_map[row][room]
            game_info["Map"]["Game Map"][row][room]["Enemies"] = []
            game_info["Map"]["Game Map"][row][room]["Description"] = random.choice(game_info["Map"]["Descriptions"])
            if game_info["Map"]["Pieces"][game_map[row][room]]["Enemies"] == ["Random"] and random.randrange(0, 100) < 20 and [row, room] != player_position:
                for i in range(random.randrange(1, 3)):
                    random_enemy = random.choice(list(game_info["Enemies"].keys()))
                    game_info["Map"]["Game Map"][row][room]["Enemies"].append(random_enemy)
            game_info["Map"]["Game Map"][row][room]["Item"] = ''
            if game_info["Map"]["Game Map"][row][room]["Piece"] != "░" and (random.randrange(0, 100) < 20 or [row, room] == player_position):
                random_item = random.choice(list(game_info["Items"].keys()))
                if [row, room] == player_position:
                    game_info["Map"]["Game Map"][row][room]["Item"] = "Medkit"
                elif game_info["Items"][random_item]["Unique"] != "True" or game_info["Items"][random_item]["Used"] == "False":
                    game_info["Map"]["Game Map"][row][room]["Item"] = random_item
                    game_info["Items"][random_item]["Used"] = "True"
    return game_info


def print_map(game_map, player_position, game_info):
    final_map = ""
    view_range = [2, 4] #Vertical, Horizontal
    for row in range(len(game_map)):
        if abs(player_position[0] - row) <= view_range[0]: #Check vertical distance
            for room in range(len(game_map[row])):
                if abs(player_position[1] - room) <= view_range[1]: #Check horizontal distance
                    if [row, room] == player_position:
                        final_map += f'\033[{game_info["Colours"]["Player"]}m' + game_map[row][room] + f'\033[{game_info["Colours"]["Normal"]}m'
                    elif (len(game_info["Map"]["Game Map"][row][room]["Enemies"]) > 0):
                        final_map += f'\033[{game_info["Colours"]["Enemy"]}m' + game_map[row][room] + f'\033[{game_info["Colours"]["Normal"]}m'
                    else:
                        final_map += f'\033[{game_info["Colours"][game_info["Map"]["Pieces"][game_map[row][room]]["Colour"]]}m' + game_map[row][room] + f'\033[{game_info["Colours"]["Normal"]}m'
            final_map += "\n"
    print(final_map)
    print(game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Description"])
    print_items(game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Item"], game_info)


def print_items(room_item, game_info):
    if room_item != "":
        print(random.choice(game_info["Items"][room_item]["Room Description"]))

def check_level(game_map, new_position, game_info):
    if game_map[new_position[0]][new_position[1]] == "2":
        if int(game_info["Player"]["Level"]) >= 2:
            return True
    elif game_map[new_position[0]][new_position[1]] == "3":
        if int(game_info["Player"]["Level"]) >= 3:
            return True
    else:
        return True
    return False


def move_player(game_map, player_position, move_direction, game_info, last_player_position):
    possible_directions = game_info["Map"]["Pieces"][game_map[player_position[0]][player_position[1]]]["Dir"]
    level_message = 'You swipe your keycard to enter the room, but it says you need a higher level of access to pass.'
    if move_direction in possible_directions:
        last_player_position = player_position.copy()
        if move_direction.lower() == "north" or move_direction.lower() == "n":
            if check_level(game_map, [player_position[0] - 1, player_position[1]], game_info):
                player_position[0] = player_position[0] - 1
            else:
                print(level_message)
        elif move_direction.lower() == "south" or move_direction.lower() == "s":
            if check_level(game_map, [player_position[0] + 1, player_position[1]], game_info):
                player_position[0] = player_position[0] + 1
            else:
                print(level_message)
        elif move_direction.lower() == "east" or move_direction.lower() == "e":
            if check_level(game_map, [player_position[0], player_position[1] + 1], game_info):
                player_position[1] = player_position[1] + 1
            else:
                print(level_message)
        elif move_direction.lower() == "west" or move_direction.lower() == "w":
            if check_level(game_map, [player_position[0], player_position[1] - 1], game_info):
                player_position[1] = player_position[1] - 1
            else:
                print(level_message)
        regenerate_health(game_info)
    return player_position, last_player_position


def initiate_battle(game_info, player_position, last_player_position, game_map):
    enemies = game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"]
    current_battle = {}
    battle_message = "In the room you find "
    for enemy in range(len(enemies)):
        if type(game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"]) is not dict:
            current_battle[enemy] = game_info["Enemies"][enemies[enemy]].copy()
            battle_message += f"an {current_battle[enemy]['Name']}, and "
            if current_battle[enemy]["Speed"] > game_info["Player"]["Speed"]:
                attacked(game_info, enemy)
        else:
            current_battle = game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"]
            battle_message = "So, you've come back to finish the fight. They are still......"
            break
    if len(current_battle) > 0:
        print(battle_message[:-6] + " blocking your path.")
        return battle(game_info, current_battle, player_position, last_player_position, game_map)
    return player_position


def battle(game_info, current_battle, player_position, last_player_position, game_map):
    while len(current_battle) > 0:
        time.sleep(1)
        if game_info['Player']['HP'] <= 0:
            time.sleep(1)
            die(game_info)
        has_attacked = False
        player_input = input(f"({game_info['Player']['HP']}HP) (BATTLE): What would you like to do next?: ")
        input_type = interperet_input(player_input, True, game_info)
        if input_type == "Attack":
            for enemy in current_battle:
                if ((len(player_input.split(" ")) > 1) and (player_input.split(" ")[1] in current_battle[enemy]["Name"])) or (len(player_input.split(" ")) == 1):
                    current_battle[enemy] = attack(game_info, current_battle[enemy])
                    has_attacked = True
                    if current_battle[enemy]["HP"] <= 0:
                        game_info['Player']['Kills'] += 1
                        game_info['Player']['Exp'] += current_battle[enemy]["Exp"]
                        print(random.choice(current_battle[enemy]['TEXT']['DEATH']))
                        if (game_info['Player']['Exp'] > 50 and game_info['Player']['Level'] == 1) or (game_info['Player']['Exp'] > 100 and game_info['Player']['Level'] == 2):
                            level_up(game_info, current_battle[enemy])
                        del(current_battle[enemy])
                    break
            if not has_attacked:
                print("I can't find that enemy.")
        elif input_type == "Inventory":
            display_inventory(game_info)
        elif input_type == "Info":
            for enemy in current_battle:
                print("\n")
                for key, value in current_battle[enemy].items():
                    if key != "TEXT" and key != "Exp":
                        print(key + ": " + str(value))
        elif input_type == "Flee":
            print_map(game_map, last_player_position, game_info)
            game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"] = current_battle
            return last_player_position
        elif input_type == "Use Item":
            item = player_input.split(" ")[1]
            use_item(game_info, item)
        if has_attacked:
            for enemy in current_battle:
                attacked(game_info, current_battle[enemy])

    game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"] = []
    return player_position


def display_inventory(game_info):
    print("Item | Count")
    for item, count in game_info["Player"]["Inventory"].items():
        print(item, count)


def attack(game_info, enemy):
    time.sleep(1)
    random_number = random.randrange(0, 100)
    if random_number >= 20:
        damage = math.ceil((game_info["Player"]["Atk"] * 5) * (random_number/100))
        damage -= enemy["Def"]
        if damage <= 0:
            print(random.choice(game_info["Enemies"][enemy["Name"]]["TEXT"]["DEF"]))
            return enemy

        enemy["HP"] -= damage
        print(random.choice(game_info["Enemies"][enemy["Name"]]["TEXT"]["HIT"]).replace("!DMG", str(damage)))
    else:
        print(random.choice(game_info["Enemies"][enemy["Name"]]["TEXT"]["MISS"]))
    return enemy


def attacked(game_info, enemy):
    time.sleep(1)
    random_number = random.randrange(0, 100)
    if random_number >= 20:
        damage = math.ceil((enemy["Atk"] * 5) * (random_number / 100))
        damage -= game_info["Player"]["Def"]
        if damage <= 0:
            print(random.choice(game_info["Enemies"][enemy["Name"]]["TEXT"]["ATKDEF"]))
            return enemy

        game_info["Player"]["HP"] -= damage
        print(random.choice(game_info["Enemies"][enemy["Name"]]["TEXT"]["ATKHIT"]).replace("!DMG", str(damage)))
    else:
        print(random.choice(game_info["Enemies"][enemy["Name"]]["TEXT"]["ATKMISS"]))


def interperet_input(input, in_battle, game_info):
    if in_battle:
        for key, value in game_info["Inputs"]["Battle"].items():
            if input.split(" ")[0] in value:
                return key
    else:
        for key, value in game_info["Inputs"]["MapView"].items():
            if input.split(" ")[0] in value:
                return key


def regenerate_health(game_info):
    if game_info["Player"]["HP"] < game_info["Player"]["MaxHP"]:
        game_info["Player"]["HP"] += 5
        if game_info["Player"]["HP"] > game_info["Player"]["MaxHP"]:
            game_info["Player"]["HP"] = game_info["Player"]["MaxHP"]


def level_up(game_info, enemy):
    game_info["Player"]["Level"] += 1
    print(f"When you killed {enemy['Name']}, it dropped a level {game_info['Player']['Level']} keycard! You can now progress to the next section of the facility!")
    time.sleep(2)


def show_player_stats(game_info):
    ignore_keys = ["MaxHP", "Inventory", "Equipped"]
    for key, value in game_info["Player"].items():
        if key not in ignore_keys:
            print(key + ": " + str(value))
            time.sleep(0.2)


def die(game_info):
    print(game_info["Art"]["Death"])
    time.sleep(1)
    print(f"{game_info['Player']['Name']} has died.")
    time.sleep(2)
    print(f"You made it to level {game_info['Player']['Level']}, and killed {game_info['Player']['Kills']} enemies.")
    time.sleep(2)
    quit()


def grab_item(game_info, player_position):
    item = game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Item"]
    game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Item"] = ''
    print(game_info["Items"][item]["TakeText"])
    add_to_inventory(game_info, item)
    time.sleep(1)


def add_to_inventory(game_info, item):
    if item not in game_info["Player"]["Inventory"]:
        game_info["Player"]["Inventory"][item] = 1
    else:
        game_info["Player"]["Inventory"][item] += 1


def use_item(game_info, item):
    print(game_info["Player"]["Inventory"])
    if item in game_info["Player"]["Inventory"]:
        if "HP" in game_info["Items"][item]:
            print(random.choice(game_info["Items"][item]["UseText"]))
            game_info["Player"]["HP"] += int(game_info["Items"][item]["HP"])
            if game_info["Player"]["HP"] > game_info["Player"]["MaxHP"]:
                game_info["Player"]["HP"] = game_info["Player"]["MaxHP"]
        elif "ATK" in game_info["Items"][item]:
            if game_info["Player"]["Equipped"][game_info["Items"][item]["Slot"]] != "":
                print(f'You put your {game_info["Player"]["Equipped"][game_info["Items"][item]["Slot"]]} back in your pocket.')
                add_to_inventory(game_info, item)
            game_info["Player"]["Equipped"][game_info["Items"][item]["Slot"]] = game_info["Items"][item]
            print(random.choice(game_info["Items"][item]["UseText"]))
            new_atk = game_info["Classes"][game_info["Player"]["Class"]]["Atk"] + int(game_info["Items"][item]["ATK"])
            game_info["Player"]["Atk"] = new_atk
        elif "DEF" in game_info["Items"][item]:
            if game_info["Player"]["Equipped"][game_info["Items"][item]["Slot"]] != "":
                print(f'You put your {game_info["Player"]["Equipped"][game_info["Items"][item]["Slot"]]} back in your pocket.')
                add_to_inventory(game_info, item)
            game_info["Player"]["Equipped"][game_info["Items"][item]["Slot"]] = game_info["Items"][item]
            print(random.choice(game_info["Items"][item]["UseText"]))
            new_atk = game_info["Classes"][game_info["Player"]["Class"]]["Atk"] + int(game_info["Items"][item]["ATK"])
            game_info["Player"]["Atk"] = new_atk

        game_info["Player"]["Inventory"][item] -= 1
        if game_info["Player"]["Inventory"][item] <= 0:
            del(game_info["Player"]["Inventory"][item])
    else:
        print("You don't have one of those. (Case sensitive)")


def main():
    player_position = [24, 17]
    last_player_position = [24, 16]
    game_info = load_game_info()
    game_map = load_game_map()
    game_info = populate_game_map(game_info, game_map, player_position)
    while True:
        player_position = initiate_battle(game_info, player_position, last_player_position, game_map)
        print_map(game_map, player_position, game_info)
        player_input = input(f"({game_info['Player']['HP']}HP) What would you like to do?: ")
        input_type = interperet_input(player_input, False, game_info)
        if input_type != "Error":
            if input_type == "Move":
                player_position, last_player_position = move_player(game_map, player_position, player_input, game_info, last_player_position)
            elif input_type == "Info":
                show_player_stats(game_info)
            elif input_type == "Take Item":
                grab_item(game_info, player_position)
            elif input_type == "Inventory":
                display_inventory(game_info)
        else:
            print("I don't know what you mean.")



if __name__ == "__main__":
    main()
