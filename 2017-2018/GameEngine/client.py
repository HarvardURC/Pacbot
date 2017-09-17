import socket, struct, sys, time
import pacmanState_pb2

MAGIC_HEADER = 11297
SIZE_HEADER = struct.Struct("!HH")

class EngineClient:
    """
    socket-based client for the game engine
    """
    
    def __init__(self, addr, port):
        """
        Takes the address and port of the server to connect to.
        """
        self.addr = addr
        self.port = port

    def connect(self):
        """
        Create the underlying socket and connect to the server.
        """
        self.s = socket.socket()
        self.s.connect((self.addr, self.port))
        self.s.setblocking(False)

    def __read_data(self, size):
        data = b""
        while len(data) < size:
            try:
                data += self.s.recv(size - len(data))
            except BlockingIOError:
                time.sleep(0.05)
        return data
        
    def read_msg(self):
        """
        Read a message from the socket and return it.
        This function is allowed to return None if it cannot read a message.

        This function is currently blocking, i.e. it will not return until
        it has read a message or reached an error condition.

        It is important to call this function often, otherwise messages may
        overflow the socket's buffer.

        Currently, the biggest downside of this implmentation is that it does
        not detect if the connection is dropped, it just waits forever.
        """
        magic, length = SIZE_HEADER.unpack(self.__read_data(SIZE_HEADER.size))
        if magic != MAGIC_HEADER:
            # Uh oh, what happened?
            self.s.close()
            print("Magic number mismatched, reconnecting...",
                  file=sys.stderr)
            self.connect()
            return
        msg = pacmanState_pb2.PacmanState()
        msg.ParseFromString(self.__read_data(length))
        return msg

    # Whee, context managers
    __enter__ = connect
    def __exit__(self, *args):
        self.s.close()
