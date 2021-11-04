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


def populate_game_map(game_info, game_map):
    for row in range(len(game_map)):
        game_info["Map"]["Game Map"][row] = {}
        for room in range(len(game_map[row])):
            game_info["Map"]["Game Map"][row][room] = {}
            game_info["Map"]["Game Map"][row][room]["Piece"] = game_map[row][room]
            game_info["Map"]["Game Map"][row][room]["Enemies"] = []
            if game_info["Map"]["Pieces"][game_map[row][room]]["Enemies"] == ["Random"] and random.randrange(0, 100) < 20:
                for i in range(random.randrange(1, 3)):
                    random_enemy = random.choice(list(game_info["Enemies"].keys()))
                    game_info["Map"]["Game Map"][row][room]["Enemies"].append(random_enemy)
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


def move_player(game_map, player_position, move_direction, game_info):
    possible_directions = game_info["Map"]["Pieces"][game_map[player_position[0]][player_position[1]]]["Dir"]
    if move_direction in possible_directions:
        if move_direction.lower() == "north" or move_direction.lower() == "n":
            player_position[0] = player_position[0] - 1
        elif move_direction.lower() == "south" or move_direction.lower() == "s":
            player_position[0] = player_position[0] + 1
        elif move_direction.lower() == "east" or move_direction.lower() == "e":
            player_position[1] = player_position[1] + 1
        elif move_direction.lower() == "west" or move_direction.lower() == "w":
            player_position[1] = player_position[1] - 1
        regenerate_health(game_info)
    return player_position


def initiate_battle(game_info, player_position):
    enemies = game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"]
    current_battle = {}
    battle_message = "In the room you find "
    for enemy in range(len(enemies)):
        current_battle[enemy] = game_info["Enemies"][enemies[enemy]].copy()
        battle_message += f"an {current_battle[enemy]['Name']}, and "
        if current_battle[enemy]["Speed"] > game_info["Player"]["Speed"]:
            attacked(game_info, enemy)
    if len(current_battle) > 0:
        print(battle_message[:-6] + ".")
        battle(game_info, current_battle, player_position)


def battle(game_info, current_battle, player_position):
    while len(current_battle) > 0:
        if game_info['Player']['HP'] <= 0:
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
                    if key != "TEXT":
                        print(key + ": " + str(value))
        if has_attacked:
            for enemy in current_battle:
                attacked(game_info, current_battle[enemy])
    game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"] = []


def display_inventory(game_info):
    print("Item | Count")
    for item, count in game_info["Player"]["Inventory"].items():
        print(item, count)


def attack(game_info, enemy):
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
    if game_info["Player"]["HP"] < 50:
        game_info["Player"]["HP"] += 5
        if game_info["Player"]["HP"] > 50:
            game_info["Player"]["HP"] = 50


def die(game_info):
    print(game_info["Art"]["939"])
    print(f"{game_info['Player']['Name']} has died.")
    time.sleep(2)
    print(f"You made it to level {game_info['Player']['Level']}, and killed {game_info['Player']['Kills']} enemies.")
    time.sleep(2)
    quit()


def main():
    player_position = [24, 17]
    game_info = load_game_info()
    game_map = load_game_map()
    game_info = populate_game_map(game_info, game_map)
    while True:
        print_map(game_map, player_position, game_info)
        initiate_battle(game_info, player_position)
        player_input = input(f"({game_info['Player']['HP']}HP) What would you like to do?: ")
        input_type = interperet_input(player_input, False, game_info)
        if input_type != "Error":
            if input_type == "Move":
                player_position = move_player(game_map, player_position, player_input, game_info)
        else:
            print("I don't know what you mean.")


if __name__ == "__main__":
    main()
