""" Search problem model module.
This also includes node and graph models.

You don't have to add/change anything in this code. If you think there are 
errors in the code, please send me a message at sirprrr@gmail.com.

You will NOT submit this file.
Ref: github.com/aimacode/aima-python """

import utils
 
# ______________________________________________________________________________
# Graph models

class Graph:
    """ The base class for a graph. 

    A graph connects nodes (vertices) by edges (links).  Each edge can also
    have a length associated with it.  The constructor call is something like:
        g = Graph({'A': {'B': 1, 'C': 2})
    this makes a graph with 3 nodes, A, B, and C, with an edge of length 1 from
    A to B,  and an edge of length 2 from A to C.  You can also do:
        g = Graph({'A': {'B': 1, 'C': 2}, directed=False)
    This makes an undirected graph, so inverse links are also added.

    Adding nodes and edges to an undirected graph may not work properly yet. """

    def __init__(self, dict={}, directed=False):
        self.dict = dict
        self.directed = directed
        if not directed:
            self.dict = self.make_undirected(dict)

    def make_undirected(self, dict):
        """ Make a digraph into an undirected graph by adding symmetric edges. """
        for a in list(dict.keys()):    # Nodes with outgoing edges
            for (b, distance) in dict[a].items():  # Nodes with incoming edges
                dict.setdefault(b, {})[a] = distance # Make symmetric connection
        return dict
            
    def get(self, a, b=None):
        """ Return a link distance or a dict of {node: distance} entries.
        .get(a,b) returns the distance or None;
        .get(a) returns a dict of {node: distance} entries, possibly {}. """
        links = self.dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        """ Return a sorted list of nodes in the graph. """
        return sorted(self.dict.keys())


def UndirectedGraph(dict=None):
    """ Build Graph from dictionary where every edge goes both ways. """
    g = Graph(dict=dict, directed=False)
    return g

# ______________________________________________________________________________
# Problem models

class Problem(object):
    """The abstract class for a formal problem.  

    You should subclass this and implement the methods actions and result, 
    and possibly __init__, goal_test, and path_cost. Then you will create 
    instances of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal


class GraphProblem(Problem):
    """ The problem of searching a graph from one node to another. """

    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph

    def actions(self, A):
        """ The (sorted) actions at a graph node are just its neighbors. """
        return sorted(self.graph.get(A).keys())#, reverse=True) # return

    def result(self, state, action):
        """ The result of going to a neighbor is just that neighbor. """
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or float('inf'))

    def h_sld(self, node):
        """ h function is straight-line distance from a node's state to goal. """
        locs = getattr(self.graph, 'locations', None)
        try:
            return int(utils.distance(locs[node.state], locs[self.goal]))
        except:
            return float('inf')


class InstrumentedProblem(Problem):
    """ Delegates to a problem, and keeps statistics. """

    def __init__(self, problem):
        self.problem = problem
        self.succs = self.goal_tests = self.expansions = 0
        self.found = None

    def actions(self, state):
        self.succs += 1
        return self.problem.actions(state)

    def result(self, state, action):
        self.expansions += 1
        # print "< expand", state, "-", action, ">", self.expansions # show nodes expanded
        return self.problem.result(state, action)

    def goal_test(self, state):
        self.goal_tests += 1
        result = self.problem.goal_test(state)
        if result:
            self.found = state
        return result

    def path_cost(self, c, state1, action, state2):
        return self.problem.path_cost(c, state1, action, state2)

    def value(self, state):
        return self.problem.value(state)

    def __getattr__(self, attr):
        return getattr(self.problem, attr)

    def __repr__(self):
        # return '<%4d/%4d/%4d/%s>' % (self.succs, self.goal_tests,
        #                              self.expansions, str(self.found)[:4])
        return "\
        Nodes expanded:\t%4d \n\
        Nodes explored:\t%4d \n\
        Goal tests:\t%4d" % (self.expansions, self.succs, self.goal_tests)

# ______________________________________________________________________________
# Node model

class Node:
    """ A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class. """

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """ Create a search tree Node, derived from a parent by an action. """
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        try:
            if 'fail' in state.lower():
                self.action = 'FAIL'
                self.parent = Node('')

            if parent:
                self.depth = parent.depth + 1
        except Exception, e:
            pass

    def __repr__(self):
        return "<Node %s, %s>" % (self.state, self.path_cost)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem, reverse=False):
        """ List the nodes reachable in one step from this node. """
        return sorted([self.child_node(problem, action)
                for action in problem.actions(self.state)], reverse=reverse)

    def child_node(self, problem, action):
        """ Return all possible child nodes from current node. """
        next = problem.result(self.state, action)
        return Node(next, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next))

    def solution(self):
        """ Return the sequence of actions to go from the root to this node. """
        return [node.action for node in self.path()[1:]]

    def path(self):
        """ Return a list of nodes forming the path from the root to this node. """
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # if isinstance(self.state, list):
        #     return hash(tuple(self.state))
        # else:
        #     return hash(self.state)
        return hash(self.state)



