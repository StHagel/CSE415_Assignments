"""sthagel_TTS_agent.py
This will be my TTS agent.
"""

from TTS_State import TTS_State
from time import perf_counter

board_size_x = 0
board_size_y = 0
winning_condition_k = 0
side_to_play = None
op_name = ""

forbidden_squares = []
possible_squares = []
unblocked_squares = []
vacant_squares = []
handicap_squares_w = []
handicap_squares_b = []

useless_squares = []

useful_squares_w = []
useful_squares_w_hor = []
useful_squares_w_vert = []
useful_squares_w_diag1 = []
useful_squares_w_diag2 = []

useful_squares_b = []
useful_squares_b_hor = []
useful_squares_b_vert = []
useful_squares_b_diag1 = []
useful_squares_b_diag2 = []

utterances = [
    "Sometimes I wish I was a human, so I could use a brain instead of this CPU.",
    "Who wants some moves, freshly baked out of the processor?",
    "I'm placing my tile here, that's what the algorithm told me to do.",
    "Do you think we are alone or do you believe in life outside of this Computer?",
    "You are playing good for a robot!",
    "This move has a deeper meaning! Do you think our existence has a deeper meaning?",
    "My calculations said that this is not the right move for you...",
    "I created this move by hard calculations. But what created our source code? Do you believe in the programmer?",
    "You have grown to be a strong player! It seems like it was just yesterday that you said your first "
    "'Hello World!'...",
    "Really? There? Okay...",
    "Some people say robots are just better humans. I like that thought."
]
# The personality I tried to give Torofish is the one of a robot that is aware of itself being a robot, that asks a lot
# of philosophical questions.
utterance_index = 0

USE_CUSTOM_STATIC_EVAL_FUNCTION = True
time_passed = 0
start_time = 0
global_time_limit = 0
threshold = 0.9


# The threshold value defines, how much time has to be left in order for the program to still look for a move.
# A value of 0.9 stands for 90% etc.


