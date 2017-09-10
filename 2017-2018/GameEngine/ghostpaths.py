from variables import *

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
              ((15,16),left),((14,16),up),((14,17),up),((14,18),up),((14,19),up)]

respawn_path = [((12,17),up),((12,16),down),((12,15),down),((13,15),right),((13,16),up),((13,17),up),((13,18),up),((13,19),up)]

ghost_home_pos = (12, 15)

pink_scatter_pos = (2, 32)
orange_scatter_pos = (0, -1)
blue_scatter_pos = (27, -1)
red_scatter_pos = (25, 32)

red_init_pos = (13,19)
red_init_npos = (12,19)
red_init_dir = left

pink_init_pos = (13,15)
pink_init_npos = (14,16)
pink_init_dir = up

blue_init_pos = (12,15)
blue_init_npos = (12,16)
blue_init_dir = up

orange_init_pos = (15,15)
orange_init_npos = (15,16)
orange_init_dir = up

ghost_no_up_tiles = [(12, 19), (15, 19), (12, 7), (15, 7)]
