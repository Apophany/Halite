import math

import game_files.debug.hlt_debug as hlt
from game_files.debug.hlt_debug import NORTH, EAST, SOUTH, WEST, STILL, Move
from utils.PriorityQueue import PriorityQueue

myID, game_map = hlt.get_init()
hlt.send_init("BfsBot")


def get_direction(l1, l2):
    angle = game_map.getAngle(l1, l2) * (180 / math.pi)
    if angle < 0.0:
        angle += 360.0

    direction = EAST
    if 45 < angle <= 135:
        direction = SOUTH
    elif 135 < angle <= 225:
        direction = WEST
    elif 225 < angle <= 315:
        direction = NORTH

    return direction


def initialise_friendly_sites():
    global explored
    explored = [[False for x in range(game_map.width)] for y in range(game_map.height)]


def find_nearest_enemy_bfs(start):
    direction = NORTH

    p_queue = PriorityQueue(key=lambda square: game_map.get_distance(start, square))

    p_queue.push(start)
    explored[start.y][start.x] = start

    while not p_queue.empty():
        vertex = p_queue.pop()

        current_square = vertex.square

        if current_square.owner != myID:
            return get_direction(start, current_square)

        for neighbour in game_map.neighbors(current_square):
            if not explored[neighbour.y][neighbour.x]:
                explored[neighbour.y][neighbour.x] = True
                p_queue.push(neighbour)

    return direction


def get_move(square):
    _, direction = next(
        (
            (neighbor.strength, direction)
            for direction, neighbor
            in enumerate(game_map.neighbors(square))
            if neighbor.owner != myID
               and neighbor.strength < square.strength
        ),
        (None, None)
    )

    if direction is not None:
        return Move(square, direction)
    elif square.strength < square.production * 5:
        return Move(square, STILL)

    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))
    if not border:
        return Move(square, find_nearest_enemy_bfs(square))
    else:
        return Move(square, STILL)


while True:
    game_map.get_frame()
    initialise_friendly_sites()
    moves = [get_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
