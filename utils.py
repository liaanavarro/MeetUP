""" Provides some utilities widely used by other modules.

You don't have to add/change anything in this code. If you think there are 
errors in the code, please send me a message at sirprrr@gmail.com.

You will NOT submit this file.
Ref: github.com/aimacode/aima-python """

from collections import deque
import bisect
import math

# ______________________________________________________________________________
# Queues: LIFOQueue (Stack), FIFOQueue, PriorityQueue

# TODO: Possibly use queue.Queue, queue.PriorityQueue

class LIFOQueue(deque):
    """ A Last-In-First-Out Queue (Stack). 
    This is the same as how a list works """

    def __repr__(self):
        return ", ".join("%s" % val for val in self)

    def extend(self, items):
        # Add items in reverse so that the first
        # in the sorted list will be the first to
        # be popped
        for item in sorted(items, reverse=True):
            self.append(item)
    

class FIFOQueue(deque):
    """A First-In-First-Out Queue."""

    def __repr__(self):
        return ", ".join("%s" % val for val in self)

    def pop(self):
        return self.popleft()



class PriorityQueue():
    """A queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first. If order is min, the item with minimum f(x) is
    returned first; if order is max, then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order=min, f=lambda x: x):
        self.A = []
        self.order = order
        self.f = f

    def __repr__(self):
    #     print [val for val in self.A]
        return ", ".join("(%s, %s)" % (val[0], val[1]) for val in self.A)

    def append(self, item):
        bisect.insort(self.A, (self.f(item), item))

    def extend(self, items):
        for item in sorted(items, reverse=True):
            self.append(item)

    def __len__(self):
        return len(self.A)

    def pop(self):
        if self.order == min:
            p = self.A.pop(0)
            return p[1], p[0]
        else:
            p = self.A.pop()
            return p[1], p[0]

    def __contains__(self, item):
        return any(item == pair[1] for pair in self.A)

    def __getitem__(self, key):
        for _, item in self.A:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.A):
            if item == key:
                self.A.pop(i)


# ______________________________________________________________________________
# Heuristic Functions
# distance (straight line/euclidean distance)

def distance(a, b):
    """ The distance between two (x, y) points. """
    return math.hypot((a[0] - b[0]), (a[1] - b[1]))


# ______________________________________________________________________________
# Misc Functions

def name(obj):
    """ Try to find some reasonable name for the object. """
    return (getattr(obj, 'name', 0) or getattr(obj, '__name__', 0) or
            getattr(getattr(obj, '__class__', 0), '__name__', 0) or
            str(obj))


def print_table(table, header=None, sep='   ', numfmt='%g'):
    """ Print a list of lists as a table, so that columns line up nicely.
    header, if specified, will be printed as the first row.
    numfmt is the format for all numbers; you might want e.g. '%6.2f'.
    (If you want different formats in different columns,
    don't use print_table.) sep is the separator between columns. """
    
    if header:
        table.insert(0, header)

    for row in table:
        for sublist in row[1:]:
            if isinstance(sublist, (list, tuple)):
                del row[1:]
                row.extend(sublist)

    justs = ['rjust' if isnumber(x) else 'ljust' for x in table[1]]

    table = [[numfmt%(x) if isnumber(x) else x for x in row]
             for row in table]

    sizes = list(
            map(lambda seq: max(map(len, seq)),
                list(zip(*[map(str, row) for row in table]))))
    
    for row in table:
        print(sep.join(getattr(
            str(x), j)(size) for (j, size, x) in zip(justs, sizes, row)))


def isnumber(x):
    """ Is x a number? """
    # return hasattr(x, ('__int__'))
    return isinstance(x, (int, float, long))
