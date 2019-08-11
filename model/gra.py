from model.board import Board


class Gra:
    def __init__(self, size=4, seed=None, tablica: Board = None):
        self.size = size
        self.seed = seed
        if tablica is None:
            self.table = self.initialise()
        else:
            self.table = tablica
        self.moves = 0
        self.score = 0
        self.search_depth = 0
        self.next_move = None
        self.next_move_value = 0

    def initialise(self):
        if self.seed:
            return Board(self.size)
        else:
            return Board(self.size)

    def print(self):
        self.table.print()
        print()

    def setNextMove(self, k):
        self.next_move = k
        return self

    def increment_depth(self):
        self.search_depth = self.search_depth + 1
        return self

    def highestTile(self):
        return self.table.highestTile()

    def move(self, movement: int):
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

    def can_move(self, move):
        self.table.hasNext()
        if move == 0:
            return self.table.values != self.table.nextUp
        if move == 1:
            return self.table.values != self.table.nextDown
        if move == 2:
            return self.table.values != self.table.nextLeft
        if move == 3:
            return self.table.values != self.table.nextRight

    def notOver(self):
        return self.table.hasNext()