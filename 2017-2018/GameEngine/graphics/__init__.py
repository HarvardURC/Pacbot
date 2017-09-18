
import pygame, asyncio

DISPLAY_FREQUENCY = 1/60 # 60 Hz

class Visualizer:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.loop.call_soon(self.draw)

        self.state = None
        
        pygame.init()
        # Set up the surface to draw on
        # This should also be used in Visualizer.draw()
        self.surface = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("PACBOT")
        
    def update(self, msg):
        """
        This will be called when a new message is received.

        It should update internal state but not *do* anything.

        This is also a similar model for how the engine will receive data
        from the computer vision.
        """
        # print("UPDATE:",__import__("time").asctime())
        self.state = msg

    def draw(self):
        self.loop.call_later(DISPLAY_FREQUENCY, self.draw)
        # I'm assuming we don't need to process any input via pygame here
        # This call is still necessarily to make the window manager happy
        # This has to be called regularly once the window is open or the
        # system will think the program has frozen.
        pygame.event.pump()

        if self.state:
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

            # Yay flipping the entire display all at once for performance!
            pygame.display.flip()
