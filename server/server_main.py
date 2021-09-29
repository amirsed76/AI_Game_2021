import argparse
import json
from server.logics.game import  Game,Map,Agent
from server.logics.network import Socket


def parse_args():
    parser = argparse.ArgumentParser(description='AI991 Project Server')
    parser.add_argument('-config', default='config.json', type=str)
    parser.add_argument('-map', default='maps/map1.txt', type=str)
    args = parser.parse_args()
    return args.config, args.map


def get_config(config_path):
    with open(config_path) as config_file:
        config = json.load(config_file)

    return config


def get_map(map_path):
    with open(map_path) as map_file:
        data = map_file.read().strip()

    rows = data.splitlines()
    return Map(map_content=rows)


def main():
    from pathlib import Path
    Path("./game_logs").mkdir(parents=True, exist_ok=True)
    print("server is already run")
    config_path, map_path = parse_args()

    config = get_config(config_path=config_path)
    server_ip = config["server_ip"]
    server_port = config["server_port"]
    game_map = get_map(map_path=map_path)
    server = Socket.create(ip=server_ip, port=server_port)
    player_connections = []
    for agent_id in range(config["player_count"]):
        try:
            conn = server.accept_client()
            player_connections.append(conn)
            print(f"one agent connected:{conn.addr}")
        except:
            pass

    game = Game.create_game(config=config, player_connections=player_connections, game_map=game_map)
    game.run()


if __name__ == '__main__':
    main()
