import queue


class Edge:
    '''Класс ребра графа'''
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w


class Graph:
    '''Класс графа'''
    def __init__(self, directed=False, adj_list=None):
        self.adj_list = {} if adj_list is None else adj_list
        self.directed = directed

    def add_vertex(self, vertex):
        '''Добавляет вершину в граф'''
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, edge):
        '''Добавляет ребро в граф'''
        if edge.u not in self.adj_list:
            self.adj_list[edge.u] = (edge.v, edge.w)
        else:
            self.adj_list[edge.u].append((edge.v, edge.w))
        if not self.directed:
            if edge.u not in self.adj_list:
                self.adj_list[edge.v] = (edge.u, edge.w)
            else:
                self.adj_list[edge.v].append((edge.u, edge.w))

    def vertices(self):
        '''Выводит список вершин графа'''
        return list(self.adj_list.keys())

    def get_adjacent(self, vertix):
        '''Выводит информацию о вершинах, смежных с vertix'''
        return list(self.adj_list[vertix])

    @staticmethod
    def from_file(filename):
        '''Считывает граф из файла с названием filename'''
        graph = Graph()
        with open(filename) as f:
            graph.directed = f.readline() == 'directed\n'
            for vertex in f.readline().split():
                graph.add_vertex(vertex)
            while True:
                line = f.readline()
                if not line:
                    break
                edge = Edge(*line.split())
                edge.w = int(edge.w)
                graph.add_edge(edge)
        return graph


class PriorityQueue:
    def __init__(self):
        self._queue = queue.PriorityQueue()

    def put(self, priority, value):
        '''Кладёт в очередь элемент (priority, value)'''
        self._queue.put((priority, value))

    def get(self):
        '''Достаёт и возвращает value элемента очереди с наименьшим priority'''
        return self._queue.get()[1]

    def empty(self):
        '''Проверяет очередь на пустоту'''
        return self._queue.empty()


class PathFinder:
    '''Базовый класс искателя кратчайшего пути в графе'''
    def __init__(self, graph):
        self.graph = graph
        self.prev = {}
        self.costs = {}
        self.validate_graph()

    def get_path(self, start, goal):
        '''Возвращает кратчайший путь от start к goal'''
        self.__init__(self.graph)
        self.find_paths(start)
        if start == goal and start in self.graph.vertices():
            return [], 0
        if goal not in self.prev:
            return None, None
        path = []
        current = goal
        while current in self.prev:
            path.append(current)
            current = self.prev[current]
        path.append(current)
        return path[::-1], self.costs[goal]


class DijkstraPathFinder(PathFinder):
    '''Искатель кратчайшего пути в графе, использует алгоритм Дейкстры'''
    def validate_graph(self):
        '''Проверяет применимость алгоритма поиска пути для данного графа'''
        for to in self.graph.adj_list.values():
            for edge_dest, edge_cost in to:
                assert edge_cost >= 0, ('Веса рёбер переданного графа'
                                        'должны быть неотрицательными')
        return True

    def find_paths(self, start):
        '''Находит кратчайшие пути от start к остальным вершинам'''
        self.costs[start] = 0
        queue = PriorityQueue()
        queue.put(self.costs[start], start)
        while not queue.empty():
            current = queue.get()
            for adj_id, edge_cost in self.graph.get_adjacent(current):
                adj_cost = self.costs[current] + edge_cost
                if adj_id not in self.costs or adj_cost < self.costs[adj_id]:
                    self.costs[adj_id] = adj_cost
                    self.prev[adj_id] = current
                    queue.put(adj_cost, adj_id)


