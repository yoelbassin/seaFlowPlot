import numpy as np
import matplotlib.pylab as pl
from matplotlib.patches import Polygon
from scipy.optimize import fmin

colors = ['#001219', '#005f73', '#0a9396', '#94d2bd', '#e9d8a6', '#ee9b00', '#ca6702',
            '#bb3e03', '#ae2012', '#9b2226']

def orthogonal_line(x1, x2, y1, y2):
    m = (y2 - y1) / (x2 - x1)
    per_m = - 1 / m
    def f(x):
        return per_m*(x - x1) + y1
    return f

def find_intersector(f1, f2):
    return np.argwhere(np.diff(np.sign(f1 - f2))).flatten()

def create_polygon(a, b, res, f1, f2, color, alpha):
    ix = np.linspace(a, b, res)
    iy = f1(ix)
    f_2 = f2(ix)
    f_start = orthogonal_line(ix[0], ix[1], iy[0], iy[1])(ix)
    f_end = orthogonal_line(ix[-1], ix[-2], iy[-1], iy[-2])(ix)
    a = find_intersector(f_start, f_2)
    b = find_intersector(f_end, f_2)
    print(a, b)
    ix2 = np.linspace(a, b, res)
    
    verts = [(a, f2(a))] + list(zip(ix, iy)) + [(b, f2(b))] + list(reversed(list(zip(ix2, f2(ix2)))))
    return Polygon(verts, color=color, alpha=alpha)

def draw(f):

    x = np.linspace(-10, 10, 10000)
    y = f(x)

    xmin, xmax, ymin, ymax = -10, 10, -5, 5

    # Plot x and y.
    fig, ax = pl.subplots()
    pl.plot(x, y, 'b', linewidth = 1)
    pl.xlim(xmin = xmin, xmax = xmax)
    pl.ylim(ymin = ymin, ymax = ymax)

    min_y = -10

    y_plt = min_y

    pgons = []

    def f_c(x):
        return f(x) + min_y

    while y_plt <= 20:
        depth = np.random.randint(1,6)
        def f2(x):
            return f_c(x) + depth
        x_plt = xmin
        while x_plt <= xmax:
            length = np.random.randint(1,6)
            poly = create_polygon(x_plt, x_plt+length, 10000, f_c, f2,
            np.random.choice(colors), alpha=np.random.randint(6,10)/10)
            x_plt += length
            ax.add_patch(poly)
        def f_c(x):
            return f(x) + min_y + depth
        y_plt += depth

    pl.figtext(0.9, 0.05, '$x$')
    pl.figtext(0.1, 0.9, '$y$')

    ax.set_xticks([])
    ax.set_yticks([])

    # Show the plot.
    pl.show()