# ______________________________________________________________________________
# Tutorial

if __name__ == '__main__':
    """ Some sample codes to better understand how the Graph, Problem and Node classes work. """

    """ Graph model """
    # " UndirectedGraph(d) creates undirected graph from dict d. "
    # graph = UndirectedGraph(dict(
    #     Arad=dict(Sibiu=140, Timisoara=118, Zerind=75),
    #     Lugoj=dict(Mehadia=70, Timisoara=111),
    #     Manila=dict()))

    # " nodes() finds all nodes in graph. "
    # print 'Nodes in graph: '
    # print '   ', ', '.join(graph.nodes())

    # " get(a) finds all nodes connected to node a. "
    # print 'Arad is connected to:'
    # print '\n'.join('   {}: {}'.format(n,d) for n,d in graph.get('Arad').iteritems())
    # print 'Manila is connected to:'
    # print '\n'.join('   {}: {}'.format(n,d) for n,d in graph.get('Manila').iteritems())

    # " get(a,b) finds distance between a and b. "
    # print 'Direct distance from Arad to Sibiu is:', graph.get('Arad', 'Sibiu')
    # print 'Direct distance from Arad to Manila is:', graph.get('Arad', 'Manila')


    # """ Problem model """
    # " GraphProblem(a, b, g) creates a problem with initial state a, goal b and graph g. "
    # problem = GraphProblem('Arad', 'Sibiu', graph)

    # " actions(s) finds all possible actions to do with / nodes to visit next from s. "
    # print 'Possible actions from Arad: '
    # print '   Go to', ', '.join(problem.actions('Arad'))

    # " result(s, x) simply returns the next state after doing action x. "
    # action = problem.actions('Arad')[0]
    # print 'The result of going from Arad to %s:' % action
    # print '     You are now at', problem.result('Arad', action)     
    
    # " path_cost(c, a, x, b) adds to current cost c the cost of going from a to b. "
    # " Note that for GraphProblem, action is not utilized here. "
    # print 'The path cost from from Arad to Sibiu is:',
    # print problem.path_cost(0, "Arad", action, 'Sibiu')

    # " goal_test(s) checks whether the current state s is the goal state. "
    # print 'The goal state is:', problem.goal
    # print "Is Manila the goal:", problem.goal_test('Manila')


    # """ Node model """
    # " Node(s) creates a node with state s. "
    # problem = GraphProblem('Arad', 'Sibiu', graph)
    # node = Node('Arad')
    # print node

    # " expand(p) returns the directly connected nodes / states to node. "
    # print 'From', node.state, 'we can go to:'
    # print '   ', ', '.join(m.state for m in node.expand(problem))

    # " child_node(p, x) returns the next node upon performing action x on node. "
    # action = 'Timisoara'
    # child = node.child_node(problem, action)
    # print 'Going from %s to %s results to:' % (node, action)
    # print '     Child with state %s, parent %s, path cost %.0f, and depth %d' %\
    #             (child.state, child.parent, child.path_cost, child.depth)

    # action = 'Lugoj'
    # child_2 = child.child_node(problem, action)
    # print 'Going from %s to %s results to:' % (child, action)
    # print '     Child with state %s, parent %s, path cost %.0f, and depth %d' %\
    #             (child_2.state, child_2.parent, child_2.path_cost, child_2.depth)

    # " Note that trying to go to a non-directly connected node gives inf path cost. "
    # " This should be filtered by the searching algorithm. "
    # action = 'Manila'
    # child_3 = child_2.child_node(problem, action)
    # print 'Going from %s to %s results to:' % (child_2, action)
    # print '     Child with state %s, parent %s, path cost %.0f, and depth %d' %\
    #             (child_3.state, child_3.parent, child_3.path_cost, child_3.depth)

    # " path() returns the constructed path while doing the search. "
    # " solution() simply calls path() to construct the solution path (excluding start) "
    # print 'Path for root state:', ' > '.join(m.state for m in node.path())
    # print 'Path for first child state:', ' > '.join(m.state for m in child.path())
    # print 'Path for second child state:', ' > '.join(m.state for m in child_2.path())
    # print 'Solution for problem', problem.initial, 'to', problem.goal, 'is:',\
    #         ' > '.join(m for m in child_2.solution())

# ______________________________________________________________________________