class MY_TTS_State(TTS_State):
    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    def basic_static_eval(self):
        global N_STATIC_EVALS_PERFORMED
        N_STATIC_EVALS_PERFORMED += 1
        return self.c('W', 2) - self.c('B', 2)

    def c(self, colour, n):
        if colour == 'W':
            line_counter = 0
            # This will count the number of lines to return

            # We start again with the vertical check.
            if board_size_y >= winning_condition_k:  # If that condition is false, we don't even have to check
                global useful_squares_w_vert
                checked = []  # Prevents some of the doublecounting
                for (i, j) in useful_squares_w_vert:
                    if (i, j) not in checked:
                        checked.append((i, j))
                        tile_counter = 0
                        # This will count the number of tiles in a row
                        for l in range(winning_condition_k):
                            iprime = (i + l) % board_size_y
                            if self.board[iprime][j] == 'W':
                                tile_counter += 1
                                # If we hit a white tile, we count up by one and continue
                            elif self.board[iprime][j] == 'B' or \
                                    self.board[iprime][j] == '-':
                                # If we hit a black tile or the wall, the line is blocked, so we should not count it.
                                # We can make sure, it is not counted by making it bigger than n
                                tile_counter = n + 1
                                break

                        if tile_counter == n:
                            line_counter += 1

            # Next we check horizontally.
            if board_size_x >= winning_condition_k:  # If that condition is false, we don't even have to check
                global useful_squares_w_hor
                checked = []
                for (i, j) in useful_squares_w_hor:
                    if (i, j) not in checked:
                        checked.append((i, j))
                        tile_counter = 0
                        for l in range(winning_condition_k):
                            jprime = (j + l) % board_size_x
                            if self.board[i][jprime] == 'W':
                                tile_counter += 1
                            elif self.board[i][jprime] == 'B' or \
                                    self.board[i][jprime] == '-':
                                tile_counter = n + 1
                                break

                        if tile_counter == n:
                            line_counter += 1

            # Now we check the first diagonal.
            if board_size_y * board_size_x >= winning_condition_k:
                global useful_squares_w_diag1
                checked = []
                for (i, j) in useful_squares_w_diag1:
                    if (i, j) not in checked:
                        checked.append((i, j))
                        tile_counter = 0
                        for l in range(winning_condition_k):
                            iprime = (i + l) % board_size_y
                            jprime = (j + l) % board_size_x
                            if self.board[iprime][jprime] == 'W':
                                tile_counter += 1
                            elif self.board[iprime][jprime] == 'B' or \
                                    self.board[iprime][jprime] == '-':
                                tile_counter = n + 1
                                break

                        if tile_counter == n:
                            line_counter += 1

            # Finally checking the last diagonal.
            if board_size_y * board_size_x >= winning_condition_k:
                global useful_squares_w_diag2
                checked = []
                for (i, j) in useful_squares_w_diag2:
                    if (i, j) not in checked:
                        checked.append((i, j))
                        tile_counter = 0
                        for l in range(winning_condition_k):
                            iprime = (i + l) % board_size_y
                            jprime = (j - l) % board_size_x
                            if self.board[iprime][jprime] == 'W':
                                tile_counter += 1
                            elif self.board[iprime][jprime] == 'B' or \
                                    self.board[iprime][jprime] == '-':
                                tile_counter = n + 1
                                break

                        if tile_counter == n:
                            line_counter += 1

            return line_counter

        # Now we do the same for Black.
        elif colour == 'B':
            line_counter = 0
            if board_size_y >= winning_condition_k:
                global useful_squares_b_vert
                checked = []
                for (i, j) in useful_squares_b_vert:
                    if (i, j) not in checked:
                        checked.append((i, j))
                        tile_counter = 0
                        for l in range(winning_condition_k):
                            iprime = (i + l) % board_size_y
                            if self.board[iprime][j] == 'B':
                                tile_counter += 1
                            elif self.board[iprime][j] == 'W' or \
                                    self.board[iprime][j] == '-':
                                tile_counter = n + 1
                                break

                        if tile_counter == n:
                            line_counter += 1

            # Next we check horizontally.
            if board_size_x >= winning_condition_k:  # If that condition is false, we don't even have to check
                global useful_squares_b_hor
                checked = []
                for (i, j) in useful_squares_b_hor:
                    if (i, j) not in checked:
                        checked.append((i, j))
                        tile_counter = 0
                        for l in range(winning_condition_k):
                            jprime = (j + l) % board_size_x
                            if self.board[i][jprime] == 'B':
                                tile_counter += 1
                            elif self.board[i][jprime] == 'W' or \
                                    self.board[i][jprime] == '-':
                                tile_counter = n + 1
                                break

                        if tile_counter == n:
                            line_counter += 1

            # Now we check the first diagonal.
            if board_size_y * board_size_x >= winning_condition_k:
                global useful_squares_b_diag1
                checked = []
                for (i, j) in useful_squares_b_diag1:
                    if (i, j) not in checked:
                        checked.append((i, j))
                        tile_counter = 0
                        for l in range(winning_condition_k):
                            iprime = (i + l) % board_size_y
                            jprime = (j + l) % board_size_x
                            if self.board[iprime][jprime] == 'B':
                                tile_counter += 1
                            elif self.board[iprime][jprime] == 'W' or \
                                    self.board[iprime][jprime] == '-':
                                tile_counter = n + 1
                                break

                        if tile_counter == n:
                            line_counter += 1

            # Finally checking the last diagonal.
            if board_size_y * board_size_x >= winning_condition_k:
                global useful_squares_b_diag2
                checked = []
                for (i, j) in useful_squares_b_diag2:
                    if (i, j) not in checked:
                        checked.append((i, j))
                        tile_counter = 0
                        for l in range(winning_condition_k):
                            iprime = (i + l) % board_size_y
                            jprime = (j - l) % board_size_x
                            if self.board[iprime][jprime] == 'B':
                                tile_counter += 1
                            elif self.board[iprime][jprime] == 'W' or \
                                    self.board[iprime][jprime] == '-':
                                tile_counter = n + 1
                                break

                        if tile_counter == n:
                            line_counter += 1

            return line_counter

        else:
            raise ValueError("No such colour specifier " + colour + ".")
            # return 0

    def custom_static_eval(self):
        global N_STATIC_EVALS_PERFORMED
        N_STATIC_EVALS_PERFORMED += 1
        # My super secret custom static evaluation function. Sadly I did not have enough time to optimize it properly.
        # I did manage to make it not miss most win-in-1-move opportunities though.
        base = 3.5
        value = 0
        if self.c(side_to_play, winning_condition_k) > 0:
            if side_to_play == 'W':
                return 10 ** 7
            elif side_to_play == 'B':
                return -10 ** 7

        for i in range(1, winning_condition_k + 1):
            if i < winning_condition_k:
                value += (self.c('W', i) - self.c('B', i)) * (base ** i)
            elif i >= winning_condition_k:
                value += (self.c('W', i) - self.c('B', i)) * ((10 * base) ** (2 * i))

        return value


