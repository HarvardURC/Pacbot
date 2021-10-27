from enum import Enum

DISPLAY_FREQUENCY = 240 # 60 Hz
SPRITE_FREQUENCY = 6
GRID_SIZE = (28, 31)
SQUARE_SIZE = 31
#SQUARE_SIZE = 30
SPRITE_FILE = 'graphics/pac_t.bmp'

# ghost enums:
class Ghosts(Enum):
    RED = 0
    BLUE = 1
    PINK = 2
    ORANGE = 3

class Split(Enum):
    TOP = 0
    BOTTOM = 1
    FULL = 2

# colors:
red_color = (255, 0, 0)
green_color = (0, 255, 0)
blue_color = (0, 255, 255)
pink_color = (255, 185, 255)
orange_color = (255, 185, 81)
yellow_color = (255, 255, 61)
white_color = (255, 255, 255)
dark_blue_color = (33, 33, 255)
black_color = (0, 0, 0)
