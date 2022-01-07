# Direction enums
right = 0
left = 1
up = 2
down = 3

# Grid enums
# o = normal pellet, e = empty space, O = power pellet, c = cherry position
# I = wall, n = ghost chambers
I = 1
o = 2
e = 3
O = 4
n = 5
c = 6

# State enums
scatter = 1
chase = 2
frightened = 3

# color enums
red = 1
orange = 2
pink = 3
blue = 4

# input signal enums
sig_normal = 0
sig_quit = 1
sig_restart = 2

# game Params
starting_lives = 3
frightened_length = 40
pellet_score = 10
power_pellet_score = 50
cherry_score = 100
ghost_score = 200
state_swap_times = [35, 135, 170, 270, 295, 395, 420]
pacbot_starting_pos = (14, 7)
pacbot_starting_dir = left
cherry_pos = (13, 13)
game_frequency = 2.
ticks_per_update = 12
