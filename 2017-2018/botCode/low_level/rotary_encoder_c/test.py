import Encoder
from threading import Thread

def init():
    Encoder.init()

thread = Thread(target = init)
thread.start()

while True:
    print(Encoder.read())
