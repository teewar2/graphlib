import argparse
import random

MAX_WEIGHT = 1000000000


def parse_args():
    parser = argparse.ArgumentParser(
        description='generates random graph')
    parser.add_argument(
        'vertices_count', type=int, help='graph vertices count')
    parser.add_argument(
        '-e', '--edges_count', type=int, help='graph edges count')
    parser.add_argument(
        '-s', '--seed', type=int, help='seed for generator')
    parser.add_argument(
        '-d', '--directed', action='store_true', help='directed graph')
    parser.add_argument(
        '-w', '--weight', type=int, help='max edge weight')
    return parser.parse_args()


def main():
    args = parse_args()
    n = args.vertices_count
    m = args.edges_count if args.edges_count else random.randint(0, n * (n - 1) // 2)
    max_weight = args.weight if args.weight else MAX_WEIGHT
    edges = set()
    if args.seed:
        rng = random.Random(args.seed)
    else:
        rng = random.Random()
    if args.directed:
        print('directed')
    else:
        print('undirected')
    print(*range(1, n + 1))
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            w = rng.randint(0, max_weight)
            if args.directed:
                edges.add((v, u, w))
            edges.add((u, v, w))
    while len(edges) > m:
        u, v, w = random.sample(edges, 1)[-1]
        edges.remove((u, v, w))
    for u, v, w in edges:
        print(u, v, w)


if __name__ == '__main__':
    main()
