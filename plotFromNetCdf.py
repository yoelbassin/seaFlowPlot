from numpy.random.mtrand import random
from streamplot import *
from scipy.interpolate import make_interp_spline, BSpline
from scipy import interpolate

from pathlib import Path
import netCDF4 as nc
import numpy as np
import math

pathlist = Path().rglob('*.nc')
for path in pathlist:
    print(path)
    _file = str(path)
    try:
        ncfile.close()
    except:
        pass
    ncfile = nc.Dataset(_file, mode='a')
    lon = ncfile['longitude'][:]
    lat = ncfile['latitude'][:]
    depth = ncfile['depth'][:]
    time = ncfile['time'][:]
    u = np.array(ncfile['uo'][:])
    v = ncfile['vo'][:]

colors = ['#001219', '#005f73', '#0a9396', '#94d2bd', '#e9d8a6', '#ee9b00', '#ca6702',
            '#bb3e03', '#ae2012', '#9b2226']

colors = ["#f1faee","#a8dadc","#457b9d","#1d3557"]

colors = ["#fff3b0","#e09f3e","#9e2a2b","#540b0e"]


import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap


import matplotlib.pyplot as plt
# creating plot
lon_ = np.linspace(lon.min(), lon.max(), len(lon))
lat_ = np.linspace(lat.min(), lat.max(), len(lat))
fig, ax = plt.subplots(figsize =(100, 100))
# ax.quiver(lon, lat, u[0][0], v[0][0])
# for i, ln in enumerate(lon_):
#     for j, lt in enumerate(lat_):
#         # if ln%1==0 and lt%1==0:
#         if i%5==0 and j%5==0:
#             ax.streamplot(lon_, lat_ , u[0][0], v[0][0], start_points=[(ln, lt)], linewidth=20, arrowstyle='-', color=np.random.choice(colors))
trajectories = streamplot(ax, lon_, lat_ , u[0][0], v[0][0], arrowstyle='-', density=5)
# for i, ln in enumerate(lon_):
#     for j, lt in enumerate(lat_):        
#         if not i%3==0 or not j%3==0:
#             continue
#         trajectories = streamplot(ax, lon_, lat_ , u[0][0], v[0][0], start_points=[(ln, lt)], arrowstyle='-')
width = np.random.normal(25, 5, len(trajectories))
for i, val in enumerate(width):
    if val < 16:
        width[i] = np.random.randint(5, 10)
    if val > 20:
        width[i] = np.random.randint(25,30)

for num, t in enumerate(trajectories):
    q = []
    for i in range(0,len(t)):
        if i == 0:
            q.append(list(t[i]))
        else:
            if list(t[i]) == list(t[i-1]):
                continue
            else:
                q.append(list(t[i]))
    q = np.array(q)
    x_values = q[:, 0]
    y_values = q[:, 1]

    tck, u_ = interpolate.splprep([x_values, y_values], s=0)

    
    unew = np.arange(0, 1.01, 0.001)
    out = interpolate.splev(unew, tck)


    plt.plot(out[0], out[1], color=np.random.choice(colors), linewidth=int(width[num]))
    

# ax.axis( [33.5, 35, 31, 34])
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])
ax.set_facecolor("#335c67")
ax.set_aspect('equal')
 
# show plot
plt.savefig("plot13.svg")