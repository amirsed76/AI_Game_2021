import pickle

from choice import best_choice
from map_reader import read_map
from objective_function import create_function_from_map


def action(map_list, score, opponent_score, agent_name, opponent_name, old_opponent_location, old_agent_location,
           traps_count):
    base_map, agent_location, opponent_location, teleports_location, has_trap = read_map(map_list, score,
                                                                                         opponent_score, agent_name,
                                                                                         opponent_name,
                                                                                         old_opponent_location,
                                                                                         old_agent_location, [-1, -1])
    objective_map = create_function_from_map(base_map, teleports_location, False)

    agent_hill = best_choice(objective_map, agent_location.copy())
    opponent_hill = best_choice(objective_map, opponent_location.copy())

    if agent_hill == opponent_hill:
        base_map, agent_location, opponent_location, teleports_location, has_trap = read_map(map_list, score,
                                                                                             opponent_score, agent_name,
                                                                                             opponent_name,
                                                                                             old_opponent_location,
                                                                                             old_agent_location,
                                                                                             agent_hill)
        objective_map = create_function_from_map(base_map, teleports_location, False)

    with open('gems.txt', 'rb') as fp:
        gems_count = pickle.load(fp)
    print(objective_map)
    print(score)
    print(gems_count)
    agent_location_row = agent_location[0]
    agent_location_col = agent_location[1]

    up = 0
    down = 0
    left = 0
    right = 0

    # Check if we are in the first row
    if agent_location_row == 0:
        up = -100

    # Check if we are in the first column
    if agent_location_col == 0:
        left = -100

    # Check if we are in the last row
    if agent_location_row == objective_map.shape[0] - 1:
        down = -100

    # Check if we are in the last column
    if agent_location_col == objective_map.shape[1] - 1:
        right = -100

    if up != -100:
        up = objective_map[agent_location_row - 1][agent_location_col]

    if down != -100:
        down = objective_map[agent_location_row + 1][agent_location_col]

    if left != -100:
        left = objective_map[agent_location_row][agent_location_col - 1]

    if right != -100:
        right = objective_map[agent_location_row][agent_location_col + 1]

    current_state = objective_map[agent_location_row][agent_location_col]
    next_state = max([up, down, right, left, current_state])

    if next_state == 10:
        gems_count[0] += 1
    if next_state == 25:
        gems_count[1] += 1
    if next_state == 35:
        gems_count[2] += 1
    if next_state == 75:
        gems_count[3] += 1

    is_same_row = agent_location[0] == opponent_location[0]
    is_same_column = agent_location[1] == opponent_location[1]
    opponent_on_left = agent_location[1] > opponent_location[1]
    opponent_on_right = agent_location[1] < opponent_location[1]
    opponent_on_top = agent_location[0] > opponent_location[0]
    opponent_on_down = agent_location[0] < opponent_location[0]
    opponent_right_move = opponent_location[1] > old_opponent_location[1]
    opponent_left_move = opponent_location[1] < old_opponent_location[1]
    opponent_up_move = opponent_location[0] < old_opponent_location[0]
    opponent_down_move = opponent_location[0] > old_opponent_location[0]

    can_add_trap = gems_count[4] * 35 <= score and gems_count[4] < traps_count

    # If movement is left
    if next_state == left and is_same_row and opponent_on_right and opponent_left_move and can_add_trap and not has_trap:
        gems_count[4] += 1
        with open('gems.txt', 'wb') as fp:
            pickle.dump(gems_count, fp)
        return "trap", opponent_location

    if next_state == right and is_same_row and opponent_on_left and opponent_right_move and can_add_trap and not has_trap:
        gems_count[4] += 1
        with open('gems.txt', 'wb') as fp:
            pickle.dump(gems_count, fp)
        return "trap", opponent_location

    if next_state == up and is_same_column and opponent_on_down and opponent_up_move and can_add_trap and not has_trap:
        gems_count[4] += 1
        with open('gems.txt', 'wb') as fp:
            pickle.dump(gems_count, fp)
        return "trap", opponent_location

    if next_state == down and is_same_column and opponent_on_top and opponent_down_move and can_add_trap and not has_trap:
        gems_count[4] += 1
        with open('gems.txt', 'wb') as fp:
            pickle.dump(gems_count, fp)
        return "trap", opponent_location

    with open('gems.txt', 'wb') as fp:
        pickle.dump(gems_count, fp)

    if next_state == current_state and [agent_location_row, agent_location_col] in teleports_location:
        return "teleport", opponent_location
    if next_state == current_state:
        return "noop", opponent_location
    if next_state == up:
        return "up", opponent_location
    if next_state == down:
        return "down", opponent_location
    if next_state == right:
        return "right", opponent_location
    if next_state == left:
        return "left", opponent_location

# def evaluate_move(objective_map, location):
#     up = 0
#     down = 0
#     left = 0
#     right = 0
#
#     brk = False
#
#     hill_loc = [0, 0]
#
#     while not brk:
#         for i in range(0, objective_map.shape[0]):
#             for j in range(0, objective_map.shape[1]):
#
#                 agent_location_row = i
#                 agent_location_col = j
#
#                 # Check if we are in the first row
#                 if agent_location_row == 0:
#                     up = -100
#
#                 # Check if we are in the first column
#                 if agent_location_col == 0:
#                     left = -100
#
#                 # Check if we are in the last row
#                 if agent_location_row == objective_map.shape[0] - 1:
#                     down = -100
#
#                 # Check if we are in the last column
#                 if agent_location_col == objective_map.shape[1] - 1:
#                     right = -100
#
#                 if up != -100:
#                     up = objective_map[agent_location_row - 1][agent_location_col]
#
#                 if down != -100:
#                     down = objective_map[agent_location_row + 1][agent_location_col]
#
#                 if left != -100:
#                     left = objective_map[agent_location_row][agent_location_col - 1]
#
#                 if right != -100:
#                     right = objective_map[agent_location_row][agent_location_col + 1]
#
#                 current_state = objective_map[agent_location_row][agent_location_col]
#                 next_state = max([up, down, right, left, current_state])
#
#                 if current_state == next_state:
#                     brk = True
#                     hill_loc = [i, j]
