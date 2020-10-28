#!/usr/bin/env python3

from distutils.core import setup
from distutils.extension import Extension

def main():
    setup(name = 'Encoder', version = '1.0',  ext_modules = [Extension('Encoder',libraries = ['pigpio'], sources = ['encoder.c'])])

if __name__ == "__main__":
    main()
