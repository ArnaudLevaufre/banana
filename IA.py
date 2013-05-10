import heapq
from collections import defaultdict
from math import sqrt


class IA(object):
    def __init__(self, x, y, gameMap):

        self.gridMap = GridMap(gameMap.sizeX+1, gameMap.sizeY+1)

        for b in gameMap.collidable:
            self.gridMap.set_blocked(b)

        self.pf = PathFinder(self.gridMap.successors, self.gridMap.move_cost,
                             self.gridMap.move_cost)

    def _recompute_path(self, xPlayer, yPlayer, xEnt, yEnt):
        self.goal_pos = xPlayer / 64, yPlayer / 64
        self.start_pos = xEnt, yEnt

        self.path = list(self.pf.compute_path(self.start_pos, self.goal_pos))


class PriorityQueueSet(object):
    """ Combined priority queue and set data structure. Acts like
        a priority queue, except that its items are guaranteed to
        be unique.

        Provides O(1) membership test and O(log N) removal of the
        *smallest* item. Addition is more complex. When the item
        doesn't exist, it's added in O(log N). When it already
        exists, its priority is checked against the new item's
        priority in O(1). If the new item's priority is smaller,
        it is updated in the queue. This takes O(N).

        Important: The items you store in the queue have identity
        (that determines when two items are the same, as far as
        you're concerned) and priority. Therefore, you must
        implement the following operators for them: __hash__,
        __cmp__ and __eq__.

        *   __eq__ will be used for exact comparison of items. It
            must return True if and only if the items are identical
            from your point of view (although their priorities can
            be different)
        *   __cmp__ will be used to compare priorities. Two items
            can be different and have the same priority, and even
            be equal but have different priorities (though they
            can't be in the queue at the same time)
        *   __hash__ will be used to hash the items for
            efficiency. To implement it, you almost always have
            to just call hash() on the attribute you're comparing
            in __eq__

        Note that for native Python objects (strings, tuples,
        etc.) these operators are already defined as needed.
    """
    def __init__(self):
        """ Create a new PriorityQueueSet
        """
        self.set = {}
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def has_item(self, item):
        """ Check if *item* exists in the queue
        """
        return item in self.set

    def pop_smallest(self):
        """ Remove and return the smallest item from the queue.
            IndexError will be thrown if the queue is empty.
        """
        smallest = heapq.heappop(self.heap)
        del self.set[smallest]
        return smallest

    def add(self, item):
        """ Add *item* to the queue.

            If such an item already exists, its priority will be
            checked versus *item*. If *item*'s priority is better
            (i.e. lower), the priority of the existing item in the
            queue will be updated.

            Returns True if the item was added or updated.
        """
        if not item in self.set:
            self.set[item] = item
            heapq.heappush(self.heap, item)
            return True
        elif item < self.set[item]:
            # No choice but to search linearly in the heap
            #
            for idx, old_item in enumerate(self.heap):
                if old_item == item:
                    del self.heap[idx]
                    self.heap.append(item)
                    heapq.heapify(self.heap)
                    self.set[item] = item
                    return True
        return False