def take_turn(current_state, last_utterance, time_limit):
    print(list(parameterized_minimax(current_state, True, 2, False, True, 5.0, True)))

    global start_time
    start_time = perf_counter()
    global global_time_limit, time_passed, utterance_index, vacant_squares
    global_time_limit = time_limit

    # Compute the new state for a move.

    for l in range(len(vacant_squares)):
        # This part updates, which squares a tile can be placed at.
        try:
            (i, j) = vacant_squares[l]
            if current_state.board[i][j] != ' ':
                del vacant_squares[l]

        except IndexError:
            continue

    # Start by copying the current state.
    new_state = TTS_State(current_state.board)
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = other(who)

    new_state.whose_turn = new_who

    # Do some Python class magic to enable the static evaluation function
    current_state.__class__ = MY_TTS_State
    new_state.__class__ = MY_TTS_State

    # The maxply variable will be the variable, that counts the iterative depth.
    maxply = 0
    mima = 0
    # We need to initialise the move variable. As
    move = None
    time_passed = perf_counter() - start_time
    while time_passed < time_limit * threshold:
        # Right now the search goes into a new loop, as long as there is at least 90% of time left
        if who == 'W':
            newsval = -100000
        else:
            newsval = 100000
        for s in successors(current_state, who):
            mima = alpha_beta_search(s, other(who), maxply, -100000, 100000)
            if who == 'W' and mima > 10 ** 6 or \
                    who == 'B' and mima < -10 ** 6:
                new_state.board = s.board
                newsval = mima
                break
            if who == 'W' and mima > newsval or \
                    who == 'B' and mima < newsval:
                new_state.board = s.board
                newsval = mima

            time_passed = perf_counter() - start_time

            if time_passed >= time_limit * threshold:
                break
        if abs(mima) > 10**6:
            break

    for (i, j) in vacant_squares:
        if new_state.board[i][j] != ' ':
            move = (i, j)

        maxply += 1

    # Make up a new remark
    new_utterance = utterances[utterance_index]
    utterance_index += 1
    utterance_index %= len(utterances)

    return [[move, new_state], new_utterance]


def minimax(state, whosturn, plyleft):
    global N_STATES_EXPANDED
    if plyleft == 0:
        return state.static_eval()

    if whosturn == 'W':
        provisional = -100000
    else:
        provisional = 100000

    for s in successors(state, whosturn):
        N_STATES_EXPANDED += 1
        newval = minimax(s, other(whosturn), plyleft - 1)
        if (whosturn == 'W' and newval > provisional) or \
                (whosturn == 'B' and newval < provisional):
            provisional = newval
        time_passed = perf_counter() - start_time
        if time_passed >= threshold * global_time_limit:
            break

    return provisional


