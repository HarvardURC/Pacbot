import pygame, asyncio
from comm.pacmanState_pb2 import PacmanState
from .variables import *
from .spriteStripAnim import *

class Visualizer:
    def __init__(self, print_walls, print_pacman, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.loop.call_soon(self.draw)

        self.state = None
        self.print_walls = print_walls
        self.print_pacman = print_pacman

        pygame.init()
        # Set up the surface to draw on
        # This should also be used in Visualizer.draw()
        self.surface = pygame.display.set_mode((GRID_SIZE[0]*SQUARE_SIZE, GRID_SIZE[1]*SQUARE_SIZE))
        pygame.display.set_caption("PACBOT")

        self.sprites = {
            'pacman': {
                'r': SpriteStripAnim('graphics/pac.bmp', (453,0,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'l': SpriteStripAnim('graphics/pac.bmp', (455,16,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'u': SpriteStripAnim('graphics/pac.bmp', (456,32,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'd': SpriteStripAnim('graphics/pac.bmp', (455,47,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            },
            'red': {
                'r': SpriteStripAnim('graphics/pac.bmp', (456,64,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'l': SpriteStripAnim('graphics/pac.bmp', (487,64,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'u': SpriteStripAnim('graphics/pac.bmp', (520,64,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'd': SpriteStripAnim('graphics/pac.bmp', (552,64,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            },
            'orange': {
                'r': SpriteStripAnim('graphics/pac.bmp', (456,112,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'l': SpriteStripAnim('graphics/pac.bmp', (487,112,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'u': SpriteStripAnim('graphics/pac.bmp', (520,112,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'd': SpriteStripAnim('graphics/pac.bmp', (552,112,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            },
            'pink': {
                'r': SpriteStripAnim('graphics/pac.bmp', (456,80,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'l': SpriteStripAnim('graphics/pac.bmp', (487,80,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'u': SpriteStripAnim('graphics/pac.bmp', (520,80,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'd': SpriteStripAnim('graphics/pac.bmp', (552,80,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            },
            'blue': {
                'r': SpriteStripAnim('graphics/pac.bmp', (456,96,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'l': SpriteStripAnim('graphics/pac.bmp', (487,96,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'u': SpriteStripAnim('graphics/pac.bmp', (520,96,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY))),
                'd': SpriteStripAnim('graphics/pac.bmp', (552,96,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            },
            'frightened': {
                'r': SpriteStripAnim('graphics/pac.bmp', (584,64,16,16), 2, 1, True, int(1/(SPRITE_FREQUENCY * DISPLAY_FREQUENCY)))
            }
        }

        self.font = pygame.font.Font('graphics/crackman.ttf', int(SQUARE_SIZE))

    def update(self, msg):
        """
        This will be called when a new message is received.

        It should update internal state but not *do* anything.

        This is also a similar model for how the engine will receive data
        from the computer vision.
        """
        # print("UPDATE:",__import__("time").asctime())
        self.state = msg

    def _update_sprites(self):
        for key in self.sprites:
            for dir_key in self.sprites[key]:
                self.sprites[key][dir_key].iter()

    def _clear_screen(self):
        self.surface.fill((0,0,0))

    def _print_score_and_lives(self, score, lives):
        score_surf_1 = self.font.render('score:', True, dark_blue_color)
        self.surface.blit(score_surf_1, (SQUARE_SIZE*23.5, SQUARE_SIZE*11))
        score_surf_2 = self.font.render('{}'.format(score), True, dark_blue_color)
        self.surface.blit(score_surf_2, (SQUARE_SIZE*23.5, SQUARE_SIZE*12))

        lives_surf_1 = self.font.render('lives:', True, dark_blue_color)
        self.surface.blit(lives_surf_1, (SQUARE_SIZE*23.5, SQUARE_SIZE*14))
        lives_surf_2 = self.font.render('{}'.format(lives), True, dark_blue_color)
        self.surface.blit(lives_surf_2, (SQUARE_SIZE*23.5, SQUARE_SIZE*15))


    def _print_ghost(self, mode, color, direction, col_idx, row_idx):
        if color == RED:
            sprite_set = self.sprites['red']
        elif color == ORANGE:
            sprite_set = self.sprites['orange']
        elif color == PINK:
            sprite_set = self.sprites['pink']
        else:
            sprite_set = self.sprites['blue']
        x = int(col_idx * SQUARE_SIZE)
        y = int(row_idx * SQUARE_SIZE)
        if mode == PacmanState.FRIGHTENED:
            self.surface.blit(pygame.transform.scale(self.sprites['frightened']['r'].next(), (SQUARE_SIZE, SQUARE_SIZE)), (x,y))
        elif direction == PacmanState.LEFT:
            self.surface.blit(pygame.transform.scale(sprite_set['l'].next(), (SQUARE_SIZE, SQUARE_SIZE)), (x,y))
        elif direction == PacmanState.RIGHT:
            self.surface.blit(pygame.transform.scale(sprite_set['r'].next(), (SQUARE_SIZE, SQUARE_SIZE)), (x,y))
        elif direction == PacmanState.UP:
            self.surface.blit(pygame.transform.scale(sprite_set['u'].next(), (SQUARE_SIZE, SQUARE_SIZE)), (x,y))
        else:
            self.surface.blit(pygame.transform.scale(sprite_set['d'].next(), (SQUARE_SIZE, SQUARE_SIZE)), (x,y))

    def _print_pacman(self, direction, col_idx, row_idx):
        x = int(col_idx * SQUARE_SIZE)
        y = int(row_idx * SQUARE_SIZE)
        if direction == PacmanState.LEFT:
            self.surface.blit(pygame.transform.scale(self.sprites['pacman']['l'].next(), (SQUARE_SIZE, SQUARE_SIZE)), (x,y))
        elif direction == PacmanState.RIGHT:
            self.surface.blit(pygame.transform.scale(self.sprites['pacman']['r'].next(), (SQUARE_SIZE, SQUARE_SIZE)), (x,y))
        elif direction == PacmanState.UP:
            self.surface.blit(pygame.transform.scale(self.sprites['pacman']['u'].next(), (SQUARE_SIZE, SQUARE_SIZE)), (x,y))
        else:
            self.surface.blit(pygame.transform.scale(self.sprites['pacman']['d'].next(), (SQUARE_SIZE, SQUARE_SIZE)), (x,y))

    def _print_pellet(self, col_idx, row_idx):
        x = int((col_idx + 1) * SQUARE_SIZE - SQUARE_SIZE/2)
        y = int((row_idx + 1) * SQUARE_SIZE - SQUARE_SIZE/2)
        pygame.draw.circle(self.surface, pygame.Color(*white_color), (x,y), int(SQUARE_SIZE/5))

    def _print_power_pellet(self, col_idx, row_idx):
        x = int((col_idx + 1) * SQUARE_SIZE - SQUARE_SIZE/2)
        y = int((row_idx + 1) * SQUARE_SIZE - SQUARE_SIZE/2)
        pygame.draw.circle(self.surface, pygame.Color(*white_color), (x,y), int(SQUARE_SIZE/3))

    def _print_wall(self, col_idx, row_idx):
        u_idx = col_idx * self.state.grid_columns + row_idx + 1 if row_idx < self.state.grid_columns - 1 else - 1
        d_idx = col_idx * self.state.grid_columns + row_idx - 1 if row_idx > 0 else - 1
        r_idx = (col_idx + 1) * self.state.grid_columns + row_idx
        l_idx = (col_idx - 1) * self.state.grid_columns + row_idx

        row_idx = GRID_SIZE[1] - row_idx - 1

        x = int(col_idx * SQUARE_SIZE)
        y = int(row_idx * SQUARE_SIZE)
        pygame.draw.rect(self.surface, pygame.Color(*dark_blue_color), pygame.Rect(x,y, SQUARE_SIZE, SQUARE_SIZE))
        x += int(SQUARE_SIZE/4)
        y += int(SQUARE_SIZE/4)
        pygame.draw.rect(self.surface, pygame.Color(*black_color), pygame.Rect(x,y, int(SQUARE_SIZE/2)+1, int(SQUARE_SIZE/2)+1))

        right = False
        left = False
        up = False
        down = False

        if (u_idx >= 0 and u_idx < len(self.state.grid) and
            self.state.grid[u_idx] == PacmanState.WALL):
            pygame.draw.rect(self.surface, pygame.Color(*black_color),
                    pygame.Rect(x,y-int(SQUARE_SIZE/4), int(SQUARE_SIZE/2)+1, int(SQUARE_SIZE/2)+1))
            up = True

        if (d_idx >= 0 and d_idx < len(self.state.grid) and
            self.state.grid[d_idx] == PacmanState.WALL):
            pygame.draw.rect(self.surface, pygame.Color(*black_color),
                    pygame.Rect(x,y+int(SQUARE_SIZE/4), int(SQUARE_SIZE/2)+1, int(SQUARE_SIZE/2)+1))
            down = True

        if (l_idx >= 0 and l_idx < len(self.state.grid) and
            self.state.grid[l_idx] == PacmanState.WALL):
            pygame.draw.rect(self.surface, pygame.Color(*black_color),
                    pygame.Rect(x-int(SQUARE_SIZE/4),y, int(SQUARE_SIZE/2)+1, int(SQUARE_SIZE/2)+1))
            left = True

        if (r_idx >= 0 and r_idx < len(self.state.grid) and
            self.state.grid[r_idx] == PacmanState.WALL):
            pygame.draw.rect(self.surface, pygame.Color(*black_color),
                    pygame.Rect(x+int(SQUARE_SIZE/4),y, int(SQUARE_SIZE/2)+1, int(SQUARE_SIZE/2)+1))
            right = True

        if left and up:
            pygame.draw.rect(self.surface, pygame.Color(*black_color), pygame.Rect(x-int(SQUARE_SIZE/4),
                y-int(SQUARE_SIZE/4), int(SQUARE_SIZE/2)+1, int(SQUARE_SIZE/2)+1))
        if right and up:
            pygame.draw.rect(self.surface, pygame.Color(*black_color), pygame.Rect(x+int(SQUARE_SIZE/4),
                y-int(SQUARE_SIZE/4), int(SQUARE_SIZE/2)+1, int(SQUARE_SIZE/2)+1))
        if left and down:
            pygame.draw.rect(self.surface, pygame.Color(*black_color), pygame.Rect(x-int(SQUARE_SIZE/4),
                y+int(SQUARE_SIZE/4), int(SQUARE_SIZE/2)+1, int(SQUARE_SIZE/2)+1))
        if right and down:
            pygame.draw.rect(self.surface, pygame.Color(*black_color), pygame.Rect(x+int(SQUARE_SIZE/4),
                y+int(SQUARE_SIZE/4), int(SQUARE_SIZE/2)+1, int(SQUARE_SIZE/2)+1))

    def draw(self):
        self.loop.call_later(DISPLAY_FREQUENCY, self.draw)
        # I'm assuming we don't need to process any input via pygame here
        # This call is still necessarily to make the window manager happy
        # This has to be called regularly once the window is open or the
        # system will think the program has frozen.
        pygame.event.pump()

        if self.state:
            state = self.state
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
                    self._print_ghost(state.mode, RED, state.red_ghost.direction, col_idx, GRID_SIZE[1] - row_idx - 1)

                elif (col_idx, row_idx) == (state.orange_ghost.x, state.orange_ghost.y):
                    self._print_ghost(state.mode, ORANGE, state.orange_ghost.direction, col_idx, GRID_SIZE[1] - row_idx - 1)

                elif (col_idx, row_idx) == (state.blue_ghost.x, state.blue_ghost.y):
                    self._print_ghost(state.mode, BLUE, state.blue_ghost.direction, col_idx, GRID_SIZE[1] - row_idx - 1)

                elif (col_idx, row_idx) == (state.pink_ghost.x, state.pink_ghost.y):
                    self._print_ghost(state.mode, PINK, state.pink_ghost.direction, col_idx, GRID_SIZE[1] - row_idx - 1)

                elif (col_idx, row_idx) == (state.pacman.x, state.pacman.y) and self.print_pacman:
                    self._print_pacman(state.pacman.direction, col_idx, GRID_SIZE[1] - row_idx - 1)

                elif el == PacmanState.PELLET:
                    self._print_pellet(col_idx, GRID_SIZE[1] - row_idx - 1)
                elif el == PacmanState.POWER_PELLET:
                    self._print_power_pellet(col_idx, GRID_SIZE[1] - row_idx - 1)
                elif el == PacmanState.WALL and self.print_walls:
                    self._print_wall(col_idx, row_idx)

                row_idx += 1
                if row_idx >= state.grid_columns:
                    row_idx = 0
                    col_idx += 1

            self._print_score_and_lives(state.score, state.lives)


            # Yay flipping the entire display all at once for performance!
            pygame.display.flip()
