import numpy as np
from shapely.geometry.polygon import Polygon
import math
import random

def generatePolygon( ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts ) :
    '''Start with the centre of the polygon at ctrX, ctrY, 
    then creates the polygon by sampling points on a circle around the centre. 
    Randon noise is added by varying the angular spacing between sequential points,
    and by varying the radial distance of each point from the centre.

    Params:
    ctrX, ctrY - coordinates of the "centre" of the polygon
    aveRadius - in px, the average radius of this polygon, this roughly controls how large the polygon is, really only useful for order of magnitude.
    irregularity - [0,1] indicating how much variance there is in the angular spacing of vertices. [0,1] will map to [0, 2pi/numberOfVerts]
    spikeyness - [0,1] indicating how much variance there is in each vertex from the circle of radius aveRadius. [0,1] will map to [0, aveRadius]
    numVerts - self-explanatory

    Returns a list of vertices, in CCW order.
    '''

    irregularity = clip( irregularity, 0,1 ) * 2*math.pi / numVerts
    spikeyness = clip( spikeyness, 0,1 ) * aveRadius

    # generate n angle steps
    angleSteps = []
    lower = (2*math.pi / numVerts) - irregularity
    upper = (2*math.pi / numVerts) + irregularity
    sum = 0
    for i in range(numVerts) :
        tmp = random.uniform(lower, upper)
        angleSteps.append( tmp )
        sum = sum + tmp

    # normalize the steps so that point 0 and point n+1 are the same
    k = sum / (2*math.pi)
    for i in range(numVerts) :
        angleSteps[i] = angleSteps[i] / k

    # now generate the points
    points = []
    angle = random.uniform(0, 2*math.pi)
    for i in range(numVerts) :
        r_i = clip( random.gauss(aveRadius, spikeyness), 0, 2*aveRadius )
        x = ctrX + r_i*math.cos(angle)
        y = ctrY + r_i*math.sin(angle)
        points.append( (int(x),int(y)) )

        angle = angle + angleSteps[i]

    return points

def clip(x, min, max) :
    if( min > max ) :  return x    
    elif( x < min ) :  return min
    elif( x > max ) :  return max
    else :             return x

class polygon3d:
    def __init__(self, ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts, dir_vec, depth):
        self.top = generatePolygon( ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts )
        self.edge_num = len(self.top)
        self.dir_vec = dir_vec
        self.depth = depth
        self.sides = []
        self.base = self.create3d()
        self.radius = aveRadius

        for coords_index in range(-1, self.edge_num -1):
            side = []
            side = [self.top[coords_index],
                        self.top[coords_index+1],
                        self.base[coords_index+1],
                        self.base[coords_index]]
            self.sides += [side]

    def distort(self,tmp,  x_off, y_off, step, x_mag, y_mag):     
        distorted = []

        cur_step = 0

        shapes = [self.top] + self.sides + [self.base]

        edge_dict = {}

        for shp in shapes:
            new_dis = []
            for num in range(-1, len(shp) - 1):
                this_dis = []
                key = (shp[num], shp[num+1]) 
                key_r = (shp[num+1], shp[num])
                if key in edge_dict.keys():
                    new_dis += edge_dict[key]
                    continue
                elif key_r in edge_dict.keys():
                    new_dis += list(reversed(edge_dict[key_r]))
                    continue
                x_ = np.linspace(shp[num][0], shp[num+1][0], 1000)
                y_ = np.linspace(shp[num][1], shp[num+1][1], 1000)
                for k in range(len(x_)):
                    x2 = x_[k] + tmp.noise2d(x_off+cur_step, 1) * x_mag
                    y2 = y_[k] + tmp.noise2d(y_off+cur_step, 1) * y_mag
                    this_dis.append((x2, y2))
                    cur_step += step
                edge_dict[key] = this_dis
                new_dis += this_dis
            distorted.append(new_dis)
        return distorted

    def create3d(self):
        x_vec, y_vec = self.dir_vec
        z = self.depth
        projection = [(c[0]-x_vec*z, c[1]-y_vec*z) for c in self.top]
        return projection

    def polygon(self, data=None):
        if data is None:
            data = [self.top] + self.sides + [self.base]
        polygons = []
        for pgon in data:
            polygons.append(Polygon(pgon))
        return polygons




