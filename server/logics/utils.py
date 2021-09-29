def replace_character(string, character, index):
    list_string = list(string)
    list_string[index] = character
    return "".join(list_string)
