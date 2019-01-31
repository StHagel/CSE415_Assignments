''' sthagel_EightPuzzleWithManhattan.py
This file augments EightPuzzle.py with heuristic information,
so that it can be used by the A* implementation given in sthagel_AStar.py.
The particular heuristic is the Manhatten distance of all 8 tiles.
'''

from EightPuzzle import *

# This dictionary stores, what coordinates each tiles belongs to. This can also be generated during runtime via

# for i in range(3):
#     for j in range(3):
#         dict_[j + 3 * i] = (i,j)

# but this would take some extra time, so I decided to hard-code it, even though it makes it a bit more tedious to
# port this implementation to a general n-puzzle.

dict_ = {
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (1, 0),
    4: (1, 1),
    5: (1, 2),
    6: (2, 0),
    7: (2, 1),
    8: (2, 2)
}


def h(s):
    distance = 0

    for i in range(3):
        for j in range(3):
            # We loop through the board...
            for l in range(1, 9):
                # ...check every single tile...
                if s.b[i][j] == l:
                    # ...find it on the board...
                    distance += abs(i - dict_[l][0]) + abs(j - dict_[l][1])
                    # ...calculate its distance and add it to the total.

    return distance
