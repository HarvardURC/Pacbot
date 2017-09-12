from gameState import GameState
import time, os, sys
import asyncio # minimum Python 3.4, changed in 3.5.1
from stateConverter import StateConverter
from variables import game_frequency

ADDRESS = os.environ.get("BIND_ADDRESS","")
PORT = os.environ.get("BIND_PORT", 11297)

class GameEngine:
    def __init__(self, loop):
        self.game = GameState()
        self.playing = False
        self.loop = loop
        
        self.loop.add_reader(sys.stdin, self.keypress)
        self.loop.call_soon(self.game_tick)
        
    def game_tick(self):
        if self.playing:
            # update_pacbot_pos
            # This will become asynchronous
            self.game.next_step()
            self._write_state()
        self.loop.call_later(1.0/game_frequency, self.game_tick)

    def quit(self):
        # self.cleanup()
        self.loop.stop()

    def restart(self):
        self.playing = False
        self.game.restart()

    def _write_state(self):
        protobuf = StateConverter.convert_game_state_to_proto(self.game)

    def keypress(self):
        char = sys.stdin.read(1)
        if char == "r":
            self.restart()
        elif char == "p":
            self.playing = not self.playing
        elif char == "q":
            self.quit()
        
def main():
    loop = asyncio.get_event_loop()
    engine = GameEngine(loop)

    if os.name != "nt" and os.environ.get("CURSES", False):
        # Make the input reading nicer if not on windows
        import curses, atexit
        curses.initscr()
        curses.cbreak()
        curses.noecho()
        atexit.register(lambda: (curses.nocbreak(),
                                 curses.echo(),
                                 curses.endwin()))

    loop.run_forever()

if __name__ == "__main__":
    main()
