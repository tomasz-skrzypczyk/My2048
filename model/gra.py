from model.tablica import Tablica


class Gra:
    def __init__(self, size=4, seed=None, tablica=None):
        self.size = size
        self.seed = seed
        if tablica is None:
            self.table = self.initialise()
        else:
            self.table = tablica
        self.moves = 0
        self.score = 0

    def initialise(self):
        if self.seed:
            return Tablica(self.size)
        else:
            return Tablica(self.size)

    def print(self):
        self.table.print()
        print()

    def highestTile(self):
        return self.table.highestTile()

    def move(self, movement):
        moved, points = self.table.move(movement)
        self.score += points
        # print("Ruch wykonano")
        if self.table.isNotFull() and moved:

            self.table.generate()
        else:
            # print("Tablica jest pełna")
            pass
        if moved:
            self.moves += 1
        return moved


    def notOver(self):
        return self.table.hasNext()