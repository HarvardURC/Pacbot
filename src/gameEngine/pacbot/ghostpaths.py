from .variables import *

# These start paths defines the paths the ghosts take at the beginning of a new round.
# Pink immedaitely leaves the respawn zone, while blue and orange remain it it for 
# some time before eventually leaving. Red begins outside the zone, and as such
# does not have a predefined starting path.

pink_start_path = [((14,17),up),((14,18),up),((14,19),up)]

blue_start_path = [((12,17),up),((12,16),down),((12,15),down),((12,16),up),((12,17),up),
            ((12,16),down),((12,15),down),((12,16),up),((12,17),up),((12,16),down),
            ((12,15),down),((12,16),up),((12,17),up),((12,16),down),((12,15),down),
            ((12,16),up),((12,17),up),((12,16),down),((12,15),down),((13,15),right),
            ((13,16),up),((13,17),up),((13,18),up),((13,19),up)]

orange_start_path = [((15,17),up),((15,16),down),((15,15),down),((15,16),up),((15,17),up),
              ((15,16),down),((15,15),down),((15,16),up),((15,17),up),((15,16),down),
              ((15,15),down),((15,16),up),((15,17),up),((15,16),down),((15,15),down),
              ((15,16),up),((15,17),up),((15,16),down),((15,15),down),((15,16),up),
              ((15,17),up),((15,16),down),((15,15),down),((15,16),up),((15,17),up),
              ((15,16),down),((15,15),down),((15,16),up),((15,17),up),((15,16),down),
              ((15,15),down),((15,16),up),((15,17),up),((15,16),down),((15,15),down),
              ((14,15),left),((14,16),up),((14,17),up),((14,18),up),((14,19),up)]

# The respawn path defines how a ghost will move out of the respawn zone when it has been
# eaten by Pacman in the middle of a round.

respawn_path = [((12,17),up),((12,16),down),((12,15),down),((13,15),right),((13,16),up),((13,17),up),((13,18),up),((13,19),up)]

# This is the location where a ghost will reappear after being eaten by Pacman.

ghost_home_pos = (12, 15)

# These are the coordinates the ghosts attempt to move towards when they are in scatter mode.

pink_scatter_pos = (2, 32)
orange_scatter_pos = (0, -1)
blue_scatter_pos = (27, -1)
red_scatter_pos = (25, 32)

# These are the locations the ghosts begin in at the start of a round.

red_init_pos = (13,19)
red_init_npos = (12,19)
red_init_dir = left

pink_init_pos = (14,15)
pink_init_npos = (14,16)
pink_init_dir = up

blue_init_pos = (12,15)
blue_init_npos = (12,16)
blue_init_dir = up

orange_init_pos = (15,15)
orange_init_npos = (15,16)
orange_init_dir = up

ghost_no_up_tiles = [(12, 19), (15, 19), (12, 7), (15, 7)]