#This file is for printing texts in color

color_dict = {
    'PURPLE':'\033[95m',
    'CYAN': '\033[96m',
    'DARKCYAN': '\033[36m',
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
    'END': '\033[0m'
}


#This outputs a text in that color
def color_text(string,color):
    colored_text = color_dict[color.upper()] + string + color_dict['END']
    return colored_text
