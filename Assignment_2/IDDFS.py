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
    IterativeDFS(initial_state)
    print(str(COUNT)+" states expanded.")
    print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))


def IterativeDFS(initial_state):
    global COUNT, BACKLINKS, MAX_OPEN_LENGTH
    depth = 0
    flag = False
    impossible = False

    while not flag and not impossible:
        print("\nDepth = " + str(depth) + "\n")
        # STEP 1. Put the start state on a list OPEN
        COUNT = 0
        open_ = [initial_state]
        closed_ = []
        BACKLINKS[initial_state] = None

        # STEP 2. If OPEN is empty, output “DONE” and stop.

        while open_ and COUNT <= depth:
            report(open_, closed_, COUNT)
            if len(open_) > MAX_OPEN_LENGTH:
                MAX_OPEN_LENGTH = len(open_)

            # STEP 3. Select the first state on OPEN and call it S.
            #         Delete S from OPEN.
            #         Put S on CLOSED.
            #         If S is a goal state, output its description
            s = open_.pop(0)
            closed_.append(s)

            if Problem.GOAL_TEST(s):
                print(Problem.GOAL_MESSAGE_FUNCTION(s))
                path = backtrace(s)
                print('Length of solution path found: '+str(len(path)-1)+' edges')
                flag = True
                return
            COUNT += 1

            # STEP 4. Generate the list L of successors of S and delete
            #         from L those states already appearing on CLOSED.
            l_ = []
            for op in Problem.OPERATORS:
                if op.precond(s):
                    new_state = op.state_transf(s)
                    if not (new_state in closed_):
                        l_.append(new_state)
                        BACKLINKS[new_state] = s

            # Delete from L any members of OPEN that occur on L.
            # Insert all members of L at the end of OPEN.
            for s2 in l_:
                for i in range(len(open_)):
                    if s2 == open_[i]:
                        del open_[i]
                        break

            open_ = l_ + open_
            print_statel_ist("OPEN", open_)

            if not open_:
                impossible = True

        depth += 1
        # STEP 6. Go to Step 2.

    if impossible:
        print("No solution could be found!")


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
