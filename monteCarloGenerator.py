import copy
from gra import Gra
import random

import numpy as np

class MonteCarloGenerator:

    @staticmethod
    def generateNext(gra, size):

        def getScore(gra):

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
        for i in range(size):

            score, first =  getScore(gra)
            movesCount[first] += 1
            movesScore[first] += score

        return np.argmax([x[0]/x[1] for x in zip(movesScore,  movesCount)])
