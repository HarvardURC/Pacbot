import robomodules as rm
from messages import *
from .variables import *
from .spriteStripAnim import *

class Visualizer(rm.ProtoModule):
    def __init__(self, addr, port, print_walls, print_pacman, split=Split.FULL, square_size=SQUARE_SIZE):
        self.subscriptions = [MsgType.FULL_STATE]
        super().__init__(addr, port, message_buffers, MsgType,DISPLAY_FREQUENCY, self.subscriptions)

        self.state = None
        self.print_walls = print_walls
        self.print_pacman = print_pacman
        self.last_tick = float('inf')

        self.square_size = square_size

        self.dirs = {
            'red': [None, None],
            'pink': [None, None],
            'orange': [None, None],
            'blue': [None, None],
            'pacman': [None, None]
        }

        pygame.init()
        # Set up the surface to draw on
        # This should also be used in Visualizer.draw()
        self.surface = pygame.Surface((GRID_SIZE[0]*self.square_size, GRID_SIZE[1]*self.square_size))
        self.split = split
        self.y_height = int(GRID_SIZE[1]*self.square_size/2)
        if GRID_SIZE[1] % 2 == 1 and self.split == Split.BOTTOM:
            self.y_height += 1
        elif self.split == Split.FULL:
            self.y_height = GRID_SIZE[1]*self.square_size
        self.display_surface = pygame.display.set_mode((GRID_SIZE[0]*self.square_size, self.y_height))
        pygame.display.set_caption("PACBOT")
        self.font = pygame.font.Font('graphics/crackman.ttf', int(self.square_size))

        self._init_sprites()


    def _init_sprites(self):
        self.sprites = {
            'pacman': {
                'r': SpriteStripAnim(SPRITE_FILE, (453,0,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'l': SpriteStripAnim(SPRITE_FILE, (455,16,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'u': SpriteStripAnim(SPRITE_FILE, (456,32,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'd': SpriteStripAnim(SPRITE_FILE, (455,47,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            },
            'red': {
                'r': SpriteStripAnim(SPRITE_FILE, (456,64,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'l': SpriteStripAnim(SPRITE_FILE, (487,64,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'u': SpriteStripAnim(SPRITE_FILE, (520,64,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'd': SpriteStripAnim(SPRITE_FILE, (552,64,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            },
            'orange': {
                'r': SpriteStripAnim(SPRITE_FILE, (456,112,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'l': SpriteStripAnim(SPRITE_FILE, (487,112,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'u': SpriteStripAnim(SPRITE_FILE, (520,112,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'd': SpriteStripAnim(SPRITE_FILE, (552,112,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            },
            'pink': {
                'r': SpriteStripAnim(SPRITE_FILE, (456,80,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'l': SpriteStripAnim(SPRITE_FILE, (487,80,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'u': SpriteStripAnim(SPRITE_FILE, (520,80,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'd': SpriteStripAnim(SPRITE_FILE, (552,80,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            },
            'blue': {
                'r': SpriteStripAnim(SPRITE_FILE, (456,96,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'l': SpriteStripAnim(SPRITE_FILE, (487,96,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'u': SpriteStripAnim(SPRITE_FILE, (520,96,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'd': SpriteStripAnim(SPRITE_FILE, (552,96,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            },
            'frightened': {
                'r': SpriteStripAnim(SPRITE_FILE, (584,64,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            },
            'fruit': {
                'r': SpriteStripAnim(SPRITE_FILE, (487,48,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            }
        }

    def _update_sprites(self):
        for key in self.sprites:
            for dir_key in self.sprites[key]:
                self.sprites[key][dir_key].iter()

    def _update_dirs(self):
        for key in self.dirs:
            self.dirs[key][0] = self.dirs[key][1]
        self.dirs['red'][1] = self.state.red_ghost.direction
        self.dirs['pink'][1] = self.state.pink_ghost.direction
        self.dirs['orange'][1] = self.state.orange_ghost.direction
        self.dirs['blue'][1] = self.state.blue_ghost.direction
        self.dirs['pacman'][1] = self.state.pacman.direction

    def _clear_screen(self):
        self.surface.fill((0,0,0))

    def _print_score_lives_time(self, score, lives, time):
        score_surf_1 = self.font.render('Score:', True, white_color)
        self.surface.blit(score_surf_1, (self.square_size*23.5, self.square_size*11))
        score_surf_2 = self.font.render('{}'.format(score), True, white_color)
        self.surface.blit(score_surf_2, (self.square_size*23.5, self.square_size*12))

        lives_surf_1 = self.font.render('Lives:', True, white_color)
        self.surface.blit(lives_surf_1, (self.square_size*1, self.square_size*16))
        lives_surf_2 = self.font.render('{}'.format(lives), True, white_color)
        self.surface.blit(lives_surf_2, (self.square_size*1, self.square_size*17))

        time_surf_1 = self.font.render('Time:', True, white_color)
        self.surface.blit(time_surf_1, (self.square_size*23.5, self.square_size*16))
        time_surf_2 = self.font.render('{0:.2f}s'.format(time), True, white_color)
        self.surface.blit(time_surf_2, (self.square_size*23.5, self.square_size*17))


    def _is_ghost_frightened(self, color):
        if color == Ghosts.RED:
            return self.state.red_ghost.frightened_counter > 0
        elif color == Ghosts.BLUE:
            return self.state.blue_ghost.frightened_counter > 0
        elif color == Ghosts.ORANGE:
            return self.state.orange_ghost.frightened_counter > 0
        elif color == Ghosts.PINK:
            return self.state.pink_ghost.frightened_counter > 0
        else:
            return False
    
    def _get_frightened_counter(self, color):
        if color == Ghosts.RED:
            return self.state.red_ghost.frightened_counter
        elif color == Ghosts.BLUE:
            return self.state.blue_ghost.frightened_counter
        elif color == Ghosts.ORANGE:
            return self.state.orange_ghost.frightened_counter
        elif color == Ghosts.PINK:
            return self.state.pink_ghost.frightened_counter
        else:
            return 0

    def _get_interpolated_pos(self, idx, inc):
        return (idx + inc * (self.state.update_ticks - self.state.ticks_per_update/2.) / self.state.ticks_per_update) * self.square_size

    def _get_draw_pos_by_dir(self, col_idx, row_idx, direction):
        if direction == None:
           return (col_idx * self.square_size, row_idx * self.square_size)
        elif direction == PacmanState.LEFT:
            return (self._get_interpolated_pos(col_idx, -1), row_idx * self.square_size)
        elif direction == PacmanState.RIGHT:
            return (self._get_interpolated_pos(col_idx, 1), row_idx * self.square_size)
        elif direction == PacmanState.UP:
            return (col_idx * self.square_size, self._get_interpolated_pos(row_idx, -1))
        else:
            return (col_idx * self.square_size, self._get_interpolated_pos(row_idx, 1))


    def _get_draw_pos(self, col_idx, row_idx, old_dir, new_dir):
        if self.state.update_ticks > self.state.ticks_per_update/2:
            return self._get_draw_pos_by_dir(col_idx, row_idx, new_dir)
        else:
            return self._get_draw_pos_by_dir(col_idx, row_idx, old_dir)

    def _print_ghost(self, color, direction, col_idx, row_idx):
        if color == Ghosts.RED:
            sprite_set = self.sprites['red']
            (x, y) = self._get_draw_pos(col_idx, row_idx, self.dirs['red'][0], self.dirs['red'][1])
        elif color == Ghosts.ORANGE:
            sprite_set = self.sprites['orange']
            (x, y) = self._get_draw_pos(col_idx, row_idx, self.dirs['orange'][0], self.dirs['orange'][1])
        elif color == Ghosts.PINK:
            sprite_set = self.sprites['pink']
            (x, y) = self._get_draw_pos(col_idx, row_idx, self.dirs['pink'][0], self.dirs['pink'][1])
        else:
            sprite_set = self.sprites['blue']
            (x, y) = self._get_draw_pos(col_idx, row_idx, self.dirs['blue'][0], self.dirs['blue'][1])

        if self._is_ghost_frightened(color):
            time_left = self._get_frightened_counter(color)
            self.surface.blit(pygame.transform.scale(self.sprites['frightened']['r'].next(), (self.square_size, self.square_size)), (x,y))
            if time_left < 10:
                if time_left % 2 != 0:
                    self.sprites['frightened']['r'].next().set_alpha(0)
                else:
                    self.sprites['frightened']['r'].next().set_alpha(255)
            else:
                self.sprites['frightened']['r'].next().set_alpha(255)
            print(time_left)
        elif direction == PacmanState.LEFT:
            self.surface.blit(pygame.transform.scale(sprite_set['l'].next(), (self.square_size, self.square_size)), (x,y))
        elif direction == PacmanState.RIGHT:
            self.surface.blit(pygame.transform.scale(sprite_set['r'].next(), (self.square_size, self.square_size)), (x,y))
        elif direction == PacmanState.UP:
            self.surface.blit(pygame.transform.scale(sprite_set['u'].next(), (self.square_size, self.square_size)), (x,y))
        else:
            self.surface.blit(pygame.transform.scale(sprite_set['d'].next(), (self.square_size, self.square_size)), (x,y))

    def _print_pacman(self, direction, col_idx, row_idx):
        (x, y) = (col_idx * self.square_size, row_idx * self.square_size)

        if direction == PacmanState.LEFT:
            self.surface.blit(pygame.transform.scale(self.sprites['pacman']['l'].next(), (self.square_size, self.square_size)), (x,y))
        elif direction == PacmanState.RIGHT:
            self.surface.blit(pygame.transform.scale(self.sprites['pacman']['r'].next(), (self.square_size, self.square_size)), (x,y))
        elif direction == PacmanState.UP:
            self.surface.blit(pygame.transform.scale(self.sprites['pacman']['u'].next(), (self.square_size, self.square_size)), (x,y))
        else:
            self.surface.blit(pygame.transform.scale(self.sprites['pacman']['d'].next(), (self.square_size, self.square_size)), (x,y))

    def _print_pellet(self, col_idx, row_idx):
        x = int((col_idx + 1) * self.square_size - self.square_size/2)
        y = int((row_idx + 1) * self.square_size - self.square_size/2)
        pygame.draw.circle(self.surface, pygame.Color(*white_color), (x,y), int(self.square_size/5))


    def _print_corners(self):
        r = int(self.square_size/3)
        pygame.draw.circle(self.surface, pygame.Color(*green_color), (r,r), r)
        pygame.draw.circle(self.surface, pygame.Color(*green_color), (r,GRID_SIZE[1]*self.square_size-r), int(self.square_size/5))
        pygame.draw.circle(self.surface, pygame.Color(*green_color), (GRID_SIZE[0]*self.square_size - r,GRID_SIZE[1]*self.square_size - r), r)
        pygame.draw.circle(self.surface, pygame.Color(*green_color), (GRID_SIZE[0]*self.square_size - r, r), r)

    def _print_power_pellet(self, col_idx, row_idx):
        x = int((col_idx + 1) * self.square_size - self.square_size/2)
        y = int((row_idx + 1) * self.square_size - self.square_size/2)
        pygame.draw.circle(self.surface, pygame.Color(*white_color), (x,y), int(self.square_size/3))

    def _print_cherry(self, col_idx, row_idx):
        (x, y) = (col_idx * self.square_size, row_idx * self.square_size)
        self.surface.blit(pygame.transform.scale(self.sprites['fruit']['r'].next(), (self.square_size, self.square_size)), (x,y))


    def _print_wall(self, col_idx, row_idx):
        u_idx = col_idx * self.state.grid_columns + row_idx + 1 if row_idx < self.state.grid_columns - 1 else - 1
        d_idx = col_idx * self.state.grid_columns + row_idx - 1 if row_idx > 0 else - 1
        r_idx = (col_idx + 1) * self.state.grid_columns + row_idx
        l_idx = (col_idx - 1) * self.state.grid_columns + row_idx

        row_idx = GRID_SIZE[1] - row_idx - 1

        x = int(col_idx * self.square_size)
        y = int(row_idx * self.square_size)
        pygame.draw.rect(self.surface, pygame.Color(*dark_blue_color), pygame.Rect(x,y, self.square_size, self.square_size))
        x += int(self.square_size/4)
        y += int(self.square_size/4)
        pygame.draw.rect(self.surface, pygame.Color(*black_color), pygame.Rect(x,y, int(self.square_size/2)+1, int(self.square_size/2)+1))

        right = False
        left = False
        up = False
        down = False

        if (u_idx >= 0 and u_idx < len(self.state.grid) and
            self.state.grid[u_idx] == PacmanState.WALL):
            pygame.draw.rect(self.surface, pygame.Color(*black_color),
                    pygame.Rect(x,y-int(self.square_size/4), int(self.square_size/2)+1, int(self.square_size/2)+1))
            up = True

        if (d_idx >= 0 and d_idx < len(self.state.grid) and
            self.state.grid[d_idx] == PacmanState.WALL):
            pygame.draw.rect(self.surface, pygame.Color(*black_color),
                    pygame.Rect(x,y+int(self.square_size/4), int(self.square_size/2)+1, int(self.square_size/2)+1))
            down = True

        if (l_idx >= 0 and l_idx < len(self.state.grid) and
            self.state.grid[l_idx] == PacmanState.WALL):
            pygame.draw.rect(self.surface, pygame.Color(*black_color),
                    pygame.Rect(x-int(self.square_size/4),y, int(self.square_size/2)+1, int(self.square_size/2)+1))
            left = True

        if (r_idx >= 0 and r_idx < len(self.state.grid) and
            self.state.grid[r_idx] == PacmanState.WALL):
            pygame.draw.rect(self.surface, pygame.Color(*black_color),
                    pygame.Rect(x+int(self.square_size/4),y, int(self.square_size/2)+1, int(self.square_size/2)+1))
            right = True

        if left and up:
            pygame.draw.rect(self.surface, pygame.Color(*black_color), pygame.Rect(x-int(self.square_size/4),
                y-int(self.square_size/4), int(self.square_size/2)+1, int(self.square_size/2)+1))
        if right and up:
            pygame.draw.rect(self.surface, pygame.Color(*black_color), pygame.Rect(x+int(self.square_size/4),
                y-int(self.square_size/4), int(self.square_size/2)+1, int(self.square_size/2)+1))
        if left and down:
            pygame.draw.rect(self.surface, pygame.Color(*black_color), pygame.Rect(x-int(self.square_size/4),
                y+int(self.square_size/4), int(self.square_size/2)+1, int(self.square_size/2)+1))
        if right and down:
            pygame.draw.rect(self.surface, pygame.Color(*black_color), pygame.Rect(x+int(self.square_size/4),
                y+int(self.square_size/4), int(self.square_size/2)+1, int(self.square_size/2)+1))


    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        if msg_type == MsgType.FULL_STATE:
            self.state = msg

    def tick(self):
        # this function will get called in a loop with DISPLAY_FREQUENCY frequency
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop.call_soon(pygame.quit)
                self.loop.stop()
        
        if self.state:
            state = self.state
            if self.state.update_ticks < self.last_tick:
                self._update_dirs()
            ## DRAW STUFF HERE
            # reference the internal state last saved by update
            # It could be None before the client receives its first message
            # hence the if statement

            # This and the Visualizer.update(msg) print calls allow one to see
            # the relative timing of these calls at the curent frequencies
            # just as an illustrative measure of how the system performs
            # you can see how they are simultaneously quite reliable while also
            # not being 100% consistent about when they are called relative to
            # each other
            # print("DRAW:",__import__("time").asctime())

            # Pygame drawing calls shouldn't be too slow, it's basically a
            # Python interface to libraries like SDL, and it's designed for
            # rendering and drawing full games at reasonable refresh rates.
            # We can definitely turn down the refresh rate later if it's
            # a problem for some reason.

            # For the animated objects, i.e. Pacman and the Ghosts, it might
            # make sense to use proper sprites, with assets.
            # I believe proper use of sprites does increase rendering
            # performance slightly.
            self._clear_screen()
            row_idx = 0
            col_idx = 0
            for el in state.grid:
                # ghosts
                if (col_idx, row_idx) == (state.red_ghost.x, state.red_ghost.y):
                    self._print_ghost(Ghosts.RED, state.red_ghost.direction, col_idx, GRID_SIZE[1] - row_idx - 1)

                elif (col_idx, row_idx) == (state.orange_ghost.x, state.orange_ghost.y):
                    self._print_ghost(Ghosts.ORANGE, state.orange_ghost.direction, col_idx, GRID_SIZE[1] - row_idx - 1)

                elif (col_idx, row_idx) == (state.blue_ghost.x, state.blue_ghost.y):
                    self._print_ghost(Ghosts.BLUE, state.blue_ghost.direction, col_idx, GRID_SIZE[1] - row_idx - 1)

                elif (col_idx, row_idx) == (state.pink_ghost.x, state.pink_ghost.y):
                    self._print_ghost(Ghosts.PINK, state.pink_ghost.direction, col_idx, GRID_SIZE[1] - row_idx - 1)

                elif (col_idx, row_idx) == (state.pacman.x, state.pacman.y) and self.print_pacman:
                    self._print_pacman(state.pacman.direction, col_idx, GRID_SIZE[1] - row_idx - 1)

                elif el == PacmanState.PELLET:
                    self._print_pellet(col_idx, GRID_SIZE[1] - row_idx - 1)
                elif el == PacmanState.POWER_PELLET:
                    self._print_power_pellet(col_idx, GRID_SIZE[1] - row_idx - 1)
                elif el == PacmanState.CHERRY:
                    self._print_cherry(col_idx, GRID_SIZE[1] - row_idx - 1)
                elif el == PacmanState.WALL and self.print_walls:
                    self._print_wall(col_idx, row_idx)

                row_idx += 1
                if row_idx >= state.grid_columns:
                    row_idx = 0
                    col_idx += 1

            self._print_score_lives_time(state.score, state.lives, state.elapsed_time)
            #self._print_corners()

            # Yay flipping the entire display all at once for performance!
            y_off = 0 if self.split in [Split.TOP, Split.FULL] else self.y_height
            self.display_surface.blit(self.surface, pygame.Rect(0, -y_off, GRID_SIZE[0]*self.square_size, self.y_height))
            pygame.display.flip()
            self.last_tick = self.state.update_ticks
