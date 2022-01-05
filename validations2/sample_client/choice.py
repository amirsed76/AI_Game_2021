def best_choice(objective_map, location2):
    location = location2
    agent_location_row = location[0]
    agent_location_col = location[1]

    up = 0
    down = 0
    left = 0
    right = 0
    trap = 0

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

    if next_state == current_state:
        return location

    elif next_state == up:
        location[0] -= 1
        return best_choice(objective_map, location)
    elif next_state == down:
        location[0] += 1
        return best_choice(objective_map, location)
    elif next_state == right:
        location[1] += 1
        return best_choice(objective_map, location)
    elif next_state == left:
        location[1] -= 1
        return best_choice(objective_map, location)
