from game_files.hlt import *
import socket
import traceback
import struct
from ctypes import *
import sys

_connection = None


def send_string(s):
    global _connection
    s += '\n'
    _connection.sendall(bytes(s, 'ascii'))


def get_string():
    global _connection
    newString = ""
    buffer = '\0'
    while True:
        buffer = _connection.recv(1).decode('ascii')
        if buffer != '\n':
            newString += str(buffer)
        else:
            return newString


def get_init():
    # Connect to environment.
    global _connection
    _connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(input('Enter the port on which to connect: '))
    _connection.connect(('localhost', port))
    print('Connected to intermediary on port #' + str(port))

    playerID = int(get_string())
    m = GameMap(get_string(), get_string())
    return playerID, m


def send_init(name):
    send_string(name)


def translate_cardinal(direction):
    "Translate direction constants used by this Python-based bot framework to that used by the official Halite game environment."
    # Cardinal indexing used by this bot framework is
    # ~ NORTH = 0, EAST = 1, SOUTH = 2, WEST = 3, STILL = 4
    # Cardinal indexing used by official Halite game environment is
    # ~ STILL = 0, NORTH = 1, EAST = 2, SOUTH = 3, WEST = 4
    # ~ >>> list(map(lambda x: (x+1) % 5, range(5)))
    # ~ [1, 2, 3, 4, 0]
    return (direction + 1) % 5


def send_frame(moves):
    send_string(' '.join(
        str(move.square.x) + ' ' + str(move.square.y) + ' ' + str(translate_cardinal(move.direction)) for move in
        moves))
