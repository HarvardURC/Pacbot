import Encoder
from threading import Thread

def init():
    Encoder.init(4,14)

thread = Thread(target = init)
thread.start()

while True:
    print(Encoder.read())