class SPFAPathFinder(PathFinder):
    '''Искатель кратчайшего пути в графе, использует SPFA'''
    def validate_graph(self):
        '''Проверяет применимость алгоритма поиска пути для данного графа'''
        check_negative_cycles(self.graph)

    def find_paths(self, start):
        '''Находит кратчайшие пути от start к остальным вершинам'''
        enqueued = {start}
        self.costs[start] = 0
        nodes = queue.Queue()
        nodes.put(start)
        enqueued.add(nodes)
        while not nodes.empty():
            current = nodes.get()
            enqueued.remove(current)
            for adj_id, edge_cost in self.graph.get_adjacent(current):
                adj_cost = self.costs[current] + edge_cost
                if adj_id not in self.costs or adj_cost < self.costs[adj_id]:
                    self.costs[adj_id] = adj_cost
                    self.prev[adj_id] = current
                    if adj_id not in enqueued:
                        nodes.put(adj_id)
                        enqueued.add(adj_id)


class LevitPathFinder(PathFinder):
    '''Искатель кратчайшего пути в графе, использует алгоритм Левита'''
    def validate_graph(self):
        '''Проверяет применимость алгоритма поиска пути для данного графа'''
        check_negative_cycles(self.graph)

    def find_paths(self, start):
        '''Находит кратчайшие пути от start к остальным вершинам'''
        calculated = set()
        enqueued = {start}
        self.costs[start] = 0
        queue1 = queue.Queue()
        queue1.put(start)
        queue2 = queue.Queue()
        while not queue1.empty() or not queue2.empty():
            if not queue2.empty():
                current = queue2.get()
            else:
                current = queue1.get()
            enqueued.remove(current)
            calculated.add(current)
            for adj_id, edge_cost in self.graph.get_adjacent(current):
                adj_cost = self.costs[current] + edge_cost
                if adj_id not in self.costs or adj_cost < self.costs[adj_id]:
                    self.costs[adj_id] = adj_cost
                    self.prev[adj_id] = current
                    if adj_id in calculated:
                        calculated.remove(adj_id)
                        queue2.put(adj_id)
                        enqueued.add(adj_id)
                    elif adj_id not in enqueued:
                        queue1.put(adj_id)
                        enqueued.add(adj_id)


class MultiPathFinder:
    def __init__(self, graph, PathFinderClass=DijkstraPathFinder):
        self.pathfinder = PathFinderClass(graph)

    def delete(self, vertix):
        if vertix in self.pathfinder.graph.adj_list:
            self.deleted[vertix] = self.pathfinder.graph.adj_list[vertix]
            self.pathfinder.graph.adj_list[vertix] = []

    def rollback(self, vertix):
        if vertix in self.deleted:
            self.pathfinder.graph.adj_list[vertix] = self.deleted.pop(vertix)

    def store(self, vertices):
        for vertix in vertices:
            self.delete(vertix)

    def restore(self, vertices):
        for vertix in vertices:
            self.rollback(vertix)

    def get_path(self, *vertices):
        path = []
        cost = 0
        self.deleted = {}
        self.store(vertices)
        self.rollback(vertices[0])
        for u, v in zip(vertices, vertices[1:]):
            self.rollback(v)
            if path:
                path.pop()
            info = self.pathfinder.get_path(u, v)
            if info == (None, None):
                path = cost = None
                break
            path += info[0]
            cost += info[1]
            self.delete(u)
        self.restore(vertices)
        return path, cost


def check_negative_cycles(graph):
    n = len(graph.vertices())
    enqueued = set()
    costs = {}
    dist = {}
    nodes = queue.Queue()
    for vertix in graph.vertices():
        enqueued.add(vertix)
        costs[vertix] = 0
        dist[vertix] = 0
        nodes.put(vertix)
    while not nodes.empty():
        current = nodes.get()
        enqueued.remove(current)
        for adj_id, edge_cost in graph.get_adjacent(current):
            adj_cost = costs[current] + edge_cost
            if adj_cost < costs[adj_id]:
                dist[adj_id] = dist[current] + 1
                assert dist[adj_id] < n, \
                    'В переданном графе не должно быть отрицательных циклов'
                costs[adj_id] = adj_cost
                if adj_id not in enqueued:
                    nodes.put(adj_id)
                    enqueued.add(adj_id)
