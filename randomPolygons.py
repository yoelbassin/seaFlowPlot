import numpy as np
from numpy import random
import matplotlib.pyplot as plt
from opensimplex import OpenSimplex
from _3dPolygon import polygon3d
import random

def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


colors = [ '#005f73', '#0a9396', '#94d2bd', '#e9d8a6', '#ee9b00', '#ca6702',
            '#bb3e03', '#ae2012', '#9b2226']

tmp = OpenSimplex(seed=3)

coords = []

#seed 6
a = int(np.random.random()*100000)
# a = 71547, 25865 # for later debugging left triangle
# a = 92554 # has a weired polygon
# a = 26602
# a = 8785, 23084 # very interesting seed
random.seed(a)
np.random.seed(a)

fig= plt.figure(figsize = (20, 10))
ax = fig.add_subplot(111)

shapes = []

distorted = []

def make_rand_vector(dims):
    vec = [random.gauss(0, 1) for i in range(dims)]
    mag = sum(x**2 for x in vec) ** .5
    return [x/mag for x in vec]


shapes = []
points = np.random.multivariate_normal([50, 50], 30*np.array([[1,0],[0,1]]), 100)
for point in points:
    pgon = polygon3d(point[0], point[1],
        np.random.randint(5,10), np.random.random(),
        np.random.random(), np.random.randint(3, 10), make_rand_vector(2), 1 + random.random() * 4)
    shapes.append(pgon)

shapes.sort(key=lambda p: p.radius)

shapes.reverse()

for shp in shapes:
    distorted = shp.distort(tmp, 0, 100000, 0.01, 0.03, 0.03)
    pgons = shp.polygon(distorted)

    for pgon in pgons:

        x, y = pgon.exterior.xy

        # ax.plot(x, y, color='#6699cc', alpha=0.7,
        #     linewidth=1)

        plt.fill(x, y, facecolor=np.random.choice(colors), edgecolor='black', linewidth=0.4, alpha=1 - (random.random() > 0.7)*random.random())

ax.set_aspect('equal')
ax.set_facecolor("#335c67")

print('seed:', a)

plt.show()