class PathFinder(object):
    """ Computes a path in a graph using the A* algorithm.

        Initialize the object and then repeatedly compute_path to
        get the path between a start point and an end point.

        The points on a graph are required to be hashable and
        comparable with __eq__. Other than that, they may be
        represented as you wish, as long as the functions
        supplied to the constructor know how to handle them.
    """
    def __init__(self, successors, move_cost, heuristic_to_goal):
        """ Create a new PathFinder. Provided with several
            functions that represent your graph and the costs of
            moving through it.

            successors:
                A function that receives a point as a single
                argument and returns a list of "successor" points,
                the points on the graph that can be reached from
                the given point.

            move_cost:
                A function that receives two points as arguments
                and returns the numeric cost of moving from the
                first to the second.

            heuristic_to_goal:
                A function that receives a point and a goal point,
                and returns the numeric heuristic estimation of
                the cost of reaching the goal from the point.
        """
        self.successors = successors
        self.move_cost = move_cost
        self.heuristic_to_goal = heuristic_to_goal

    def compute_path(self, start, goal):
        """ Compute the path between the 'start' point and the
            'goal' point.

            The path is returned as an iterator to the points,
            including the start and goal points themselves.

            If no path was found, an empty list is returned.
        """
        #
        # Implementation of the A* algorithm.
        #
        closed_set = {}

        start_node = self._Node(start)
        start_node.g_cost = 0
        start_node.f_cost = self._compute_f_cost(start_node, goal)

        open_set = PriorityQueueSet()
        open_set.add(start_node)

        while len(open_set) > 0:
            # Remove and get the node with the lowest f_score from
            # the open set
            #
            curr_node = open_set.pop_smallest()

            if curr_node.coord == goal:
                return self._reconstruct_path(curr_node)

            closed_set[curr_node] = curr_node

            for succ_coord in self.successors(curr_node.coord):
                succ_node = self._Node(succ_coord)
                succ_node.g_cost = self._compute_g_cost(curr_node, succ_node)
                succ_node.f_cost = self._compute_f_cost(succ_node, goal)

                if succ_node in closed_set:
                    continue

                if open_set.add(succ_node):
                    succ_node.pred = curr_node

        return []

    ########################## PRIVATE ##########################

    def _compute_g_cost(self, from_node, to_node):
        return (from_node.g_cost +
                self.move_cost(from_node.coord, to_node.coord))

    def _compute_f_cost(self, node, goal):
        return node.g_cost + self._cost_to_goal(node, goal)

    def _cost_to_goal(self, node, goal):
        return self.heuristic_to_goal(node.coord, goal)

    def _reconstruct_path(self, node):
        """ Reconstructs the path to the node from the start node
            (for which .pred is None)
        """
        pth = [node.coord]
        n = node
        while n.pred:
            n = n.pred
            pth.append(n.coord)

        return pth

    class _Node(object):
        """ Used to represent a node on the searched graph during
            the A* search.

            Each Node has its coordinate (the point it represents),
            a g_cost (the cumulative cost of reaching the point
            from the start point), a f_cost (the estimated cost
            from the start to the goal through this point) and
            a predecessor Node (for path construction).

            The Node is meant to be used inside PriorityQueueSet,
            so it implements equality and hashinig (based on the
            coordinate, which is assumed to be unique) and
            comparison (based on f_cost) for sorting by cost.
        """
        def __init__(self, coord, g_cost=None, f_cost=None, pred=None):
            self.coord = coord
            self.g_cost = g_cost
            self.f_cost = f_cost
            self.pred = pred

        def __eq__(self, other):
            return self.coord == other.coord

        def __cmp__(self, other):
            return cmp(self.f_cost, other.f_cost)

        def __hash__(self):
            return hash(self.coord)

        def __str__(self):
            return 'N(%s) -> g: %s, f: %s' % (self.coord, self.g_cost, self.f_cost)

        def __repr__(self):
            return self.__str__()

class GridMap(object):
    """ Represents a rectangular grid map. The map consists of
        nrows X ncols coordinates (squares). Some of the squares
        can be blocked (by obstacles).
    """
    def __init__(self, nrows, ncols):
        """ Create a new GridMap with the given amount of rows
            and columns.
        """
        self.nrows = nrows
        self.ncols = ncols
        self.map = [[0] * self.ncols for i in xrange(self.nrows)]
        self.blocked = defaultdict(lambda: False)

    def set_blocked(self, coord, blocked=True):
        """ Set the blocked state of a coordinate. True for
            blocked, False for unblocked.
        """
        self.map[coord[0]][coord[1]] = blocked
        if blocked:
            self.blocked[coord] = True
        else:
            if coord in self.blocked:
                del self.blocked[coord]

    def move_cost(self, c1, c2):
        """ Compute the cost of movement from one coordinate to
            another.
        """
        return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)

    def successors(self, c):
        """ Compute the successors of coordinate 'c': all the
            coordinates that can be reached by one step from 'c'.
        """
        slist = []
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                if drow == 0 and dcol == 0:
                    continue
                elif (drow**2 + dcol**2) == 2:
                    continue

                newrow = c[0] + drow
                newcol = c[1] + dcol
                if (0 <= newrow <= self.nrows - 1 and
                        0 <= newcol <= self.ncols - 1 and
                        self.map[newrow][newcol] == 0 and
                        self.blocked[(newrow, newcol)] is False):
                    slist.append((newrow, newcol))

        return slist
