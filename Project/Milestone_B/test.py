import numpy as np
from problemFormulation import Environment

if __name__ == "__main__":
    # Set a random seed
    np.random.seed(8)

    # Create a 3x3x3 cube
    env = Environment(3)

    # Reward of a saved cube
    print(env.reward())

    # Shuffle the cube
    env.shuffle(rand_nb=10)

    # Reward of a random cube
    print(env.reward())

    # Make a specific move
    env.perform_action((1, 0, 1))

    # Make another move
    env.perform_action((1, 0, -1))

    print("Test has passed.")
