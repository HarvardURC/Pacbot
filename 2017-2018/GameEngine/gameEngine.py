from gameState import GameState
import time, os, sys, struct
import asyncio # minimum Python 3.4, changed in 3.5.1
from stateConverter import StateConverter
from variables import game_frequency

ADDRESS = os.environ.get("BIND_ADDRESS","")
PORT = os.environ.get("BIND_PORT", 11297)

# Message sizes are communicated as a single unsigned short
# encoded using network byte-order (big-endian).
# receiving libraries will need to account for this properly.
# The header also includes a magic number (also a short) for verification
MAGIC_HEADER = 11297
SIZE_HEADER = struct.Struct("!HH")

class GameEngine:
    def __init__(self, loop):
        self.game = GameState()
        self.loop = loop
        self.clients = []
        
        coro = asyncio.start_server(self._add_client, ADDRESS, PORT)
        self.server = loop.run_until_complete(coro)
        
        self.loop.add_reader(sys.stdin, self.keypress)
        self.loop.call_soon(self.game_tick)

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.quit()
            
    def _add_client(self, reader, writer):
        self.clients.append(writer)
        
    def game_tick(self):
        if self.game.play:
            # update_pacbot_pos
            # This will become asynchronous
            self.game.next_step()
            self._write_state()
        self.loop.call_later(1.0/game_frequency, self.game_tick)

    def quit(self):
        self.loop.stop()
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()

    def _write_state(self):
        protobuf = StateConverter.convert_game_state_to_proto(self.game)
        msg = protobuf.SerializeToString()
        length = SIZE_HEADER.pack(MAGIC_HEADER, len(msg))
        for i in self.clients:
            if i.transport.is_closing():
                self.clients.remove(i)
            else:
                i.write(length)
                i.write(msg)

    def keypress(self):
        char = sys.stdin.read(1)
        if char == "r":
            self.game.restart()
        elif char == "p":
            self.game.play = not self.game.play
        elif char == "q":
            self.quit()
        
def main():
    loop = asyncio.get_event_loop()
    engine = GameEngine(loop)

    if os.name != "nt" and os.environ.get("CURSES", False):
        # Make the input reading nicer if not on windows
        # This pretty much breaks any output, though
        import curses, atexit
        curses.initscr()
        curses.cbreak()
        curses.noecho()
        atexit.register(lambda: (curses.nocbreak(),
                                 curses.echo(),
                                 curses.endwin()))

    engine.run()

if __name__ == "__main__":
    main()
