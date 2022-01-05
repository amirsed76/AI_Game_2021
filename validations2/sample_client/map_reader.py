import pickle
from cmath import sqrt

import numpy as np


def read_map(game_map, agent_score, opponent_score, agent_name, opponent_name, old_opponent_loc, old_agent_loc,
             banned_gem):
    agent_location = []
    opponent_location = []
    teleports_location = []
    has_trap = False
    with open('gems.txt', 'rb') as fp:
        gems_count = pickle.load(fp)
    map_list = np.zeros((len(game_map), len(game_map[0])))

    for i in range(0, len(game_map)):
        for j in range(0, len(game_map[i])):
            if agent_name in game_map[i][j]:
                agent_location = [i, j]
                if agent_name.lower() in game_map[i][j]:
                    has_trap = True

            if opponent_name in game_map[i][j]:
                opponent_location = [i, j]

    for i in range(0, len(game_map)):
        for j in range(0, len(game_map[i])):

            agent_distance = abs(agent_location[0] - i) + abs(agent_location[1] - j)
            opponent_distance = (abs(opponent_location[0] - i) + abs(opponent_location[1] - j))

            banned=[i,j]==banned_gem and agent_distance>opponent_distance

            if 'E' in game_map[i][j][0]:
                map_list[i][j] = 0

            elif '1' in game_map[i][j][0] and gems_count[0] < 15 and not banned:
                map_list[i][j] = 10 * opponent_distance

            elif '2' in game_map[i][j][0] and gems_count[1] < 8 and (agent_score - agent_distance) >= 15 and not banned:
                map_list[i][j] = 25 * opponent_distance

            elif '3' in game_map[i][j][0] and gems_count[2] < 5 and (agent_score - agent_distance) >= 50 and not banned:
                map_list[i][j] = 35 * opponent_distance

            elif '4' in game_map[i][j][0] and gems_count[3] < 4 and (agent_score - agent_distance) >= 140 and not banned:
                map_list[i][j] = 75 * opponent_distance

            elif game_map[i][j][0] == 'W':
                map_list[i][j] = -1

            elif 'T' in game_map[i][j][0]:
                map_list[i][j] = 0
                teleports_location.append([i, j])

            else:
                map_list[i][j] = 0

            # if agent_name in game_map[i][j]:
            #     agent_location = [i, j]
            #
            # if opponent_name in game_map[i][j]:
            #     opponent_location = [i, j]

    old_distance = sqrt(
        abs(old_opponent_loc[0] - old_agent_loc[0]) ** 2 + abs(old_opponent_loc[1] - old_agent_loc[1]) ** 2)
    new_distance = sqrt(
        abs(agent_location[0] - opponent_location[0]) ** 2 + abs(agent_location[1] - opponent_location[1]) ** 2)

    if new_distance.real < old_distance.real and agent_score > opponent_score:
        map_list[opponent_location[0], opponent_location[1]] = 20

    with open('gems.txt', 'wb') as fp:
        pickle.dump(gems_count, fp)

    return map_list, agent_location, opponent_location, teleports_location, has_trap
