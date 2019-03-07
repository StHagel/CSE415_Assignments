"""cube.py
This file contains the problem formulation for a general NxNxN Rubik's cube.

Usage:
-----
- initialize a solved cube with c = Cube(N), where N is the side length.
- randomize a cube with c.randomize(k) where k is the number of random moves to make.
  This will be useful for the curriculum learning.
- make cube moves with c.move() and turn the whole cube with c.turn().

conventions
-----------
- This is a model of where the stickers are, not where the solid cubies are.
- The faces have integers and one-letter names. The one-letter face names are given by the dictionary Cube.facedict.
- The layers of the cube have names that are composed of a face letter and a number,
  with 0 indicating the outermost face.
"""

import numpy as np


class Cube(object):
    """
    Cube
    ----
    Initialize with arguments:
    - N, the side length (the cube is NxNxN)
    - stickers, Initialize a cube with a given set of stickers (optional).
    """

    # This dictionary translates between letter and integer descriptions of the faces.
    facedict = {"U": 0, "D": 1, "F": 2, "B": 3, "R": 4, "L": 5}

    # For convenience we also add an inverse dictionary.
    inv_facedict = {0: "U", 1: "D", 2: "F", 3: "B", 4: "R", 5: "L"}

    def __init__(self, N=None, stickers=None):
        if stickers is None:
            self.N = N
            self.stickers = np.array(
                [np.tile(i, (self.N, self.N)).astype(np.int8) for i in range(6)])
        else:
            self.N = stickers.shape[1]
            self.stickers = stickers

    def move(self, i, l_, d):
        """
        Make a layer move of layer l parallel to face inv_facedict[i] through d 90-degree turns in the
        clockwise direction.  Layer 0 is the face itself, and higher l values are for layers deeper into the cube.
        Use d=3 for counter-clockwise moves, and d=2 for a 180-degree move.
        i is in range(6)
        l is in range(N)
        d is in range(1, 4)
        """
        f = self.inv_facedict[i]
        l2 = self.N - 1 - l_
        assert l_ < self.N
        ds = range((d + 4) % 4)
        if f == "U":
            f2 = "D"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["F"], range(self.N), l2),
                              (self.facedict["R"], range(self.N), l2),
                              (self.facedict["B"], range(self.N), l2),
                              (self.facedict["L"], range(self.N), l2)])
        if f == "D":
            return self.move(self.facedict["U"], l2, -d)
        if f == "F":
            f2 = "B"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["U"], range(self.N), l_),
                              (self.facedict["L"], l2, range(self.N)),
                              (self.facedict["D"], range(self.N)[::-1], l2),
                              (self.facedict["R"], l_, range(self.N)[::-1])])
        if f == "B":
            return self.move(self.facedict["F"], l2, -d)
        if f == "R":
            f2 = "L"
            i2 = self.facedict[f2]
            for d in ds:
                self._rotate([(self.facedict["U"], l2, range(self.N)),
                              (self.facedict["F"], l2, range(self.N)),
                              (self.facedict["D"], l2, range(self.N)),
                              (self.facedict["B"], l_, range(self.N)[::-1])])
        if f == "L":
            return self.move(self.facedict["R"], l2, -d)
        for d in ds:
            if l_ == 0:
                self.stickers[i] = np.rot90(self.stickers[i], 3)
            if l_ == self.N - 1:
                self.stickers[i2] = np.rot90(self.stickers[i2], 1)
        return None

    def _rotate(self, args):
        """
        Internal function for the move() function.
        """
        a0 = args[0]
        sticker_a0 = self.stickers[a0]
        a = a0
        for b in args[1:]:
            self.stickers[a] = self.stickers[b]
            a = b
        self.stickers[a] = sticker_a0
        return None

    def randomize(self, k):
        """
        Make k randomly chosen moves to scramble the cube.
        """
        moves = []
        for _ in range(k):
            f = np.random.randint(6)
            l_ = np.random.randint(self.N)
            d = 1 + np.random.randint(3)
            self.move(f, l_, d)
            moves.append([f, l_, d])
        return moves

    def finish(self,):
        return np.array_equal(self.stickers, np.array([np.tile(i, (self.N, self.N)) for i in range(6)]))


def reverse_action(move):
    [f, l, d] = move
    if d == 0 or d == 4:
        return [f, l, d]
    if d == 1:
        return [f, l, 3]
    if d == 2:
        return [f, l, 2]
    return [f, l, 1]
