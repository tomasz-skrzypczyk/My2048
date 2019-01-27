import copy
import random

import numpy as np

from model.gra import Gra


class MonteCarloGenerator:

    @staticmethod
    def generateNext(gra: Gra, steps):

        def getScore(gra: Gra):

            simulation = copy.deepcopy(gra)
            first = random.randint(0,3)
            if simulation.notOver():
                moved = simulation.move(first)
            else:
                raise ValueError("Nie ma ruchu")
            if moved:
                while simulation.notOver():
                    simulation.move(random.randint(0, 3))
                return simulation.score, first
            else:
                return 0, first


        movesScore = [0,0,0,0]
        movesCount = [0,0,0,0]
        for _ in range(steps):
            score, first = getScore(gra)
            movesCount[first] += 1
            movesScore[first] += score
        movesCount = [1 if x == 0 else x for x in movesCount]
        return np.argmax([x[0]/x[1] for x in zip(movesScore,  movesCount)])
