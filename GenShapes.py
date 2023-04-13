from Engine import *
import random
import math
from numpy import pi, cos, sin, arccos, arange

def genSphere(Radius, lod):
    print("New Sphere! Radius: " + str(Radius))
    
    trianglelist = []
    veclist = []

    indices = arange(0,lod, dtype=float)
    phi = arccos(1 -2 * indices/lod)
    theta = pi * (1 + 5 ** 0.5) * indices

    x, y, z = cos(theta) * sin(phi) *Radius, sin(theta) * sin(phi) *Radius, (cos(phi) *Radius) +1;

    for i in range(lod):
        veclist.append(TriVec3d(x[i],y[i],z[i]))

    for j in range(int(lod/3)):
        trianglelist.append(Triangle3d([veclist[j*3],veclist[j*3 + 1], veclist[j*3 + 2]]))

    Generatedmesh = Mesh3d(trianglelist)
    Genobject = Object3d(Generatedmesh)
    return Genobject



