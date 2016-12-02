from game_files.networking import *

myID, gameMap = getInit()
sendInit("TheConnor")


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
        return Move(location, find_nearest_enemy(location))

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
