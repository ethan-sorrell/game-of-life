import matplotlib.pyplot as plt
import numpy as np
import time
from IPython import get_ipython
get_ipython().magic('%matplotlib')

threshold = 1
x_dim = 50
y_dim = 50


def next_generation(world):
    "return a series for livelihood of next generation"
    atime = time.time()
    counts = neighbor_counts(world)
    print('time to find neighbor counts: {}'.format(time.time() - atime))
    new_world = {k:z for k,v in counts.items() for z in [1 if (v == 2 or v == 3) else 0]}
    return new_world

def neighbor_counts(world):
    "return a dict of neighbor counts for each cell in world"
    counts = dict()
    for cell in world.keys():
        counts[cell] = sum([world[key] for key in neighbors(world, cell)])
    return counts

def neighbors(world, cell):
    "return list of positions of all possible neighbors of cell"
    xs = [cell[0]+i for i in [-1, 0, 1]]
    ys = [cell[1]+i for i in [-1, 0, 1]]
    possible_neighbors = ((x,y) for x in xs for y in ys
                          if 0 <= x < 50 and 0 <= y < 50)
    return possible_neighbors

def live(world):
    "returns a series of livelihood of cells in world"
    livelihood = dict()
    for index in world.index:
        livelihood[index] = 0 if world.ix[index]['health'] < threshold else 1
    return pd.Series(livelihood)

def display(world):
    "display world as plot with points at locations of living cells"
    fig, ax = plt.subplots(figsize=(10,10))
    living = [k for k,v in world.items() if not (v < threshold)]
    ax.scatter([x for x in map(lambda a: a[0], living)],
               [y for y in map(lambda a: a[1], living)])
    ax.set_xticks(np.arange(-0.5,50.5))
    ax.set_yticks(np.arange(-0.5,50.5))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)
    plt.show()

def main():
    world = {key:value for key in ((x,y) for x in range(x_dim) for y in range(y_dim))
                       for value in np.random.randint(0, 2, x_dim*y_dim)}
    display(world)
    a_time = time.time()
    world2 = next_generation(world)
    print('time to generate new world: {}'.format(time.time() - a_time))
    display(world2)



if __name__ == '__main__':
    main()


# for repl testing purposes
main()



