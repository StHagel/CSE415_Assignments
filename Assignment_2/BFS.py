'''BFS.py
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

print("\nWelcome to BFS")
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
    iterative_bfs(initial_state)
    print(str(COUNT)+" states expanded.")
    print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))


def iterative_bfs(initial_state):
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH

    open_ = [initial_state]
    closed_ = []
    BACKLINKS[initial_state] = None
    visited = {}
    visited[initial_state.__hash__()] = 0
    # This implementation differs from the example implementation for the DFS in some points. The changes I made are
    # explained in more detail in the comments in the IDDFS.py file.

    while open_:
        report(open_, closed_, COUNT)
        if len(open_) > MAX_OPEN_LENGTH:
            MAX_OPEN_LENGTH = len(open_)

        s = open_.pop(0)
        # In contrast to the IDDFS we pop elements at the different end of open_ then where we append them. This lets
        # us use open_ as a queue instead of a stack.

        current_depth = visited[s.__hash__()]
        closed_.append(s)

        if Problem.GOAL_TEST(s):
            print(Problem.GOAL_MESSAGE_FUNCTION(s))
            path = backtrace(s)
            print('Length of solution path found: '+str(len(path)-1)+' edges')
            return
        COUNT += 1

        for op in Problem.OPERATORS:
            if op.precond(s):
                new_state = op.state_transf(s)
                if new_state.__hash__() not in visited or visited[new_state.__hash__()] > current_depth:
                    open_.append(new_state)
                    visited[new_state.__hash__()] = current_depth
                    BACKLINKS[new_state] = s

        print_statel_ist("OPEN", open_)


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
