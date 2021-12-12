from numpy.random.mtrand import rand, random
from opensimplex import OpenSimplex
import matplotlib.pyplot as plt
import numpy as np

tmp = OpenSimplex(seed=np.random.randint(0,1000000))

dots = []



colors = [ '#005f73', '#0a9396', '#94d2bd', '#e9d8a6', '#ee9b00', '#ca6702',
            '#bb3e03', '#ae2012', '#9b2226']

# colors = ["#fff3b0","#e09f3e","#9e2a2b","#540b0e"]


fig, ax = plt.subplots(figsize=(10, 10))

cur_row_step = 0
cur_col_step = 0
row_step = np.random.random() / 1000
col_step = np.random.random() / 1000
mag = np.random.random()

for j in range(40):
    col_step += np.random.random() / 100000
    row_step += np.random.random() / 100000
    for i in range(60):
        # if 50 >= i >= 10:
        #     pass
        # elif i > 45:
        #     i_temp = 60-i
        # else:
        #     i_temp = i
        if i > 30:
            i_temp = 60 - i
        else:
            i_temp = i
        x = j
        y = i + tmp.noise2d(cur_row_step, cur_col_step) * i_temp / ( 1 + mag)
        plt.plot(x, y, 'o', color=colors[(i) % len(colors)])
        cur_row_step += row_step
        cur_col_step += col_step
        
        

ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])
# ax.set_facecolor("#335c67")
ax.set_facecolor('#f8f8f8')
ax.set_aspect('equal')
 
# show plot
plt.show()