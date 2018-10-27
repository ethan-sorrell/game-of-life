import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from IPython import get_ipython
get_ipython().magic('%matplotlib')

threshold = 1


def next_generation(world):
    "return a series for livelihood of next generation"
    counts = neighbor_counts(world)
    livelihood =  counts.apply(lambda x: 1 if (x == 2 or x == 3) else 0)
    new_world = world.copy()
    new_world['health'] = livelihood
    return new_world


def neighbor_counts(world):
    "return a series of neighbor counts from world"
    counts = dict()
    for index in world.index:
        counts[index] = live(neighbors(world, index)).sum()
    return pd.Series(counts)

def neighbors(world, index):
    "takes a cell index and a world dataframe and returns # neighbors for that cell"
    cell = world.ix[index]
    xs = [cell['x']+i for i in [-1, 0, 1]]
    ys = [cell['y']+i for i in [-1, 0, 1]]
    possible_neighbors = world.query('(x in @xs) & (y in @ys)')
    return possible_neighbors

def live(world):
    "returns a series of livelihood of cells in world"
    livelihood = dict()
    for index in world.index:
        livelihood[index] = 0 if world.ix[index]['health'] < threshold else 1
    return pd.Series(livelihood)

def display(world):
    "display world as plot with points at locations of living cells"
    living_ixs = live(world)
    living_ixs = living_ixs[~(living_ixs < threshold)].index
    living = world.ix[living_ixs]
    fig, ax = plt.subplots(figsize=(10,10))
    ax.scatter(living['x'], living['y'])
    ax.set_xticks(np.arange(-0.5,50.5))
    ax.set_yticks(np.arange(-0.5,50.5))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)
    plt.show()

def main():
    world = pd.DataFrame(data={'x' : [x for x in range(50) for _ in range(50)],
                               'y' : [y for _ in range(50) for y in range(50)],
                               'health' : [np.random.binomial(1,0.5)
                                           for _ in range(50) for _ in range(50)]})
    display(world)
    a_time = time.time()
    world2 = next_generation(world)
    print('time to generate new world: {}'.format(time.time() - a_time))
    display(world2)
    print('time to generate new world: {}')



if __name__ == '__main__':
    main()


# for repl testing purposes
main()



