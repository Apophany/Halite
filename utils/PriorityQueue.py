import heapq


class PriorityQueue(object):
    def __init__(self, initial=None, key=lambda x: x):
        self.key = key
        self._count = 0

        if initial:
            self._data = [self.__create_vertex__(item) for item in initial]
            heapq.heapify(self._data)
        else:
            self._data = []

    def __create_vertex__(self, item):
        self._count += 1
        return LocationVertex(item, self.key(item), self._count)

    def push(self, item):
        heapq.heappush(self._data, self.__create_vertex__(item))

    def pop(self):
        return heapq.heappop(self._data)

    def empty(self):
        return len(self._data) == 0


class LocationVertex(object):
    def __init__(self, location, priority, vertex_count):
        self.location = location
        self.priority = priority
        self._vertex_count = vertex_count

    def __lt__(self, other):
        if self.priority == other.priority:
            return self._vertex_count < other._vertex_count
        return self.priority < other.priority

    def __str__(self):
        return "[location:%s, priority:%d, vertex_count:%d]" % (self.location.__str__(), self.priority, self._vertex_count)