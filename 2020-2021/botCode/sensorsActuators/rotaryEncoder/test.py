#!/usr/bin/env python3
import Encoder
from time import sleep

def main():
    Encoder.init(4,14, 0)
    Encoder.init(15,17, 1)
    while True:
        sleep(0.5)
        print('{}:{}'.format(Encoder.read(0), Encoder.read(1)))

if __name__ == "__main__":
    main()
