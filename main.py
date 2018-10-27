import time

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anim

from IPython import get_ipython
get_ipython().magic('%matplotlib')

plt.style.use('fivethirtyeight')

threshold = 1
x_dim = 50
y_dim = 50

def next_generation(world):
    "returns next generation of world"
    counts = dict()
    for cell in world.keys():
        adj_colors = [key for key in neighbors(world,cell) if not world[key][0] < 1]
        counts[cell] = (1 if (sum([world[key][0] for key in neighbors(world, cell)]) in [2,3]) else 0,
                        np.mean([world[key][1] for key in adj_colors]),
                        np.mean([world[key][2] for key in adj_colors]),
                        np.mean([world[key][3] for key in adj_colors]))
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
    living = [k for k,v in world.items() if not (v[0] < threshold)]
    colors = [v[1:] for k,v in world.items() if not (v[0] < threshold)]
    ax.scatter([x for x in map(lambda a: a[0], living)],
               [y for y in map(lambda a: a[1], living)], c=colors)
    ax.set_xticks(np.arange(-0.5,x_dim+0.5))
    ax.set_yticks(np.arange(-0.5,y_dim+0.5))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)
    plt.show()

def updater(i):
    living = [k for k,v in generations[i].items() if not (v[0] < threshold)]
    colors = [v[1:]+(1,) for k,v in generations[i].items() if not (v[0] < threshold)]
    scat.set_offsets(living)
    scat.set_color(colors)


fig, ax = plt.subplots(figsize=(10,10))
ax.set_xlim(-1,51)
ax.set_ylim(-1,51)
ax.set_xticks(np.arange(-0.5,x_dim+0.5))
ax.set_yticks(np.arange(-0.5,y_dim+0.5))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.grid(True)

world = {key:(0, 0., 0., 0.) for key in ((x,y) for x in range(x_dim) for y in range(y_dim))}
world[(5,5)] = (1, 0.1, 0., 0.8)
world[(6,5)] = (1, 0.2, 0., 0.8)
world[(7,5)] = (1, 0.1, 0., 0.8)
world[(11,8)] = (1, 0.3, 0.8, 0.)
world[(11,9)] = (1, 0.1, 0.8, 0.)
world[(21,20)] = (1, 0.8, 0., 0.)
world[(21,22)] = (1, 0.8, 0., 0.1)
world[(41,40)] = (1, 0., 0.8, 0.)
world[(41,42)] = (1, 0.8, 0.2, 0.)
world[(42,43)] = (1, 0.8, 0., 0.8)
world[(42,44)] = (1, 0., 0.8, 0.)

num_frames = 50
living = [k for k,v in world.items() if not (v[0] < threshold)]

scat = ax.scatter([x for x in map(lambda a: a[0], living)],
                  [y for y in map(lambda a: a[1], living)])

print(scat.get_edgecolor())
generations = [world]
for i in range(num_frames):
    generations.append(next_generation(generations[i]))

ani = anim.FuncAnimation(fig, updater, interval=200, frames=range(num_frames))
plt.show()

# fig, ax = plt.subplots(figsize=(10,10))
# ax.set_xlim(-1,51)
# ax.set_ylim(-1,51)
# ax.set_xticks(np.arange(-0.5,x_dim+0.5))
# ax.set_yticks(np.arange(-0.5,y_dim+0.5))
# ax.set_xticklabels([])
# ax.set_yticklabels([])
# ax.grid(True)
# 
# world = {key:(0, 0, 0, 0) for key in ((x,y) for x in range(x_dim) for y in range(y_dim))}
# 
# world[(5,5)] = (1, 0, 0, 255)
# world[(6,5)] = (1, 0, 0, 255)
# world[(7,5)] = (1, 0, 0, 255)
# world[(11,8)] = (1, 0, 255, 0)
# world[(11,9)] = (1, 0, 255, 0)
# world[(21,20)] = (1, 255, 0, 0)
# world[(21,22)] = (1, 255, 0, 0)
# world[(41,40)] = (1, 255, 0, 0)
# world[(41,42)] = (1, 255, 0, 0)
# world[(42,43)] = (1, 255, 0, 0)
# world[(42,44)] = (1, 255, 0, 0)
# 
# 
# num_frames = 25
# living = [k for k,v in world.items() if not (v[0] < threshold)]
# 
# scat = ax.scatter([x for x in map(lambda a: a[0], living)],
#                   [y for y in map(lambda a: a[1], living)])
# 
# generations = [world]
# for i in range(num_frames):
#     generations.append(next_generation(generations[i]))
# 
# 
# ani = anim.FuncAnimation(fig, updater, interval=200, frames=range(num_frames))
# plt.show()
