from model.MiniMax import *

class MonoHeurGenerator:

    @staticmethod
    def generateNext(game: Gra, type="corner", exponential_parameter=4, weights=None, depth=4, branching_factor=6):
        def monoheuristic(table):
            if type == "corner" or type != "corner":
                weights_tables = []
                aux = [[exponential_parameter ** (i + j) for i in range(game.size)] for j in
                       range(game.size)]
                weights_tables.append(copy.deepcopy(aux))
                [l.reverse() for l in aux]
                weights_tables.append(copy.deepcopy(aux))
                aux.reverse()
                weights_tables.append(copy.deepcopy(aux))
                [l.reverse() for l in aux]
                weights_tables.append(copy.deepcopy(aux))

            table_aux = [[int(2 ** (j)) for j in i] for i in table]
            if table == game.table.plansza:
                return 0
            score = 0
            for weights_table in weights_tables:
                score = max(score,
                            sum(sum([a * b for (a, b) in zip(i, j)]) for (i, j) in zip(table_aux, weights_table)))
            return score

        game.table.hasNext()

        root_node = copy.deepcopy(game)
        search_tree = MiniMax(game, heuristic=monoheuristic, branching_factor=branching_factor, search_depth=depth)
        best_move = search_tree.search()

        return best_move
