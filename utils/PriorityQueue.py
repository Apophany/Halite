import heapq
import itertools

WHITE = 'white'
GREY = 'grey'
BLACK = 'black'


class PriorityQueue(object):
    def __init__(self, initial=None, key=lambda x: x):
        self.key = key
        self._count = itertools.count()

        if initial:
            self._data = [self.__create_item__(item) for item in initial]
            heapq.heapify(self._data)
        else:
            self._data = []

    def __create_item__(self, item):
        self._count += 1
        return LocationVertex(item, self.key(item), self._count, WHITE)

    def push(self, item):
        heapq.heappush(self._data, self.__create_item__(item))

    def pop(self):
        return heapq.heappop(self._data)[1]

    def empty(self):
        return len(self._data) == 0


class LocationVertex(object):
    def __init__(self, location, priority, vertex_count, color):
        self.location = location
        self.priority = priority
        self.color = color
        self._vertex_count = vertex_count

    def __lt__(self, other):
        if self.priority == other.priority:
            return self._vertex_count < other._vertex_count
        return self.priority < other.priority
