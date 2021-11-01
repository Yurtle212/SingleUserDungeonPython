"""
Your name: Lachlan Butler
Your student number: A01266963

All of your code must go in this file.
"""
import json
import random


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
                    else:
                        final_map += f'\033[{game_info["Colours"][game_info["Map"]["Pieces"][game_map[row][room]]["Colour"]]}m' + \
                                     game_map[row][room] + f'\033[{game_info["Colours"]["Normal"]}m'
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
    return player_position


def initiate_battle(game_info, player_position):
    enemies = game_info["Map"]["Game Map"][player_position[0]][player_position[1]]["Enemies"]
    current_battle = {}
    for enemy in range(len(enemies)):
        current_battle[enemy] = game_info["Enemies"][enemies[enemy]]

        if current_battle[enemy]["Speed"] > game_info["Player"]["Speed"]:
            game_info = attacked(game_info, enemy)
    battle(game_info, enemies, current_battle)


def battle(game_info, enemies, current_battle):
    while len(enemies) > 0:
        player_input = input("What would you like to do next?: ")
        input_type = interperet_input(player_input, True, game_info)
        if input_type == "Attack":
            has_attacked = False
            for enemy in current_battle:
                if (len(player_input.split(" ")) > 0) and (player_input.split(" ")[1] in current_battle[enemy]["Name"]):
                    current_battle[enemy] = attack(game_info, enemy)
                    has_attacked = True
            if not has_attacked:
                print("I can't find that enemy.")
        elif input_type == "Inventory":
            display_inventory(game_info)
        elif input_type == "Info":
            for enemy in current_battle:
                print("\n")
                for key, value in current_battle[enemy].items():
                    print(key + ": " + str(value))


def display_inventory(game_info):
    print("Item | Count")
    for item, count in game_info["Player"]["Inventory"].items():
        print(item, count)


def attack(game_info, enemy):
    return enemy


def attacked(game_info, enemy):
    return game_info


def interperet_input(input, in_battle, game_info):
    if in_battle:
        for key, value in game_info["Inputs"]["Battle"].items():
            if input.split(" ")[0] in value:
                return key
    else:
        for key, value in game_info["Inputs"]["MapView"].items():
            if input.split(" ")[0] in value:
                return key


def main():
    player_position = [24, 17]
    game_info = load_game_info()
    game_map = load_game_map()
    game_info = populate_game_map(game_info, game_map)
    while True:
        print_map(game_map, player_position, game_info)
        initiate_battle(game_info, player_position)
        player_input = input("What would you like to do?: ")
        input_type = interperet_input(player_input, False, game_info)
        if input_type != "Error":
            if input_type == "Move":
                player_position = move_player(game_map, player_position, player_input, game_info)
        else:
            print("I don't know what you mean.")


if __name__ == "__main__":
    main()
