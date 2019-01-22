'''IDDFS.py
by Stephan Hagel

Assignment 2, in CSE 415, Winter 2019.

This file contains my implementation of the iterative Breadth-First-Search algorithm.
The code is mainly based on the ItrDFS.py provided by S. Tanimoto and has only been changed to perform the BFS.
'''


import sys

if sys.argv == [''] or len(sys.argv) < 2:
    #  import EightPuzzle as Problem
    import sthagel_Farmer_Fox as Problem
else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to IDDFS")
COUNT = None
BACKLINKS = {}


def runDFS():
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH
    COUNT = 0
    BACKLINKS = {}
    MAX_OPEN_LENGTH = 0
    iterative_deepening_dfs(initial_state)
    print(str(COUNT) + " states expanded.")
    print('MAX_OPEN_LENGTH = ' + str(MAX_OPEN_LENGTH))


def iterative_deepening_dfs(initial_state):
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH
    depthlimit = 0

    while True:
        # To implement the iterative deepening we loop around the DFS until we hit the goal.
        print("\nCurrent depthlimit = " + str(depthlimit) + "\n")
        COUNT = 0
        current_depth = 0
        open_ = [initial_state]
        closed_ = []
        BACKLINKS[initial_state] = None
        visited = {}
        visited[initial_state.__hash__()] = current_depth
        # For this to work we need to track, which states have already been visited. This is realized with a dictionary,
        # which maps the hash of a state to its depth inside the graph.

        while open_:
            report(open_, closed_, COUNT)
            if len(open_) > MAX_OPEN_LENGTH:
                MAX_OPEN_LENGTH = len(open_)

            s = open_.pop()
            # As I was working on this task, it turned out to be inconveniant to stick with the approach used in the
            # example DFS formulation. Therefore I changed a few things from it. For example I pop the state from the
            # other end of open_ and therefore also append the states on the other side.

            current_depth = visited[s.__hash__()]
            # We need the depth of the state we just popped later to get the depth of the states coming after it.

            closed_.append(s)

            if Problem.GOAL_TEST(s):
                print(Problem.GOAL_MESSAGE_FUNCTION(s))
                path = backtrace(s)
                print('Length of solution path found: ' + str(len(path) - 1) + ' edges')
                return
            COUNT += 1

            if current_depth < depthlimit:
                # This if statement is part of the logic that implements the iterative deepening.
                current_depth += 1
                # Now we can safely increase the current_depth, to give the new states the correct depth.
                for op in Problem.OPERATORS:
                    if op.precond(s):
                        new_state = op.state_transf(s)
                        # The list of possible states is generated just as in the example DFS implementation.

                        if new_state.__hash__() not in visited or visited[new_state.__hash__()] > current_depth:
                            # This part is different though. Instead of checking, weather the new state appears in
                            # open_ or closed, we check if the hash of the new state already appears in the visited
                            # dictionary. We also replace the state, if it already appears but it has been reached
                            # via a longer path before.

                            open_.append(new_state)
                            visited[new_state.__hash__()] = current_depth
                            # As stated earlier, popping from the other end of open_ allows us to use the append()
                            # function for new states. We also add the depth of the new state to the dictionary.

                            BACKLINKS[new_state] = s

        depthlimit += 1
        # If the search does not find a path to the goal state, we increase the depthlimit and run it again.


def print_statel_ist(name, lst):
    print(name+" is now: ", end='')
    for s in lst[:-1]:
        print(str(s), end=', ')
    print(str(lst[-1]))


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
    print("len(OPEN)=" + str(len(open_)), end='; ')
    print("len(CLOSED)=" + str(len(closed)), end='; ')
    print("COUNT = " + str(count))


if __name__ == '__main__':
    runDFS()
