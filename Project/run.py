"""run.py

This file executes the actual Q-Learning.
The plan is the following:
i) Initialize a solved cube
ii) Make n moves (starting with n=1)
iii) Train the agent on this configuration for a certain number of episodes with a maximum number of moves
iv) Go back to step i) but make a different move in step ii) until all possibilities (or at least some) have been done
v) increase n by one and go back to i)

"""

import Cubes
import random
import sys
from math import fabs

GOD_NUMBER_TWO = 14  # The maximum number of moves needed to solve a 2x2x2 cube from any given state
GOD_NUMBER_THREE = 26  # The maximum number of moves needed to solve a 3x3x3 cube from any given state
N_EPISODES = 100  # Number of episodes the agent uses on each configuration
MAX_MOVES = 7  # The maximum number of moves we make starting from a solved cube to create a new initial state
MAX_ITER = 2  # The maximum number of wrong moves allowed until the cube is reset.

Q_VALUES = {}
POLICY = {}
KNOWN_STATES = []
ACTIONS = None
EPSILON = 0.3
ALPHA = 0.5
DISCOUNT = 0.9
SIZE = 2
LIVING_COST = 0.0

# TODO: Implement a method to save and load Q-Values and policies.
SAVE_Q_VALS = False
LOAD_Q_VALS = False


def run():
    global ACTIONS, KNOWN_STATES, Q_VALUES, POLICY
    ACTIONS = Cubes.ActionOps

    if LOAD_Q_VALS:
        with open("q_vals.txt", "r") as f:
            print("Reading qvals")
            s = f.read()
            Q_VALUES = eval(s)
        with open("policy.txt", "r") as f:
            print("reading pol")
            s = f.read()
            POLICY = eval(s)

    else:
        # This loop handles the curriculum learning
        for current_max in range(MAX_MOVES):
            print("Shuffling " + str(current_max + 1) + " times.")
            num_steps = 12 * (current_max + 1)

            # At each step in curr. learning we take `num_steps` different starting positions to learn from
            for k in range(num_steps):

                # Initializing a solved cube
                if SIZE == 2:
                    cube = Cubes.State(Cubes.GOAL_STATES_TWO[0])
                else:
                    cube = Cubes.State(Cubes.GOAL_STATE_THREE)

                # Shuffling the cube
                for j in range(current_max + 1):
                    print("Shuffling...")
                    rm = random_move()
                    cube = Cubes.move(cube, rm[0], rm[1])

                # Add the start state to the `KNOWN_STATES` list, if it is not already in there
                if cube not in KNOWN_STATES:
                    KNOWN_STATES.append(cube)

                # The number of episodes we train our agent on depends on the number of moves made to shuffle the cube
                eps = N_EPISODES * (current_max + 1)

                # Do the actual Q-Learning
                qlearn(cube, current_max + 1, DISCOUNT, EPSILON, ALPHA, MAX_ITER + current_max, eps)

        print("Did the training.")

        if SAVE_Q_VALS:
            print("Saving Q-Values and policy")
            with open("q_vals.txt", "w") as f:
                print(Q_VALUES, file=f)

            with open("policy.txt", "w") as f:
                print(POLICY, file=f)

        print("Testing the model")
        if SIZE == 2:
            testcube = Cubes.State(Cubes.GOAL_STATES_TWO[0])

        else:
            testcube = Cubes.State(Cubes.GOAL_STATE_THREE)

        testcube = Cubes.move(testcube, 0, 1)
        testcube = Cubes.move(testcube, 3, -1)
        testcube = Cubes.move(testcube, 2, 1)
        testcube = Cubes.move(testcube, 4, -1)
        testcube = Cubes.move(testcube, 5, 1)

        test_model(testcube, 5)


def random_move():
    """
    :return: tuple `(i, j)`, where `i` is a random face and `j` is a random direction
    """
    i = random.randint(0, 5)
    j = random.choice([1, -1])
    return i, j


