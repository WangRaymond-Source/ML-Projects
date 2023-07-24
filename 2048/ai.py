from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])
        
        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        return len(self.children) == 0

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    #self.simulator.get_open_tiles()
    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node = None, depth = 0):
        #deep Copy current state
        #set the state of the current node
        self.simulator.set_state(node.state[0], node.state[1])
        state = copy.deepcopy(self.simulator.current_state())
        # matrix state
        saveState = state[0]
        # matrix score
        saveScore = state[1]
        # up = self.simulator.move(0)
        # self.simulator.set_state(saveState,saveScore)
        # left = self.simulator.move(1)
        # self.simulator.set_state(saveState,saveScore)
        # down = self.simulator.move(2)
        # self.simulator.set_state(saveState,saveScore)
        # right = self.simulator.move(3)
        # self.simulator.set_state(saveState,saveScore)
        if depth == 0:
            return
        elif node.player_type == CHANCE_PLAYER:
            list_tile = self.simulator.get_open_tiles()
            for (x,y) in list_tile:
                # get the board
                board = copy.deepcopy(saveState)
                # change the tile from 0 to 2
                board[x][y] = 2
                # sets the state
                self.simulator.set_state(board, saveScore)
                # make the state a node--- gets the state
                n = Node(copy.deepcopy(self.simulator.current_state()),MAX_PLAYER)
                node.children.append((None,n))
                # recurse
                self.build_tree(n,depth - 1)
            return
        elif node.player_type == MAX_PLAYER:
            moves = [0,2,1,3]
            for x in moves:
                if self.simulator.move(x):
                    n0 = Node(copy.deepcopy(self.simulator.current_state()),CHANCE_PLAYER)
                    node.children.append((x,n0))
                    self.build_tree(n0, depth - 1)
                self.simulator.set_state(saveState,saveScore)
            # if self.simulator.move(0):
            #     n0 = Node(copy.deepcopy(self.simulator.current_state()),CHANCE_PLAYER)
            #     node.children.append((0,n0))
            #     self.build_tree(n0, depth - 1)
            # self.simulator.set_state(saveState,saveScore)
            # if self.simulator.move(2):
            #     n2 = Node(copy.deepcopy(self.simulator.current_state()),CHANCE_PLAYER)
            #     node.children.append((2,n2))
            #     self.simulator.set_state(saveState,saveScore)
            #     self.build_tree(n2, depth - 1)
            # self.simulator.set_state(saveState,saveScore)
            # if self.simulator.move(1):
            #     n1 = Node(copy.deepcopy(self.simulator.current_state()),CHANCE_PLAYER)
            #     node.children.append((1,n1))
            #     self.build_tree(n1, depth - 1)
            # self.simulator.set_state(saveState,saveScore)
            # if self.simulator.move(3):
            #     n3 = Node(copy.deepcopy(self.simulator.current_state()),CHANCE_PLAYER)
            #     node.children.append((3,n3))
            #     self.build_tree(n3, depth - 1)
            # self.simulator.set_state(saveState,saveScore)
            return

    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        #print tree
        # for n in self.root.children:
        #     print((n[0], n[1].state[1]))
        # print("-------")
        # to store a list of (direction, node) tuples
        if node.is_terminal():
            return (None, node.state[1])
        elif MAX_PLAYER == node.player_type:
            value = -1
            direction = None
            for n in node.children:
                preV = value
                value = max(value, self.expectimax(n[1])[1])
                if preV != value:
                    direction = n[0]
            return (direction, value)
        elif CHANCE_PLAYER == node.player_type:
            value = 0
            for n in node.children:
                value += self.expectimax(n[1])[1]
            value = value / len(node.children)
            return (None, value)
        else:
            return
    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction
        #return random.randint(0, 3)

