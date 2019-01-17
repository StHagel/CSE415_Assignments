'''sthagel_Farmer_Fox.py
by Stephan Hagel

Assignment 2, in CSE 415, Winter 2019.

This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''


# <METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Farmer Fox"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['S. Hagel']
PROBLEM_CREATION_DATE = "17-JAN-2018"
PROBLEM_DESC = \
    '''This formulation of the Farmer, fox, chicken, grain problem uses generic
    Python 3 constructs and has been tested with Python 3.6.
    It is designed to work according to the QUIET2 tools interface.
    '''
# </METADATA>


# <COMMON_CODE>
# Seems good, needs testing though
class State:
    def __init__(self, d):
        self.d = d

    def __eq__(self, s2):
        for bank in ['left', 'right']:
            for entity in self.d[bank]:
                if entity not in s2.d[bank]:
                    return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        txt = "["
        for peg in ['left', 'right']:
            txt += str(self.d[peg]) + " ,"
        return txt[:-2] + "]"

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        for bank in ['left', 'right']:
            news.d[bank] = self.d[bank][:]
        return news

    def can_move(self, passenger):
        # Test, if it is legal, to bring the farmer and the passenger from the _from bank to the _to bank.
        try:
            if 'F' in self.d['left']:
                _from = 'left'
                _to = 'right'
            else:
                _from = 'right'
                _to = 'left'

            from_bank = self.d[_from]  # The bank that the boat leaves from

            if passenger != '' and passenger not in from_bank:
                return False  # The passenger is not at the "from" bank

            temp_list = []  # This will hold the entities (f,c,g), that will be left behind, if the move is performed.

            for entity in from_bank:
                if entity != 'F' and entity != passenger:
                    temp_list.append(entity)

            # Sanity check
            if 'F' in temp_list or passenger in temp_list:
                print("An unexpected error occurred in State.can_move().")
                return False

            if 'f' in temp_list and 'c' in temp_list:
                return False  # The fox eats the chicken

            if 'c' in temp_list and 'g' in temp_list:
                return False  # The chicken eats the grain

            return True
        except Exception as e:
            print(e)

    def move(self, passenger):
        """Assuming it's legal to make the move, this computes
           the new state resulting from moving the topmost disk
           from the From peg to the To peg."""
        news = self.copy()  # start with a deep copy.

        if 'F' in self.d['left']:
            _from = 'left'
            _to = 'right'
        else:
            _from = 'right'
            _to = 'left'

        if passenger != '':
            news.d[_to] = self.d[_to] + ['F', passenger]  # The farmer and passenger cross the river
        else:
            news.d[_to] = self.d[_to] + ['F']  # Only the farmer crosses the river

        temp_list = []  # This list will contain the entities left behind
        for entity in self.d[_from]:
            if entity != 'F' and entity != passenger:
                temp_list.append(entity)

        news.d[_from] = temp_list

        return news  # return new state


# DONE
def goal_test(s):
    # If no one is on the left side of the river, the puzzle is solved.
    return s.d['left'] == []


# DONE
def goal_message(s):
    return "Everyone crossed the river safely!"


# DONE
class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

# </COMMON_CODE>


# <INITIAL_STATE>
INITIAL_DICT = {'left': ['F', 'f', 'c', 'g'], 'right': []}
CREATE_INITIAL_STATE = lambda: State(INITIAL_DICT)
# DUMMY_STATE =  {'left':[], 'right':[]}
# </INITIAL_STATE>

# <OPERATORS>
possible_passengers = ['', 'f', 'c', 'g']
name_dict = {'f': 'fox', 'c': 'chicken', 'g': 'grain', '': ''}

OPERATORS = [Operator("Farmer and " + name_dict[entity] + " cross the river",
                      lambda s, ent=entity: s.can_move(ent),
                      lambda s, ent=entity: s.move(ent))
             for entity in possible_passengers]
# </OPERATORS>


# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>


# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>
