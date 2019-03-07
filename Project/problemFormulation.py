"""problemFormulation.py

This file gives a more elegant way to handle the problem formulation.
It is basically just a wrapper for the Cube class defined in cube.py
"""

import numpy as np
from cube import Cube


class Environment(object):

    # Initialize a finished cube
    def __init__(self, N):
        self.N = N
        self.cube = Cube(N=N)

    # This function shuffles the cube. It also has the option to just make a fixed action, given as an argument.
    def shuffle(self, rand_nb=None, fixed_action=None):
        if rand_nb is not None:
            moves = self.cube.randomize(rand_nb)
            return moves
        self.perform_action(fixed_action)
        return fixed_action

    # This function performs an action on the cube and gets a reward.
    # The reward is 1, if the cube is solved and 0 otherwise.
    def perform_action(self, action):
        (f, l, d) = action
        self.cube.move(f, l, d)
        return self.reward()

    # The reward function might be upgraded later on with some type of heuristics.
    def reward(self):
        return self.cube.finish()

    # Select a random_action
    def random_action(self):
        f = np.random.randint(6)
        l = np.random.randint(self.N)
        d = 1 + np.random.randint(3)
        return [f, l, d]

    def get_state(self):
        return self.cube.stickers
