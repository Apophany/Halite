from game_files.networking import *
from utils import timer
from utils.PriorityQueue import PriorityQueue

myID, gameMap = getInit()
# timer.setup(myID)
sendInit("TheConnor")


def get_direction(l1, l2):
    angle = gameMap.getAngle(l1, l2) * (180 / math.pi)
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


def find_nearest_enemy_bfs(start_loc):
    direction = NORTH

    explored = [[False for x in range(gameMap.width)] for y in range(gameMap.height)]

    p_queue = PriorityQueue(key=lambda loc: gameMap.getDistance(start_loc, loc))

    p_queue.push(start_loc)
    explored[start_loc.y][start_loc.x] = start_loc

    while not p_queue.empty():
        vertex = p_queue.pop()

        current_loc = vertex.location
        current_site = gameMap.getSite(current_loc)

        if current_site.owner != myID:
            return get_direction(start_loc, current_loc)

        for d in CARDINALS:
            neighbour_loc = gameMap.getLocation(current_loc, d)

            if not explored[neighbour_loc.y][neighbour_loc.x]:
                explored[neighbour_loc.y][neighbour_loc.x] = True
                p_queue.push(neighbour_loc)

    return direction


# @timer.timeit
def find_nearest_enemy(location):
    direction = NORTH
    max_distance = min(gameMap.width, gameMap.height) / 2

    for d in CARDINALS:
        distance = 0
        current_location = location

        current_site = gameMap.getSite(current_location, d)

        while current_site.owner == myID and distance < max_distance:
            distance += 1
            current_location = gameMap.getLocation(current_location, d)
            current_site = gameMap.getSite(current_location)

        if distance < max_distance:
            direction = d
            max_distance = distance

    return direction


def move(location):
    site = gameMap.getSite(location)

    border = False
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        if not neighbour_site.owner == myID:
            border = True
            if neighbour_site.strength < site.strength:
                return Move(location, d)

    if site.strength < site.production * 5:
        return Move(location, STILL)

    if not border:
        return Move(location, find_nearest_enemy_bfs(location))

    return Move(location, STILL)


while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
    sendFrame(moves)
