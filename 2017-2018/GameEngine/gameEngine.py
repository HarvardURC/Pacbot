from gameState import GameState
import time, os, sys, struct, logging
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
        self.server.close()
        self.loop.stop()

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
        # For some reason I couldn't quite get this to do what I wanted
        # Still it's a bit cleaner than otherwise
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        sys.stdout.flush()
        if char == "r":
            logging.info("Restarting...")
            self.game.restart()
            self._write_state()
        elif char == "p":
            if (self.game.play):
                logging.info('Game is paused')
            else:
                logging.info('Game resumed')
            self.game.play = not self.game.play
        elif char == "q":
            logging.info("Quitting...")
            self.quit()
        
def main():
    # logger automatically adds timestamps
    # I wanted it to print each sequentially but it did not want to
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s',
                        datefmt="%I:%M:%S %p")
    loop = asyncio.get_event_loop()
    engine = GameEngine(loop)
    print('Game is paused.')
    print('Controls:')
    print('    r - restart')
    print('    p - (un)pause')
    print('    q - quit')

    engine.run()

if __name__ == "__main__":
    main()
