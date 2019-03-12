"""Cubes.py
Define a cube
"""

ACTIONS = ['front-face-right', 'back-face-right', 'left-face-right', 'right-face-right', 'top-face-right',
           'bottom-face-right', 'front-face-left', 'back-face-left', 'left-face-left', 'right-face-left',
           'top-face-left', 'bottom-face-left', 'end']
# Note that an action is NOT the same thing as an operator, because
# in an MDP, the action indicates only an intended operator, and
# the actual operator that is used is random, according to the
# probability in the transition table.


class State:
    def __init__(self, d, size=None):
        self.d = d
        if size is None:
            self.size = len(d[0])
        else:
            self.size = size

    def __str__(self):
        # Produces a brief textual description of a state.
        d = self.d
        txt = ""
        txt = txt + self.print_face(d[0], "\t   ")
        txt = txt + self.print_four_faces(d[1], d[2], d[4], d[5], "")
        txt = txt + self.print_face(d[3], "\t   ")

        return txt
        
    def print_face(self, face, indent):
        txt = indent
        for row in face:
            for n in row:
                txt = txt + "[" + str(n) + "]"
            txt = txt + "\n" + indent
        return txt + "\n"
        
    def print_four_faces(self, face1, face2, face3, face4, indent):
        txt = indent
        for row in range(self.size):
            for n in face1[row]:
                txt = txt + "[" + str(n) + "]"
            txt = txt + "  "
            
            for n in face2[row]:
                txt = txt + "[" + str(n) + "]"
            
            txt = txt + "  "
            
            for n in face3[row]:
                txt = txt + "[" + str(n) + "]"
                
            txt = txt + "  "
            
            for n in face4[row]:
                txt = txt + "[" + str(n) + "]"
            txt = txt + "\n" + indent
            
        return txt + "\n"

    def __eq__(self, s2):
        if not (type(self) == type(s2)):
            return False
        d1 = self.d
        d2 = s2.d
        return d1 == d2

    def __hash__(self):
        return (str(self)).__hash__()

    def __copy__(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State([], self.size)
        for face in self.d:
            newface = copy_face(face)
            news.d.append(newface)
        
        return news

    def __lt__(self, s2):
        return True


GOAL_STATE_THREE = [
    [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ],
    [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ],
    [
        [2, 2, 2],
        [2, 2, 2],
        [2, 2, 2]],
    [
        [3, 3, 3],
        [3, 3, 3],
        [3, 3, 3]
    ],
    [
        [4, 4, 4],
        [4, 4, 4],
        [4, 4, 4]],
    [
        [5, 5, 5],
        [5, 5, 5],
        [5, 5, 5]
    ]
]
        
# Data of a completed 2x2 cube        
GOAL_STATE_TWO = [
    [
        [0, 0],
        [0, 0]
    ],
    [
        [1, 1],
        [1, 1]
    ],
    [
        [2, 2],
        [2, 2]
    ],
    [
        [3, 3],
        [3, 3]
    ],
    [
        [4, 4],
        [4, 4]
    ],
    [
        [5, 5],
        [5, 5]
    ]
]
        

INITIAL_STATE = (0, 0)


# Define the precond - since all moves can be made using a rubiks cube and all of them
# lead to a valid state, this precondition will always be true
def can_move(s):
    return True


def move(s, facenum, direction):
    news = s.__copy__()
    
    news.d[facenum] = rotate_face(s, facenum, direction)
    updated_faces = rotate_edge(s, facenum, direction)
    for newf in updated_faces:
        news.d[newf] = updated_faces[newf]
    return news


# Rotates the values on a single face (not including the edges)
# 1 -> clockwise
# -1 -> counterclockwise
def rotate_face(s, facenum, direction):
    face = s.d[facenum]
    newf = copy_face(s.d[facenum])

    if s.size == 2:
        # Rotate clockwise
        if direction == 1:
            # print("Rotate clockwise")
            for i in range(2):
                for j in range(2):
                    newf[i][j] = face[1-j][i]
    
        # Rotate counterclockwise
        elif direction == -1:
            for i in range(2):
                for j in range(2):
                    newf[i][j] = face[j][1-i]
    else:
        # Rotate clockwise
        if direction == 1:
            # print("Rotate clockwise")
            for i in range(3):
                for j in range(3):
                    newf[i][j] = face[2-j][i]
    
        # Rotate counterclockwise
        elif direction == -1:
            for i in range(3):
                for j in range(3):
                    newf[i][j] = face[j][2-i]
    
    return newf


# looking from the top, the rotated rows will be on the
def rotate_edge(s, facenum, direction):
    edge_set = edge_rotation[facenum]
    updated_faces = {}
    
    if s.size == 3:
        for i in range(4):
            
            edge_tuple = edge_set[i]
            previous_tuple = edge_set[(i-direction) % 4]
            # grab current face we are looking at
            curr_face = s.d[edge_tuple[0]]
            # grab previous face
            prev_face = s.d[previous_tuple[0]]
            # grab edge of previous face
            temp_edge = get_edge(prev_face, previous_tuple[1])
            # update edge of new face
            newf = set_edge(curr_face, edge_tuple[1], temp_edge)
            # Update face
            updated_faces[edge_tuple[0]] = newf
            # print(updated_faces)
            
    # else:
    #     if direction == 1:
    #         updated_faces = {edge_set[0][0]: s.d[edge_set[1][0]], edge_set[1][0]: s.d[edge_set[2][0]],
    #                          edge_set[2][0]: s.d[edge_set[3][0]], edge_set[3][0]: s.d[edge_set[0][0]]}
    #     else:
    #         updated_faces = {edge_set[0][0]: s.d[edge_set[3][0]], edge_set[1][0]: s.d[edge_set[0][0]],
    #                          edge_set[2][0]: s.d[edge_set[1][0]], edge_set[3][0]: s.d[edge_set[2][0]]}

    else:
        if direction == -1:
            updated_faces = {edge_set[0][0]: [s.d[edge_set[0][0]][0], s.d[edge_set[1][0]][0]],
                             edge_set[1][0]: [s.d[edge_set[1][0]][0], s.d[edge_set[2][0]][0]],
                             edge_set[2][0]: [s.d[edge_set[2][0]][0], s.d[edge_set[3][0]][0]],
                             edge_set[3][0]: [s.d[edge_set[3][0]][0], s.d[edge_set[0][0]][0]]}
        else:
            updated_faces = {edge_set[0][0]: [s.d[edge_set[0][0]][0], s.d[edge_set[3][0]][0]],
                             edge_set[1][0]: [s.d[edge_set[1][0]][0], s.d[edge_set[0][0]][0]],
                             edge_set[2][0]: [s.d[edge_set[2][0]][0], s.d[edge_set[1][0]][0]],
                             edge_set[3][0]: [s.d[edge_set[3][0]][0], s.d[edge_set[2][0]][0]]}

    return updated_faces


# Maps each face to a tuple. The first element of the tuple is an adjacent face,
# and the second element represents which edge of the adjacent face is to be
# rotated (0-top 1-right 2-bottom 3-left)
# The replacement of edge values is determined by the order of the tuples in the list.
# Each edge represented by a tuple is replaced by the previous one in the list.
edge_rotation = {0: [(1, 0), (5, 0), (4, 0), (2, 0)], 1: [(0, 3), (2, 3), (3, 3), (5, 1)],
                 2: [(0, 2), (4, 3), (3, 0), (1, 1)], 3: [(2, 2), (4, 2), (5, 2), (1, 2)],
                 4: [(2, 1), (0, 1), (5, 3), (3, 1)], 5: [(0, 0), (1, 3), (3, 2), (4, 1)]}


def get_edge(face, edge):
    if edge == 2:
        return face[edge]
    # Bottom edge is reversed because we want the values in clockwise order.
    # on the bottom this means they should be in order from right to left
    elif edge == 0:
        return list(reversed(face[edge]))
    else:
        edge_list = []
        # j is the index within the row. (edge + 1) % 3 means edge 1 -> index 2
        # edge 3 -> index 0
        j = (edge + 1) % 4
        l_ = range(3)
        if edge == 1:
            l_ = reversed(l_)
        for i in l_:
            edge_list.append(face[i][j])
        return edge_list


def set_edge(face, edge, new_edge):
    newf = copy_face(face)
    if edge == 2: 
        newf[edge] = new_edge
    elif edge == 0:
        newf[edge] = list(reversed(new_edge))
    else:
        edge_list = []
        # j is the index within the row. (edge + 1) % 3 means edge 1 -> index 2
        # edge 3 -> index 0
        j = (edge + 1) % 4
        l_ = range(3)
        n = 0
        # Reverse row index if edge = 3
        if edge == 1:
            l_ = reversed(l_)
        for i in l_:
            newf[i][j] = new_edge[n]
            n += 1
    
    return newf
    

def copy_face(face):
    newf = []
    for row in face:
        newr = []
        for n in row:
            newr.append(n)
        newf.append(newr)

    return newf


# Define operators
class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


frontFaceRightOp = Operator("Turn the front face to the right",
                            lambda s: can_move(s),
                            lambda s: move(s, 2, 1))

frontFaceLeftOp = Operator("Turn the front face to the left",
                           lambda s: can_move(s),
                           lambda s: move(s, 2, -1))

backFaceRightOp = Operator("Turn the back face to the right",
                           lambda s: can_move(s),
                           lambda s: move(s, 5, 1))

backFaceLeftOp = Operator("Turn the back face to the left",
                          lambda s: can_move(s),
                          lambda s: move(s, 5, -1))

leftFaceRightOp = Operator("Turn the left face to the right",
                           lambda s: can_move(s),
                           lambda s: move(s, 1, 1))

leftFaceLeftOp = Operator("Turn the left face to the left",
                          lambda s: can_move(s),
                          lambda s: move(s, 1, -1))

rightFaceRightOp = Operator("Turn the right face to the right",
                            lambda s: can_move(s),
                            lambda s: move(s, 4, 1))

rightFaceLeftOp = Operator("Turn the right face to the left",
                           lambda s: can_move(s),
                           lambda s: move(s, 4, -1))
                   
topFaceRightOp = Operator("Turn the top face to the right",
                          lambda s: can_move(s),
                          lambda s: move(s, 0, 1))

topFaceLeftOp = Operator("Turn the top face to the left",
                         lambda s: can_move(s),
                         lambda s: move(s, 0, -1))

bottomFaceRightOp = Operator("Turn the bottom face to the right",
                             lambda s: can_move(s),
                             lambda s: move(s, 3, 1))

bottomFaceLeftOp = Operator("Turn the bottom face to the left",
                            lambda s: can_move(s),
                            lambda s: move(s, 3, -1))
                   
OPERATORS = [bottomFaceLeftOp, bottomFaceRightOp, topFaceLeftOp, topFaceRightOp, rightFaceLeftOp, rightFaceRightOp,
             leftFaceLeftOp, leftFaceRightOp, backFaceLeftOp, backFaceRightOp, frontFaceLeftOp, frontFaceRightOp]

# The following dictionary maps each action (except the End action)
# to the three operators that might be randomly chosen to perform it.
# In this MDP, the first gets probability P_normal, and the other two
# each get probability P_noise.


ActionOps = {'bottomFaceLeft': bottomFaceLeftOp,
             'bottomFaceRight': bottomFaceRightOp,
             'topFaceLeft':  topFaceLeftOp,
             'topFaceRight':  topFaceRightOp,
             'rightFaceLeft':  rightFaceLeftOp,
             'rightFaceRight':  rightFaceRightOp,
             'leftFaceLeft':  leftFaceLeftOp,
             'leftFaceRight':  leftFaceRightOp,
             'backFaceLeft':  backFaceLeftOp,
             'backFaceRight':  backFaceRightOp,
             'frontFaceLeft': frontFaceLeftOp,
             'frontFaceRight': frontFaceRightOp}


# Transition probability
def T(s, a, sp):
    """Compute the transition probability for going from state s to
       state sp after taking action a."""
    if ActionOps[a].apply(s) == sp:
        return 1.0
    return 0.0  # Default case is probability 0.
    

# Reward function
def threesReward(state, action, state_p):
    """Return the reward associated with transitioning from s to sp via action a."""
    if state == GOAL_STATE_THREE:
        return 1.0  # the Goal has been reached
    
    return -0.01   # cost of living.


def reward(state=None, size=2, cost=0.0):
    if state is None:
        return 0.0

    if size == 2:
        if state.d == GOAL_STATE_TWO:
            return 1.0
        else:
            return 0.0

    elif size == 3:
        if state.d == GOAL_STATE_THREE:
            return 1.0
        else:
            return 0.0

    else:
        return cost


# testcube = State(GOAL_STATE_TWO)
# print(testcube)
# testcube = move(testcube, 3, -1)
# print(testcube)
# testcube = move(testcube, 2, 1)
# print(testcube)
# testcube = move(testcube, 4, -1)
# print(testcube)
# testcube = move(testcube, 5, 1)
# print(testcube)