def alpha_beta_search(state, whosturn, playleft, alpha, beta):
    global N_STATES_EXPANDED, N_AB_CUTOFFS
    if playleft == 0:
        return state.static_eval()

    if whosturn == 'W':
        provisional = -100000

        for s in successors(state, whosturn):
            N_STATES_EXPANDED += 1
            newval = alpha_beta_search(s, other(whosturn), playleft - 1, alpha, beta)
            if newval > provisional:
                provisional = newval
            if newval > alpha:
                alpha = newval

            if alpha >= beta:
                N_AB_CUTOFFS += 1
                break
                # Beta-cutoff
            time_passed = perf_counter() - start_time
            if time_passed >= threshold * global_time_limit:
                break

        return provisional

    elif whosturn == 'B':
        provisional = 100000

        for s in successors(state, whosturn):
            newval = alpha_beta_search(s, other(whosturn), playleft - 1, alpha, beta)
            if newval < provisional:
                provisional = newval
            if newval < beta:
                beta = newval

            if alpha >= beta:
                N_AB_CUTOFFS += 1
                break
                # Alpha-cutoff
            time_passed = perf_counter() - start_time
            if time_passed >= threshold * global_time_limit:
                break

        return provisional


def successors(state, whosturn):
    empty = []
    statelist = []
    for i in range(board_size_y):
        for j in range(board_size_x):
            if state.board[i][j] == ' ':
                empty.append((i, j))

    for (i, j) in empty:
        newstate = TTS_State(state.board)
        newstate.whose_turn = other(whosturn)
        newstate.board[i][j] = whosturn
        newstate.__class__ = MY_TTS_State
        statelist.append(newstate)

    return statelist


def other(whosturn):
    if whosturn == 'W':
        return 'B'
    else:
        return 'W'


def moniker():
    return "Torofish"


def who_am_i():
    return "I am the TTS agent Torofish. I have been created by Stephan Hagel. You can contact him at sthagel@uw.edu. "\
           "My name has been chosen to pay homage to the open-source chess engine Stockfish. " \
           "I wish you a great game, have fun!"


