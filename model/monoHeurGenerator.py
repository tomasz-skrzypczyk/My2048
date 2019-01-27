from typing import List

import numpy as np


class MonoHeurGenerator:

    @staticmethod
    def generateNext(gameController, type="corner", exponential_parameter=2, weights=None):
        def monoheuristic(table, weights_table):
            table_aux = [[int(2 ** (j)) for j in i] for i in table]
            if table == gameController.game.table:
                return 0
            return sum(sum([a * b for (a, b) in zip(i, j)]) for (i, j) in zip(table_aux, weights_table))

        movesScore: List[int] = [0, 0, 0, 0]
        gameController.game.table.hasNext()
        TODO: "opisy"

        # wygeneruj wszystkie tablice:
        if type == "corner" or type != "corner":
            weights_tables = []
            aux = [[exponential_parameter ** (i + j) for i in range(gameController.game.size)] for j in
                   range(gameController.game.size)]
            weights_tables.append(aux)
            weights_tables.append([l.reverse() for l in aux])
            weights_tables.append(aux.reverse())
            weights_tables.append([l.reverse() for l in aux])

        # dla kazdej kombinacji:
        for weights_table in weights_tables:
            movesScore[0] = max(monoheuristic(gameController.game.table.nextUp, weights_table), movesScore[0])
            movesScore[1] = max(monoheuristic(gameController.game.table.nextDown, weights_table), movesScore[1])
            movesScore[2] = max(monoheuristic(gameController.game.table.nextLeft, weights_table), movesScore[2])
            movesScore[3] = max(monoheuristic(gameController.game.table.nextRight, weights_table), movesScore[3])
            break

        return np.random.choice(np.flatnonzero(movesScore == np.array(movesScore).max()))
