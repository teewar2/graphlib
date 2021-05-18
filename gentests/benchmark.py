import csv
import functools
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from graphlib import pathfinder


ALGOS = [
    pathfinder.DijkstraPathFinder,
    pathfinder.SPFAPathFinder,
    pathfinder.LevitPathFinder,
    pathfinder.MultiPathFinder,
]
MEASURE_REPETITIONS_COUNT = 20
N = 6
T = 2.5706
TESTS_COUNT = 100


class Test:
    def __init__(self, filename):
        self.graph = pathfinder.Graph.from_file(filename)
        self.start_goal_vertices = ('1', '2')


def measure(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(5):
            func(*args, **kwargs)
        t1 = time.perf_counter()
        for i in range(MEASURE_REPETITIONS_COUNT):
            func(*args, **kwargs)
        t2 = time.perf_counter()
        return (t2 - t1) / MEASURE_REPETITIONS_COUNT

    return wrapper


@measure
def run(algo, test):
    finder = algo(test.graph)
    finder.get_path(*test.start_goal_vertices)


def make_measurement_stat(algo, test):
    elapsed_times = [run(algo, test) for _ in range(N)]
    mean_time = sum(elapsed_times) / N
    sq = 0
    for t in elapsed_times:
        sq += (t - mean_time) ** 2
    s = (sq / (N - 1)) ** 0.5
    delta = T * s / N ** 0.5
    return delta, mean_time


def warmup(test):
    for i in range(5):
        run(ALGOS[0], test)


def main():
    with open('result.csv', 'w') as f:
        statwriter = csv.writer(f)
        tests = []
        for i in range(TESTS_COUNT):
            tests.append(Test(f'tests/test_random{i}'))
        warmup(tests[0])
        c = 0
        for test in tests:
            c += 1
            print(c)
            size = len(test.graph.adj_list)
            row = [size]
            mean_times = []
            deltas = []
            for algo in ALGOS:
                delta, mean_time = make_measurement_stat(algo, test)
                deltas.append(delta)
                mean_times.append(mean_time)
            row += mean_times + deltas
            statwriter.writerow(row)


if __name__ == '__main__':
    main()