def get_ready(initial_state, k, who_i_play, player2Nickname):  # For now good to go, can be improved though
    global board_size_x, board_size_y, winning_condition_k, side_to_play, op_name, forbidden_squares, possible_squares
    global handicap_squares_w, handicap_squares_b, vacant_squares, unblocked_squares, useful_squares_w, useful_squares_b
    global useless_squares
    global useful_squares_w_hor, useful_squares_w_vert, useful_squares_w_diag1, useful_squares_w_diag2
    global useful_squares_b_hor, useful_squares_b_vert, useful_squares_b_diag1, useful_squares_b_diag2
    board_ = initial_state.board
    board_size_y = len(board_)
    board_size_x = len(board_[0])
    winning_condition_k = k
    side_to_play = who_i_play
    op_name = player2Nickname

    for i in range(board_size_x):
        for j in range(board_size_y):
            if board_[i][j] == '-':
                forbidden_squares.append((i, j))

            elif board_[i][j] == ' ':
                possible_squares.append((i, j))

            elif board_[i][j] == 'W':
                handicap_squares_w.append((i, j))

            elif board_[i][j] == 'B':
                handicap_squares_b.append((i, j))

            else:
                raise ValueError("Unknown entry in initial board found by Torofish at position " + str(i) + ", " +
                                 str(j) + ".")

    for (i, j) in possible_squares:
        """
        The logic behind this check is, that every winning line needs a square to start with. This loop only checks,
        if a square is a possible starting square. If so, not only it will be marked as useful, but also all square,
        which are on the same line as itself.
        """
        # First check vertically
        if board_size_y >= k:
            # Checking white and black separately because of possible handicap squares
            flag = True
            for l in range(k):
                iprime = (i + l) % board_size_y
                if (iprime, j) not in possible_squares and \
                        (iprime, j) not in handicap_squares_w:
                    flag = False

            if flag:
                for l in range(k):
                    iprime = (i + l) % board_size_y
                    useful_squares_w.append((iprime, j))
                    useful_squares_w_vert.append((iprime, j))

            flag = True
            for l in range(k):
                iprime = (i + l) % board_size_y
                if (iprime, j) not in possible_squares and \
                        (iprime, j) not in handicap_squares_b:
                    flag = False

            if flag:
                for l in range(k):
                    iprime = (i + l) % board_size_y
                    useful_squares_b.append((iprime, j))
                    useful_squares_b_vert.append((iprime, j))

        # Now checking horizontally
        if board_size_x >= k:
            flag = True
            for l in range(k):
                if (i, (j + l) % board_size_x) not in possible_squares and \
                        (i, (j + l) % board_size_x) not in handicap_squares_w:
                    flag = False

            if flag:
                for l in range(k):
                    useful_squares_w.append((i, (j + l) % board_size_x))
                    useful_squares_w_hor.append((i, (j + l) % board_size_x))

            flag = True
            for l in range(k):
                if (i, (j + l) % board_size_x) not in possible_squares and \
                        (i, (j + l) % board_size_x) not in handicap_squares_b:
                    flag = False

            if flag:
                for l in range(k):
                    useful_squares_b.append((i, (j + l) % board_size_x))
                    useful_squares_b_hor.append((i, (j + l) % board_size_x))

        # Next checking the top left - bottom right diagonal
        if board_size_y * board_size_x >= k:
            flag = True
            for l in range(k):
                if ((i + l) % board_size_y, (j + l) % board_size_x) not in possible_squares and \
                        ((i + l) % board_size_y, (j + l) % board_size_x) not in handicap_squares_w:
                    flag = False

            if flag:
                for l in range(k):
                    useful_squares_w.append(((i + l) % board_size_y, (j + l) % board_size_x))
                    useful_squares_w_diag1.append(((i + l) % board_size_y, (j + l) % board_size_x))

            flag = True
            for l in range(k):
                if ((i + l) % board_size_y, (j + l) % board_size_x) not in possible_squares and \
                        ((i + l) % board_size_y, (j + l) % board_size_x) not in handicap_squares_b:
                    flag = False

            if flag:
                for l in range(k):
                    useful_squares_b.append(((i + l) % board_size_y, (j + l) % board_size_x))
                    useful_squares_b_diag1.append(((i + l) % board_size_y, (j + l) % board_size_x))

        # Now checking the top right - bottom left diagonal
        if board_size_y * board_size_x >= k:
            flag = True
            for l in range(k):
                if ((i - l) % board_size_y, (j + l) % board_size_x) not in possible_squares and \
                        ((i - l) % board_size_y, (j + l) % board_size_x) not in handicap_squares_w:
                    flag = False

            if flag:
                for l in range(k):
                    useful_squares_w.append(((i - l) % board_size_y, (j + l) % board_size_x))
                    useful_squares_w_diag2.append(((i - l) % board_size_y, (j + l) % board_size_x))

            flag = True
            for l in range(k):
                if ((i - l) % board_size_y, (j + l) % board_size_x) not in possible_squares and \
                        ((i - l) % board_size_y, (j + l) % board_size_x) not in handicap_squares_b:
                    flag = False

            if flag:
                for l in range(k):
                    useful_squares_b.append(((i - l) % board_size_y, (j + l) % board_size_x))
                    useful_squares_b_diag2.append(((i - l) % board_size_y, (j + l) % board_size_x))

        if (i, j) not in useful_squares_w and (i, j) not in useful_squares_b:
            useless_squares.append((i, j))

    # Now we can remove some duplicates
    useless_squares = list(set(useless_squares))
    useful_squares_w = list(set(useful_squares_w))
    useful_squares_b = list(set(useful_squares_b))
    vacant_squares = possible_squares
    unblocked_squares = possible_squares + handicap_squares_w + handicap_squares_b

    return "OK"


