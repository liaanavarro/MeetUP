import utils
from model import (
    Problem, GraphProblem, InstrumentedProblem,
    Node, Graph, UndirectedGraph)
from functools32 import lru_cache

import os, sys
import os.path

def best_first_graph_search(problem, f=lambda node: node.depth):
    frontier = utils.PriorityQueue(min, f)

    explored = utils.PriorityQueue(min, f)
    frontier.append(Node(problem.initial))

    while frontier:
        children = utils.PriorityQueue(min, f)
        node = frontier.pop()
        if problem.goal_test(node[0].state):
            return node[0]
        explored.append(node[0])
        children.extend(node[0].expand(problem))

        for x in children.A:
            existing = 0
            for y in explored.A:
                if x[1] == y[1]:
                    existing = 1
                    break

            if existing == 0:
                for z in frontier.A:
                    if x[1] == z[1]:
                        existing = 1
                        if x[0] < z[0]:
                            frontier.A.__delitem__(frontier.A.index(z))
                            frontier.append(x[1])
                        break

                if existing == 0:
                    frontier.append(x[1])

    return Node('fail')

def astar_search(problem, h=None):
    h = lru_cache()(h or problem.h_sld, 'h')
    return best_first_graph_search(problem, lambda node: h(node) + node.path_cost)
