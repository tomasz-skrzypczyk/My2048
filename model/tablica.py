import random

import numpy as np


class Tablica:
    def __init__(self, size):
        self.size = size
        self.plansza = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        self.generate()
        self.generate()
        self.nextLeft = self.plansza
        self.nextRight = self.plansza
        self.nextUp = self.plansza
        self.nextDown = self.plansza
        self.leftPoints = 0
        self.rightPoints = 0
        self.upPoints = 0
        self.downPoints = 0

    def toList(self):
        return [item for sublist in self.plansza for item in sublist]

    def generate(self):
        rand = random.randint(0, 15)
        while self.plansza[int(rand / self.size)][rand % self.size] != -1:
            rand = random.randint(0, self.size * self.size - 1)
        self.plansza[int(rand / self.size)][rand % self.size] = 1 if random.randint(0, 9) != 0 else 2

    def isNotFull(self):
        return any([any([x == -1 for x in el]) for el in self.plansza])

    def highestTile(self):
        return 2 ** np.amax(self.plansza)
    def print(self):
        for el in self.plansza:
            print([int(pow(2, x)) for x in el])

    def move(self, movement):
        moved = True
        points = 0
        if movement == 2 and self.plansza != self.nextLeft:
            self.plansza = self.nextLeft
            points = self.leftPoints
            self.clearPoints()
            # print("lewo")
        elif movement == 3 and self.plansza != self.nextRight:
            # print("Prawo")
            self.plansza = self.nextRight
            points = self.rightPoints
            self.clearPoints()
        elif movement == 0 and self.plansza != self.nextUp:
            self.plansza = self.nextUp
            points = self.upPoints
            self.clearPoints()
        elif movement == 1 and self.plansza != self.nextDown:
            self.plansza = self.nextDown
            points = self.downPoints
            self.clearPoints()
        else:
            moved = False
        return moved, points

    def clearPoints(self):
        self.leftPoints = 0
        self.rightPoints = 0
        self.upPoints = 0
        self.downPoints = 0

    def hasNext(self):
        self.nextLeft = np.array([self.right(x, "down") for x in np.array(self.plansza).T.tolist()]).T.tolist()
        self.nextRight = np.array([self.left(x, "up") for x in np.array(self.plansza).T.tolist()]).T.tolist()
        self.nextUp = [self.right(x) for x in self.plansza]
        self.nextDown = [self.left(x) for x in self.plansza]

        if any([self.plansza != possible_move for possible_move in
                [self.nextLeft, self.nextRight, self.nextUp, self.nextDown]]):
            return True

        return False

    def left(self, x, direction="left"):
        result = [number for number in x if number != -1]
        while len(result) != len(x):
            result.insert(0, -1)
        for i in range(len(x) - 1)[::-1]:
            if result[i] == result[i + 1] and result[i] != -1:
                result[i + 1] += 1
                if direction == "down":
                    self.downPoints += pow(2, result[i + 1])
                else:
                    self.rightPoints += pow(2, result[i + 1])

                for j in range(1, i + 1)[::-1]:
                    result[j] = result[j - 1]
                result[0] = -1
        return result

    def right(self, x, direction="right"):
        result = [number for number in x if number != -1]
        while len(result) != len(x):
            result.append(-1)
        # print(result)
        for i in range(len(x) - 1):
            if result[i] == result[i + 1] and result[i] != -1:
                result[i] += 1
                if direction == "up":
                    self.upPoints += pow(2, result[i])
                else:
                    self.leftPoints += pow(2, result[i])
                for j in range(i + 1, len(x) - 1):
                    result[j] = result[j + 1]
                result[-1] = -1

        return result

    @staticmethod
    def up(x):
        return x

    @staticmethod
    def down(x):
        return x