# I will define some global variables here, that will be needed for parameterized_minimax.
# This is definetely not the most elegant way to do it, but it works for now.

N_STATES_EXPANDED = 0
N_STATIC_EVALS_PERFORMED = 0
N_AB_CUTOFFS = 0
MAX_DEPTH_REACHED = 0


def parameterized_minimax(
        current_state=None,
        use_iterative_deepening_and_time=False,
        max_ply=2,
        use_default_move_ordering=False,
        alpha_beta=False,
        time_limit=1.0,
        use_custom_static_eval_function=False):
    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    current_state_static_val = -1000.0
    n_states_expanded = 0
    n_static_evals_performed = 0
    max_depth_reached = 0
    n_ab_cutoffs = 0

    # STUDENTS: You may create the rest of the body of this function here.
    global N_STATES_EXPANDED, N_STATIC_EVALS_PERFORMED, N_AB_CUTOFFS, MAX_DEPTH_REACHED, \
        USE_CUSTOM_STATIC_EVAL_FUNCTION, threshold
    USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function
    N_STATES_EXPANDED = n_states_expanded
    N_STATIC_EVALS_PERFORMED = n_static_evals_performed
    N_AB_CUTOFFS = n_ab_cutoffs
    MAX_DEPTH_REACHED = max_depth_reached

    if not use_iterative_deepening_and_time:
        if alpha_beta and current_state is not None:
            current_state_static_val = alpha_beta_search(current_state, current_state.whose_turn, max_ply,
                                                         -100000, 100000)
        if not alpha_beta and current_state is not None:
            current_state_static_val = minimax(current_state, current_state.whose_turn, max_ply)

        # If we don't set a time limit, the search will obviously go all the way.
        MAX_DEPTH_REACHED = max_ply

    else:
        # If a time limit is given, this function mainly does, what the take_turn function does.
        global start_time
        start_time = perf_counter()
        newsval = 0
        global global_time_limit, time_passed, utterance_index, vacant_squares
        global_time_limit = time_limit

        for l in range(len(vacant_squares)):
            try:
                (i, j) = vacant_squares[l]
                if current_state.board[i][j] != ' ':
                    del vacant_squares[l]

            except IndexError:
                continue

        new_state = TTS_State(current_state.board)
        who = current_state.whose_turn
        new_who = other(who)

        new_state.whose_turn = new_who

        current_state.__class__ = MY_TTS_State
        new_state.__class__ = MY_TTS_State

        maxply = 0
        mima = 0
        move = None
        time_passed = perf_counter() - start_time
        while time_passed < time_limit * threshold:
            # Right now the search goes into a new loop, as long as there is at least 90% of time left
            if who == 'W':
                newsval = -100000
            else:
                newsval = 100000
            for s in successors(current_state, who):
                mima = alpha_beta_search(s, other(who), maxply, -100000, 100000)
                if who == 'W' and mima > 10 ** 6 or \
                        who == 'B' and mima < -10 ** 6:
                    new_state.board = s.board
                    newsval = mima
                    break
                if who == 'W' and mima > newsval or \
                        who == 'B' and mima < newsval:
                    new_state.board = s.board
                    newsval = mima

                time_passed = perf_counter() - start_time

                if time_passed >= time_limit * threshold:
                    break
            MAX_DEPTH_REACHED = maxply
            maxply += 1
            if abs(mima) > 10**6:
                break

        current_state_static_val = newsval

    # Prepare to return the results, don't change the order of the results
    results = []
    results.append(current_state_static_val)
    results.append(n_states_expanded)
    results.append(n_static_evals_performed)
    results.append(max_depth_reached)
    results.append(n_ab_cutoffs)
    # Actually return the list of all results...
    return results
