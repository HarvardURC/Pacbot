from flask import Flask, jsonify
from json import dumps
import copy
from threading import Thread, Lock, Timer
import time
import sys
import select
import curses
from pynput import keyboard

STOP = 0
FORWARD = 1
BACK = 2
LEFT = 3
RIGHT = 4

cur_dir = 0

app = Flask("Pacman")

@app.route('/pac-bot')
def pacBot():
    return ("${}".format(str(cur_dir))) #jsonify(getFormattedData())

def getFormattedData():
    response = {}
    response['action'] = cur_dir
    return response

# def main():
#     Thread(target = appRunner).start()


def appRunner():
    app.run(host="0.0.0.0", port=8080)

def on_press(key):
    global cur_dir
    if key.char == 'w':
        cur_dir = 1
    elif key.char == 's':
        cur_dir = 2
    elif key.char == 'a':
        cur_dir = 3
    elif key.char == 'd':
        print("got here")
        cur_dir = 4
    # try:
    #     print('alphanumeric key {0} pressed'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(
    #         key))

def on_release(key):
    global cur_dir
    print('key released')
    cur_dir = 0
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# def input(stdscr):
#     global cur_dir
#     # do not wait for input when calling getch
#     stdscr.nodelay(1)
#     while True:
#         # get keyboard input, returns -1 if none available
#         c = stdscr.getch()
#         if c != -1:
#             # print numeric value
#             stdscr.addstr(str(c) + ' ')
#             stdscr.refresh()
#             # return curser to start position
#             stdscr.move(0, 0)
#         else:
#             stdscr.addstr('   ')
#             stdscr.refresh()
#             # return curser to start position
#             stdscr.move(0, 0)

if __name__ == '__main__':
    global cur_dir
    Thread(target = appRunner).start()
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
               listener.join()
    # curses.wrapper(input)



