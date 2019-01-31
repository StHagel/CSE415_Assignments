''' sthagel_EightPuzzleWithHamming.py
This file augments EightPuzzle.py with heuristic information,
so that it can be used by the A* implementation given in sthagel_AStar.py.
The particular heuristic is the Hamming distance, i.e. the number of tiles, that are out of place.

The implementation is really simple: We just need to loop through the board of a given state and
increase a counter variable by one each time, a tile is out of place.
'''

from EightPuzzle import *


def h(s):
    counter = 0
    for i in range(3):
        for j in range(3):
            k = 3 * i + j
            if s.b[i][j] != k:
                counter += 1

    return counter
