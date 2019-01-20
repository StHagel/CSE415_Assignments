'''ItrBFS.py
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

print("\nWelcome to ItrBFS")
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
    IterativeDFS(initial_state)
    print(str(COUNT)+" states expanded.")
    print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))


def IterativeDFS(initial_state):
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH

    # STEP 1. Put the start state on a list OPEN
    _open = [initial_state]
    _closed = []
    BACKLINKS[initial_state] = None

    # STEP 2. If OPEN is empty, output “DONE” and stop.
    while _open:
        report(_open, _closed, COUNT)
        if len(_open) > MAX_OPEN_LENGTH:
            MAX_OPEN_LENGTH = len(_open)

        # STEP 3. Select the first state on OPEN and call it S.
        #         Delete S from OPEN.
        #         Put S on CLOSED.
        #         If S is a goal state, output its description
        s = _open.pop(0)
        _closed.append(s)

        if Problem.GOAL_TEST(s):
            print(Problem.GOAL_MESSAGE_FUNCTION(s))
            path = backtrace(s)
            print('Length of solution path found: '+str(len(path)-1)+' edges')
            return
        COUNT += 1

        # STEP 4. Generate the list L of successors of S and delete
        #         from L those states already appearing on CLOSED.
        _l = []
        for op in Problem.OPERATORS:
            if op.precond(s):
                new_state = op.state_transf(s)
                if not (new_state in _closed):
                    _l.append(new_state)
                    BACKLINKS[new_state] = s

        # Delete from L any members of OPEN that occur on L.
        # Insert all members of L at the end of OPEN.
        for s2 in _open:
            for i in range(len(_l)):
                if s2 == _l[i]:
                    del _l[i]
                    break

        _open = _open + _l
        print_state_list("OPEN", _open)
    # STEP 6. Go to Step 2.


def print_state_list(name, lst):
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


def report(_open, closed, count):
    print("len(OPEN)=" + str(len(_open)), end='; ')
    print("len(CLOSED)=" + str(len(closed)), end='; ')
    print("COUNT = " + str(count))


if __name__ == '__main__':
    runDFS()
