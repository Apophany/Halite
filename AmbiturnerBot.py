from game_files import hlt
from game_files.hlt import NORTH, EAST, SOUTH, WEST, STILL, Move

myID, game_map = hlt.get_init()
hlt.send_init("AmbiturnerBot")


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
        return Move(square, find_nearest_enemy(square))
    else:
        return Move(square, STILL)


while True:
    game_map.get_frame()
    moves = [get_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
