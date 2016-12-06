###############################################################
# Functions for communicating with the Halite game environment#
###############################################################
import sys

from game_files.hlt import GameMap


def send_string(s):
    sys.stdout.write(s)
    sys.stdout.write('\n')
    sys.stdout.flush()


def get_string():
    return sys.stdin.readline().rstrip('\n')


def get_init():
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
