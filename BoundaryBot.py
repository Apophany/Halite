import math
import sys

import game_files.hlt as hlt
from game_files.hlt import NORTH, EAST, SOUTH, WEST, STILL, Move

myID, game_map = hlt.get_init()
hlt.send_init("BoundaryBot")


def get_direction(s1, s2):
    angle = game_map.getAngle(s1, s2) * (180 / math.pi)
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


def initialise_boundary_enemies():
    global boundary_enemies
    boundary_enemies = [
        enemy for enemy in game_map if
        any([neighbour.owner == myID for neighbour in game_map.neighbors(enemy)])
        and enemy.owner != myID
    ]


def find_nearest_enemy(start):
    closest_enemy = None
    closest_distance = sys.maxsize

    for enemy in boundary_enemies:
        current_distance = game_map.get_distance(start, enemy)

        if current_distance < closest_distance:
            closest_enemy = enemy
            closest_distance = current_distance
        elif closest_distance == current_distance:
            if prod_per_strength(enemy) > prod_per_strength(closest_enemy):
                closest_enemy = enemy

    return get_direction(start, closest_enemy)


def prod_per_strength(square):
    if square.strength == 0:
        return sys.maxsize
    return int(square.production / square.strength)


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
        return Move(square, find_nearest_enemy(square))
    else:
        return Move(square, STILL)


while True:
    game_map.get_frame()
    initialise_boundary_enemies()

    moves = [get_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
