import random
from gra import Gra
from monteCarloGenerator import MonteCarloGenerator

SEED = random.randint(0, 500)
random.seed(SEED)

nowaGra = Gra(4)
nowaGra.print()

randoms = [random.randint(0, 3) for x in range(400)]
# i = 0
monteCarloSize = 100

while nowaGra.notOver():
    # time.sleep(1)
    # ruch = randint(0, 3)
    # print("Wylosowano: ", str(ruch))
    # moved = nowaGra.move(randoms[i])
    # nextMove = MonteCarloGenerator.generateNext(nowaGra, monteCarloSize)
    # print(nextMove)
    moved = nowaGra.move(MonteCarloGenerator.generateNext(nowaGra, monteCarloSize))
    # moved = nowaGra.move(random.randint(0, 3))
    # i += 1
    # if moved:
        # nowaGra.print()

    print("Moves= ", nowaGra.moves)

nowaGra.print()
print("Game over, wykonano {} ruchów. Zdobyto {} punktów".format(nowaGra.moves, nowaGra.score))
