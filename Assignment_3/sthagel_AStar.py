""" sthagel_AStar.py
 A* Search of a problem space.
 Version 0.1, January 23, 2019.
 Stephan Hagel

 Usage:
 python3 sthagel_AStar.py FranceWithDXHeuristics
"""

import sys

VERBOSE = False  # Set to True to see progress; but it slows the search.

if sys.argv == [''] or len(sys.argv) < 2:
    import EightPuzzle as Problem
else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to UCS")

COUNT = None  # Number of nodes expanded.
MAX_open__LENGTH = None  # How long open_ ever gets.
SOLUTION_PATH = None  # List of states from initial to goal, along lowest-cost path.
TOTAL_COST = None  # Sum of edge costs along the lowest-cost path.
BACKLINKS = {}  # Predecessor links, used to recover the path.

# The value g(s) represents the cost along the best path found so far
# from the initial state to state s.
g = {}  # We will use a global hash table to associate g values with states.
h = Problem.h  # This will make life a whole lot easier.


class MyPriorityQueue:
    def __init__(self):
        self.q = []  # Actual data goes in a list.

    def __contains__(self, elt):
        """If there is a (state, priority) pair on the list
        where state==elt, then return True."""
        # print("In MyPriorityQueue.__contains__: elt= ", str(elt))
        for pair in self.q:
            if pair[0] == elt:
                return True
        return False

    def delete_min(self):
        """ Standard priority-queue dequeuing method."""
        if not self.q:
            return []  # Simpler than raising an exception.
        temp_min_pair = self.q[0]
        temp_min_value = temp_min_pair[1]
        temp_min_position = 0
        for j in range(1, len(self.q)):
            if self.q[j][1] < temp_min_value:
                temp_min_pair = self.q[j]
                temp_min_value = temp_min_pair[1]
                temp_min_position = j
        del self.q[temp_min_position]
        return temp_min_pair

    def insert(self, state, priority):
        """We do not keep the list sorted, in this implementation."""
        # print("calling insert with state, priority: ", state, priority)

        if self[state] != -1:
            print("Error: You're trying to insert an element into a MyPriorityQueue instance,")
            print(" but there is already such an element in the queue.")
            return
        self.q.append((state, priority))

    def __len__(self):
        """We define length of the priority queue to be the
        length of its list."""
        return len(self.q)

    def __getitem__(self, state):
        """This method enables Pythons right-bracket syntax.
        Here, something like  priority_val = my_queue[state]
        becomes possible. Note that the syntax is actually used
        in the insert method above:  self[state] != -1  """
        for (S, P) in self.q:
            if S == state:
                return P
        return -1  # This value means not found.

    def __delitem__(self, state):
        """This method enables Python's del operator to delete
        items from the queue."""
        # print("In MyPriorityQueue.__delitem__: state is: ", str(state))
        for count, (S, P) in enumerate(self.q):
            if S == state:
                del self.q[count]
                return

    def __str__(self):
        txt = "MyPriorityQueue: ["
        for (s, p) in self.q:
            txt += '(' + str(s) + ',' + str(p) + ') '
        txt += ']'
        return txt


def runUCS():
    """This is an encapsulation of some setup before running
    UCS, plus running it and then printing some stats."""
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS, MAX_open__LENGTH, SOLUTION_PATH
    COUNT = 0
    BACKLINKS = {}
    MAX_open__LENGTH = 0
    SOLUTION_PATH = UCS(initial_state)
    print(str(COUNT) + " states expanded.")
    print('MAX_open__LENGTH = ' + str(MAX_open__LENGTH))
    # print("The CLOSED list is: ", ''.join([str(s)+' ' for s in CLOSED]))


def UCS(initial_state):
    """Uniform Cost Search. This is the actual algorithm."""
    global g, COUNT, BACKLINKS, MAX_open__LENGTH, CLOSED, TOTAL_COST
    CLOSED = []
    BACKLINKS[initial_state] = None
    # The "Step" comments below help relate UCS's implementation to
    # those of Depth-First Search and Breadth-First Search.

    # STEP 1a. Put the start state on a priority queue called open_
    open_ = MyPriorityQueue()
    open_.insert(initial_state, 0)
    # STEP 1b. Assign g=0 to the start state.
    g[initial_state] = 0.0

    # STEP 2. If open_ is empty, output “DONE” and stop.
    while len(open_) > 0:
        if VERBOSE:
            report(open_, CLOSED, COUNT)
        if len(open_) > MAX_open__LENGTH:
            MAX_open__LENGTH = len(open_)

        # STEP 3. Select the state on open_ having lowest priority value and call it S.
        #         Delete S from open_.
        #         Put S on CLOSED.
        #         If S is a goal state, output its description
        (S, P) = open_.delete_min()
        # print("In Step 3, returned from open_.delete_min with results (S,P)= ", (str(S), P))
        CLOSED.append(S)

        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            print('Length of solution path found: ' + str(len(path) - 1) + ' edges')
            TOTAL_COST = g[S]
            print('Total cost of solution path found: ' + str(TOTAL_COST))
            return path
        COUNT += 1

        # STEP 4. Generate each successors of S and delete
        #         and if it is already on CLOSED, delete the new instance.
        gs = g[S]  # Save the cost of getting to S in a variable.
        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                if new_state in CLOSED:
                    # print("Already have this state, in CLOSED. del ...")
                    del new_state
                    continue
                edge_cost = S.edge_distance(new_state)
                new_g = gs + edge_cost

                # If new_state already exists on open_:
                #   If its new priority is less than its old priority,
                #     update its priority on open_, and set its BACKLINK to S.
                #   Else: forget out this new state object... delete it.

                if new_state in open_:
                    # print("new_state is in open_ already, so...")
                    p2 = open_[new_state]
                    if new_g < p2:
                        # print("New priority value is lower, so del older one")
                        del open_[new_state]
                        open_.insert(new_state, new_g)
                    else:
                        # print("Older one is better, so del new_state")
                        del new_state
                        continue
                else:
                    # print("new_state was not on open_ at all, so just put it on.")
                    open_.insert(new_state, new_g)
                BACKLINKS[new_state] = S
                g[new_state] = new_g

        # print_state_queue("open_", open_)
    # STEP 6. Go to Step 2.
    return None  # No more states on open_, and no goal reached.


def print_state_queue(name, q):
    print(name + " is now: ", end='')
    print(str(q))


def backtrace(s):
    global BACKLINKS
    path = []
    while s:
        path.append(s)
        s = BACKLINKS[s]
    path.reverse()
    print("Solution path: ")
    for s2 in path:
        print(s2)
    return path


def report(open_, closed, count):
    print("len(open_)=" + str(len(open_)), end='; ')
    print("len(CLOSED)=" + str(len(closed)), end='; ')
    print("COUNT = " + str(count))


if __name__ == '__main__':
    runUCS()
