#!/usr/bin/env python3

from pacbot.gameState import GameState
import time, os, sys, logging
import asyncio # minimum Python 3.4, changed in 3.5.1
from comm.stateConverter import StateConverter
from comm.asyncproto import AsyncProto
from comm.pacmanState_pb2 import PacmanState
from comm import pack_msg
from pacbot.variables import game_frequency

ADDRESS = os.environ.get("BIND_ADDRESS","")
PORT = os.environ.get("BIND_PORT", 11297)
INPUT_PORT = os.environ.get("INPUT_PORT", 11295)

class GameEngine(AsyncProto):
    def __init__(self, loop):
        self.game = GameState()
        self.loop = loop
        self.clients = []
        
        coro = asyncio.start_server(self._add_client, ADDRESS, PORT)
        self.server = loop.run_until_complete(coro)
        coro = loop.create_server(lambda: self, ADDRESS, INPUT_PORT)
        self.input_server = loop.run_until_complete(coro)
        
        self.loop.add_reader(sys.stdin, self.keypress)
        self.loop.call_soon(self.game_tick)

    def msg_received(self, data):
        """
        This function will be called with the raw binary data when a new
        message is received from the vision client.
        """
        # parse data into a message
        pos = PacmanState.Position()
        pos.ParseFromString(data)
        self.game.pacbot.update((pos.x, pos.y))
        
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
        msg = pack_msg(protobuf.SerializeToString())
        for i in self.clients:
            if i.transport.is_closing():
                self.clients.remove(i)
            else:
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
