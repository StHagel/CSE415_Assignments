"""sthagel_VI.py

Value Iteration for Markov Decision Processes.
"""

from math import fabs


# Edit the returned name to ensure you get credit for the assignment.
def student_name():
    return "Hagel, Stephan"  # For an autograder.


Vkplus1 = {}
Q_Values_Dict = {}
Policy = {}


def one_step_of_VI(S, A, T, R, gamma, Vk):
    """S is list of all the states defined for this MDP.
    A is a list of all the possible actions.
    T is a function representing the MDP's transition model.
    R is a function representing the MDP's reward function.
    gamma is the discount factor.
    The current value of each state s is accessible as Vk[s].


    Your code should fill the dictionaries Vkplus1 and Q_Values_dict
    with a new value for each state, and each q-state, and assign them
    to the state's and q-state's entries in the dictionaries, as in
        Vkplus1[s] = new_value
        Q_Values_Dict[(s, a)] = new_q_value

    Also determine delta_max, which we define to be the maximum
    amount that the absolute value of any state's value is changed
    during this iteration.
    """

    global Q_Values_Dict, Vkplus1

    delta_max = 0.0

    for state in S:
        # Loop through S to update the value of each individual state

        best_value = None
        # Will be used to track the maximum

        for action in A:
            # Calculate sum_Sp (T * (R + gamma * V)) in here
            sum_ = 0
            for state_prime in S:
                sum_ += T(state, action, state_prime) * (R(state, action, state_prime) + gamma * Vk[state_prime])

            Q_Values_Dict[(state, action)] = sum_
            # Update Q values

            if not best_value:
                best_value = sum_
                # If no action has been checked yet, the first one will be the maximum up to this point

            if sum_ > best_value:
                best_value = sum_
                # Update the maximum

        Vkplus1[state] = best_value
        # Update state value

        delta = fabs(Vk[state] - Vkplus1[state])
        if delta > delta_max:
            delta_max = delta
        # If the current state's value changed by more than any state before that,
        # it's change will be kept as delta_max

    return Vkplus1, delta_max
    # return Vk, 0  # placeholder


def return_Q_values(S, A):
    """Return the dictionary whose keys are (state, action) tuples,
    and whose values are floats representing the Q values from the
    most recent call to one_step_of_VI. This is the normal case, and
    the values of S and A passed in here can be ignored.
    However, if no such call has been made yet, use S and A to
    create the answer dictionary, and use 0.0 for all the values.
    """
    global Q_Values_Dict

    if Q_Values_Dict == {}:
        for state in S:
            for action in A:
                Q_Values_Dict[(state, action)] = 0.0

    return Q_Values_Dict  # placeholder


def extract_policy(S, A):
    """Return a dictionary mapping states to actions. Obtain the policy
    using the q-values most recently computed.  If none have yet been
    computed, call return_Q_values to initialize q-values, and then
    extract a policy.  Ties between actions having the same (s, a) value
    can be broken arbitrarily.
    """
    global Policy
    Policy = {}

    qvals = return_Q_values(S, A)
    # A local copy of the q values, that also initializes them, if needed.

    for state in S:
        best_action = None
        best_value = None
        # We use the same method for finding the maximum as before, but this time we need to track the action as well.
        for action in A:
            new_value = qvals[(state, action)]
            if not best_value:
                best_value = new_value
                best_action = action

            if new_value > best_value:
                best_action = action
                best_value = new_value

        Policy[state] = best_action
        # write the best action into the Policy dictionary

    return Policy


def apply_policy(s):
    """Return the action that your current best policy implies for state s."""
    global Policy

    return Policy[s]
    # return None  # placeholder
