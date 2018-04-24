#!/usr/bin/env python3
import Encoder

def main():
    Encoder.init(4,14)
    while True:
        print(Encoder.read())

if __name__ == "__main__":
    main()
