import copy
from random import *

import numpy

from model.gra import Gra


class MiniMax:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game, branching_factor=8, search_depth=2, heuristic=None):
        self.root: Gra = game  # GameNode
        self.currentNode = None  # GameNode
        self.successors = []  # List of GameNodes
        self.branching_factor = branching_factor
        self.search_depth = search_depth
        self.heuristic = heuristic
        self.root_Successors = None
        return

    def search(self):
        return self.minimax(self.root)

    def minimax(self, node: Gra):
        # first, find the max value
        best_val = self.max_value(node)  # should be root node of tree

        # second, find the node which HAS that max value
        #  --> means we need to propagate the values back up the
        #      tree as part of our minimax algorithm
        successors = self.root_Successors
        print("MiniMax:  Utility Value of Root Node: = " + str(best_val))
        # find the node with our best move
        best_move = None
        for elem in successors:  # ---> Need to propagate values up tree for this to work
            if elem.next_move_value == best_val:
                best_move = elem.next_move
                break
        if best_val == 0:
            best_move = randrange(4)
        # return that best value that we've found
        return best_move

    def max_value(self, node: Gra):

        if self.isTerminal(node):
            return self.getUtility(node)

        infinity = float('inf')
        max_value = -infinity

        successors_states = self.get_4_Successors(node)
        if node.search_depth == 0:
            self.root_Successors = successors_states
        for state in successors_states:
            max_value = max(max_value, self.avg_value(state))
        node.next_move_value = max_value
        return max_value

    def avg_value(self, node: Gra):

        if self.isTerminal(node):
            return self.getUtility(node)

        infinity = float('inf')
        min_value = infinity

        successor_states = self.get_k_Successors(node)
        min_value = min(min_value, numpy.mean([self.max_value(state) for state in successor_states]))
        node.next_move_value = min_value
        return min_value

    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def get_4_Successors(self, node: Gra):
        assert node is not None
        nodes = [copy.deepcopy(node) for k in range(4) if node.can_move(k)]
        succesors = [el.setNextMove(k).increment_depth() for el, k in zip(nodes, range(4))]
        return succesors

    def get_k_Successors(self, node: Gra):
        assert node is not None
        successors = [copy.deepcopy(node) for k in range(self.branching_factor)]
        for succesor in successors:
            succesor.move(node.next_move)
        return successors

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node: Gra):
        assert node is not None
        isOver = False if node.notOver() else True
        if isOver:
            pass
        isMaxDepth = node.search_depth >= self.search_depth
        return isOver or isMaxDepth

    def getUtility(self, node: Gra):
        assert node is not None
        value = self.heuristic(node.table.plansza)
        return value
