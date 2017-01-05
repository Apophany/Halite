import math
import hlt as hlt

from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move
from utils.PriorityQueue import PriorityQueue

myID, game_map = hlt.get_init()
hlt.send_init("TheConnor")


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


def find_nearest_enemy_bfs(start):
    direction = NORTH

    explored = [[False for x in range(game_map.width)] for y in range(game_map.height)]

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


# @timer.timeit
def find_nearest_enemy(square):
    direction = NORTH
    max_distance = min(game_map.width, game_map.height) / 2

    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current_square = square

        while current_square.owner == myID and distance < max_distance:
            distance += 1
            current_square = game_map.get_target(current_square, d)

        if distance < max_distance:
            direction = d
            max_distance = distance

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
    moves = [get_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
