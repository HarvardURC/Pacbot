import os
import robomodules as rm
import variables as var
from grid import grid
from low_level.motors import Motors
from low_level.motors import Direction
from messages import MsgType, message_buffers, LightState, PacmanCommand
import threading
from time import sleep
ADDRESS = os.environ.get("LOCAL_ADDRESS","192.168.0.101")
PORT = os.environ.get("LOCAL_PORT", 11295)

FREQUENCY = 1 # was 10

GRID_VAL = 200

class CommandExecution():
    def __init__():
        self.motors = Motors()
        self.current_command = None
    
    def _execute_command(self):
        if self.current_command:
            cmd = self.current_command
            self.current_command = None
            
            if cmd == PacmanCommand.STOP:
                self.motors.stop()
                return

            if cmd == PacmanCommand.NORTH:
                motor_dir = Direction.N
                print("N")
            elif cmd == PacmanCommand.SOUTH:
                motor_dir = Direction.S
                print("S")
            elif cmd == PacmanCommand.WEST:
                motor_dir = Direction.W
                print("W")
            else:
                motor_dir = Direction.E
                print("E")
            
            self.motors.drive_in_direction(motor_dir, 1)

    def kill(self):
        self.motors.stop()

    def getCurrentCommand(self):
        with open('command.txt', "r") as myfile:
            command = myfile.read()
            if command == "N":
                self.current_command = PacmanCommand.NORTH
            elif command == "W":
                self.current_command = PacmanCommand.WEST
            elif command == "S":
                self.current_command = PacmanCommand.SOUTH
            elif command == "E":
                self.current_command = PacmanCommand.EAST
            elif command == "0":
                self.current_command = PacmanCommand.STOP
            else:
                self.current_command = None


    def tick_thread(self):
        while 1:
            self.getCurrentCommand()
            if self.current_command:
                self._execute_command()
            else:
                if(self.motors.detectWalls()):
                    self.kill()

def main():
    module = CommandExecution()
    try:
        module.tick_thread()
    except KeyboardInterrupt:
        module.kill()


if __name__ == "__main__":
    main()
