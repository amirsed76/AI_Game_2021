import argparse
import json
from server.logics.game import Game, Map
from server.logics.network import Socket
from server.logics import Exceptions
from pathlib import Path


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def parse_args():
    parser = argparse.ArgumentParser(description='AI991 Project Server')
    parser.add_argument('-config', default='config.json', type=str)
    args = parser.parse_args()
    return args.config


def get_config(config_path):
    with open(config_path) as config_file:
        config = json.load(config_file)

    return config


def get_map(map_path):
    with open(map_path) as map_file:
        data = map_file.read().strip()

    if data.count("T") == 1:
        raise Exceptions.InValidMap(why_invalid="number of exist teleports can't 1 ")

    rows = data.splitlines()
    if [rows[0][0], rows[0][-1], rows[-1][0], rows[-1][-1]] != ["E"] * 4:
        raise Exceptions.InValidMap(why_invalid="map corners must be empty")
    height = len(rows)
    width = len(rows[0])

    for row in rows:
        if len(row) != width:
            raise Exceptions.InValidMap(why_invalid="length of each row must be the same")
        for character in row:
            if character not in ["E", "W", "1", "2", "3", "4", "T"]:
                raise Exceptions.InValidMap(why_invalid=f"{character} is not valid map character")

    if height > 30 or width > 30:
        raise Exceptions.InValidMap(why_invalid=f"width and height can't bigger than 30 ")

    return Map(map_content=rows)


def main():
    Path("./game_logs").mkdir(parents=True, exist_ok=True)
    print("server is already run")
    config_path = parse_args()

    config = get_config(config_path=config_path)
    server_ip = config["server_ip"]
    server_port = config["server_port"]
    map_path = f"maps/{config['map']}"
    game_map = get_map(map_path=map_path)
    server = Socket.create(ip=server_ip, port=server_port)
    player_connections = []
    if config["player_count"] not in range(1, 3):
        raise Exceptions.InValidConfig(why_invalid="player count can only 1 or 2 ")

    for agent_id in range(config["player_count"]):
        try:
            conn = server.accept_client()
            player_connections.append(conn)
            print(f"one agent connected:{conn.addr}")
        except Exception as e:
            print(bcolors.WARNING, e)

    game = Game.create_game(config=config, player_connections=player_connections, game_map=game_map)
    game.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(bcolors.FAIL, e)
