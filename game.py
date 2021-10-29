"""
Your name: Lachlan Butler
Your student number: A01266963

All of your code must go in this file.
"""
import json


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


def print_map(game_map, player_position, game_info):
    final_map = ""
    for row in range(len(game_map)):
        for room in range(len(game_map[row])):
            if [row, room] == player_position:
                final_map += f'\033[{game_info["Colours"]["Player"]}m' + game_map[row][room] + f'\033[{game_info["Colours"]["Normal"]}m'
            else:
                final_map += game_map[row][room]
        final_map += "\n"
    return final_map


def main():
    player_position = [2, 12]
    game_info = load_game_info()
    game_map = load_game_map()
    print(print_map(game_map, player_position, game_info))


if __name__ == "__main__":
    main()