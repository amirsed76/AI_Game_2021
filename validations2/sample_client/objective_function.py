def update_teleports(map_list, teleports_location):
    if len(teleports_location) > 0:
        sum = 0
        for i in range(0, len(teleports_location)):
            sum += map_list[teleports_location[i][0]][teleports_location[i][1]]

        teleports_avg = sum / len(teleports_location)
        for i in range(0, len(teleports_location)):
            map_list[teleports_location[i][0]][teleports_location[i][1]] = teleports_avg


def create_function_from_map(map_list, teleports_location, teleports_updated):
    is_changed = False
    for i in range(0, map_list.shape[0]):
        for j in range(0, map_list.shape[1]):

            up = 0
            down = 0
            left = 0
            right = 0
            # Check if we are in the first row
            if i == 0:
                up = -100

            # Check if we are in the first column
            if j == 0:
                left = -100

            # Check if we are in the last row
            if i == map_list.shape[0] - 1:
                down = -100

            # Check if we are in the last column
            if j == map_list.shape[1] - 1:
                right = -100

            if up != -100:
                up = map_list[i - 1][j]

            if down != -100:
                down = map_list[i + 1][j]

            if left != -100:
                left = map_list[i][j - 1]

            if right != -100:
                right = map_list[i][j + 1]

            if map_list[i][j] < max([up, down, left, right]) / 2 and map_list[i][j] != -1:
                map_list[i][j] = max([up, down, left, right]) / 2
                is_changed = True

    if is_changed:
        create_function_from_map(map_list, teleports_location, teleports_updated)

    elif not teleports_updated:
        update_teleports(map_list, teleports_location)
        create_function_from_map(map_list, teleports_location, True)
    return map_list
