import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from graphlib import pathfinder


ALGOS = [
    pathfinder.DijkstraPathFinder,
    pathfinder.SPFAPathFinder,
    pathfinder.LevitPathFinder,
]


class TestCase:
    @staticmethod
    def from_file(filename):
        testcase = TestCase()
        testcase.graph = pathfinder.Graph.from_file(f'{filename}_graph')
        with open(filename) as f:
            testcase.query = f.readline().split()
            strpath = f.readline()
            if strpath == 'None':
                testcase.path = None
            else:
                testcase.path = list(strpath[:-1].strip('[]').split(', '))
            strcost = f.readline()
            if strcost == 'None':
                testcase.cost = None
            else:
                testcase.cost = int(strcost)
        return testcase


class CommonTests():
    ALGO = None
    STESTFILENAME = 'testdata/common_test'

    def test(self):
        testcase = TestCase.from_file(self.STESTFILENAME)
        finder = self.ALGO(testcase.graph)
        path, cost = finder.get_path(*testcase.query)
        self.assertEqual(path, testcase.path)
        self.assertEqual(cost, testcase.cost)


class ValidnessTests():
    VTESTFILENAME = 'testdata/nonnegative_validation'

    def test_validation(self):
        expect_raise = [True, False, False]
        for i in range(len(expect_raise)):
            graph = pathfinder.Graph.from_file(f'{self.VTESTFILENAME}{i}')
            if expect_raise[i]:
                with self.assertRaises(AssertionError):
                    self.ALGO(graph)
            else:
                self.ALGO(graph)


class TestDijkstra(ValidnessTests, CommonTests, unittest.TestCase):
    ALGO = pathfinder.DijkstraPathFinder
    VTESTFILENAME = 'testdata/dijkstra_validation'


class TestSPFA(ValidnessTests, CommonTests, unittest.TestCase):
    ALGO = pathfinder.SPFAPathFinder


class TestLevit(ValidnessTests, CommonTests, unittest.TestCase):
    ALGO = pathfinder.LevitPathFinder


class TestMultiPathFinder(CommonTests, unittest.TestCase):
    ALGO = pathfinder.MultiPathFinder
    STESTFILENAME = 'testdata/multitest'


if __name__ == '__main__':
    unittest.main()