def qlearn(start_state, currmax, discount=DISCOUNT, epsilon=EPSILON, alpha=ALPHA, max_moves=MAX_ITER, eps=N_EPISODES,
           testing=False):
    """
    :param start_state: The state we start the Q-Learning from
    :param currmax:  The number of moves done while shuffling the cube
    :param discount: The discount factor (gamma)
    :param epsilon: The probability that a random move is chosen instead of following the policy
    :param alpha: The learning rate
    :param max_moves: The maximum number of moves the agent gets to take before the state is reset to `start_state`
    :param eps: The number of episodes the agent is trained
    :param testing: Enables more detailed output and tests the trained model
    """
    global ACTIONS, Q_VALUES, SIZE, POLICY, KNOWN_STATES
    goal_counter = 0  # Counts how many times we already reached the goal
    episode = 0

    # We need to initialize the Q-Values once
    Q_VALUES = return_Q_values(KNOWN_STATES, ACTIONS)
    POLICY = extract_policy(KNOWN_STATES, ACTIONS)

    # To speed up the process, the agent does not have to do all `eps` episodes, but if it reaches the goal `10*currmax`
    # times, we can go to the next start state.
    while goal_counter < 10 * currmax and episode < eps:
        if testing:
            print("Episode Nr. " + str(episode + 1) + ":")
        print("Episode Nr. " + str(episode + 1) + ":")
        episode += 1

        current_state = start_state
        current_move = 0
        if SIZE == 3:
            gs = Cubes.GOAL_STATES_THREE
        else:
            gs = Cubes.GOAL_STATES_TWO
        while not current_state.d in gs and not current_move == max_moves:
            s = current_state

            # We need to generate a random number to decide, whether we apply our policy or make a random move.
            chance = random.uniform(0.0, 1.0)
            if chance > epsilon:
                # Choose an action according to the policy
                if s in POLICY:
                    act = apply_policy(s)
                else:
                    act, actA = random.choice(list(ACTIONS.items()))
                    del actA
            else:
                act, actA = random.choice(list(ACTIONS.items()))
                del actA

            # Using act on the current state gives the new state
            new_state = ACTIONS[act].apply(s)
            KNOWN_STATES.append(new_state)

            # We might need to initialize the Q value for the current state with the chosen action
            if (s, act) not in Q_VALUES:
                Q_VALUES[(s, act)] = 0.0

            # This finds the maximum, that is needed in the Q value iteration
            maxQ = -1000
            for act2 in ACTIONS:
                if (new_state, act2) not in Q_VALUES:
                    Q_VALUES[(new_state, act2)] = 0.0
                if Q_VALUES[(new_state, act2)] > maxQ:
                    maxQ = Q_VALUES[(new_state, act2)]

            # Calculate the sample for the move we did
            rew = Cubes.reward(new_state, SIZE, LIVING_COST)
            if fabs(rew - 1.0) < 1e-5:
                if testing:
                    print("reached a goal state!")
                print("reached a goal state!")
                goal_counter += 1

            sample = rew + discount * maxQ

            # Update the Q value for the current state
            Q_VALUES[(s, act)] = (1.0 - alpha) * Q_VALUES[(s, act)] + alpha * sample

            if not goal_counter == 0:
                alpha /= goal_counter

            # Instead of updating the policy for all states, we just need to update the one for the current state
            update_policy(s, KNOWN_STATES, ACTIONS)

            # Actually move to the new state and increase the move counter
            current_state = new_state
            current_move += 1
            if testing:
                print(current_state)
                if goal_counter > 0:
                    print("Solved!")
                    return


def apply_policy(s):
    """Return the action that your current best policy implies for state s."""
    global POLICY

    return POLICY[s]


def return_Q_values(S, A):
    """Return the dictionary whose keys are (state, action) tuples,
    and whose values are floats representing the Q values from the
    most recent call to one_step_of_VI. This is the normal case, and
    the values of S and A passed in here can be ignored.
    However, if no such call has been made yet, use S and A to
    create the answer dictionary, and use 0.0 for all the values.
    """
    global Q_VALUES

    if Q_VALUES == {}:
        for state in S:
            for action in A:
                Q_VALUES[(state, action)] = 0.0

    return Q_VALUES


def update_policy(state, S, A):
    """
    Updates the Policy of `state`.
    """

    global POLICY, ACTIONS

    if state in POLICY:
        curr_act = apply_policy(state)
        curr_val = Q_VALUES[(state, curr_act)]
        max_val = curr_val
        max_act = curr_act

        for new_act in ACTIONS:
            new_val = Q_VALUES[(state, new_act)]
            if new_val > max_val:
                max_val = new_val
                max_act = new_act

        POLICY[state] = max_act
    else:
        POLICY = extract_policy(S, A)


def extract_policy(S, A):
    """Return a dictionary mapping states to actions. Obtain the policy
    using the q-values most recently computed.  If none have yet been
    computed, call return_Q_values to initialize q-values, and then
    extract a policy.  Ties between actions having the same (s, a) value
    can be broken arbitrarily.
    """
    global POLICY
    POLICY = {}

    qvals = return_Q_values(S, A)
    # A local copy of the q values, that also initializes them, if needed.

    for state in S:
        best_action = None
        best_value = None
        # We use the same method for finding the maximum as before, but this time we need to track the action as well.
        for action in A:
            if (state, action) in qvals:
                new_value = qvals[(state, action)]
            else:
                qvals[(state, action)] = 0.0
                new_value = qvals[(state, action)]
            if not best_value:
                best_value = new_value
                best_action = action

            if new_value > best_value:
                best_action = action
                best_value = new_value

        if best_action:
            POLICY[state] = best_action
        # write the best action into the Policy dictionary

    return POLICY


def test_model(cube, currmax):
    print(cube)
    a = "continue"
    while not a == "stop":
        qlearn(cube, currmax, max_moves=(MAX_ITER + currmax), testing=True)
        a = input()


use_default = input("Use default values? (Y/n)")
if not use_default.lower() == "n":
    run()
else:
    SIZE = int(input("Please input Cube size. (Only 3 working right now): "))
    DISCOUNT = float(input("Please input discount. (Default = 0.9): "))
    ALPHA = float(input("Please input learning rate. (Default = 0.5): "))
    EPSILON = float(input("Please input epsilon. (Default = 0.3): "))
    LIVING_COST = float(input("Please input living cost. (Negative number, default = 0): "))
    N_EPISODES = int(input("Please input number of episodes. (Default = 100): "))
    MAX_MOVES = int(input("Please input maximum number of scrambles. (Default = 3): "))
    MAX_ITER = int(input("Please input maximum number of moves allowed. (Default = 2): "))
    run()
