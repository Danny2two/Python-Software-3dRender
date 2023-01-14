import math
import arcade
import numpy
from numba import jit
from copy import copy

SW = 1000
SH = 800
AspectR = (SH/SW)
FoVdeg = 90
TransMatrix = []
wireframe = False

'''
Writen by: Daniel Mitchell

Adapted from video series by javidk9 on Youtube

'''


class TriVec3d(): #Baisc Vector class
    def __init__(self,x,y,z):
        self.ox =x
        self.oy =y
        self.oz =z
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str((str(self.x), str(self.y), str(self.z)))


class Triangle3d(): #basic triangle class, holds 3 vectors
    def __init__(self, Vectors: list[TriVec3d]):
        self.vects = Vectors
        self.aveZ = 0
        self.color = [0,0,0]

    def getaveZ(self): #get the average z value of the vetors
        self.aveZ = ((self.vects[0].z + self.vects[1].z + self.vects[2].z)/3)

    def scale(self, dScale):
        for i in self.vects:
            i.x = i.ox* dScale
            i.y = i.oy* dScale
            i.z = i.oz* dScale




class Mesh3d(): #basic mesh class, hold all of the triangles 
    def __init__(self, listoftriangles: list[Triangle3d]):
        self.triangles = []
        count = 0
        for i in listoftriangles:
            count += 1
            self.triangles.append( i)
        print( "Made a mesh with " + str(count) + " triangles")

class Object3d():
    def __init__(self, mesh):
        self.colorRGB = [255,50,20]
        self.lightvector = TriVec3d(1,-1,-1) #direction light comes from 
        self.ambientlight = [75,50,50] # Ambient light in the environmenmt shines on all faces
        self.mesh = mesh
        self.trans = []
        self.ztheta = 0
        self.xtheta = 0
        self.dxtheta = 0
        self.dztheta = 0
        self.zoffset = 4
        self.mscale = 1

        self.vcam = TriVec3d(0,0,0)

        # projectionmatrix
        Fnear = 0.1
        FFar = 1000
        FFov = 120
        FAspectratio = AspectR
        FFovRad = 1 / (math.tan((FFov  / (180 * 3.14159))/2))

        mat4x4 = [[0, 0, 0, 0], #matrix for transformations in 3d space
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
        
        mat4x4[0][0] = FAspectratio * FFovRad
        mat4x4[1][1] = FFovRad
        mat4x4[2][2] = FFar / (FFar - Fnear)
        mat4x4[3][2] = (-FFar * Fnear) / FFar - Fnear
        mat4x4[2][3] = 1
        mat4x4[3][3] = 0
        self.trans = mat4x4
        print("Transformation matrix made")
        for i in self.trans:
            print(i)


        fTheta = self.ztheta
        matrotz = [[0, 0, 0, 0], #setting up a transformation matrix for rotation in the z axis
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

        matrotz[0][0] = math.cos(fTheta)
        matrotz[0][1] = math.sin(fTheta)
        matrotz[1][0] = -math.sin(fTheta)
        matrotz[1][1] = math.cos(fTheta)
        matrotz[2][2] = 1
        matrotz[3][3] = 1
        self.rotz = matrotz

        matrotx = [[0, 0, 0, 0], #setting up a transformation matrix for rotation in the x axis
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

        matrotx[0][0] = 1
        matrotx[1][1] = math.cos(self.ztheta)
        matrotx[1][2] = math.sin(self.ztheta)
        matrotx[2][1] = -math.sin(self.ztheta)
        matrotx[2][2] = math.cos(self.ztheta)
        matrotx[3][3] = 1
        self.rotx = matrotx

        

   
    def on_draw(self, mesh: Mesh3d):
        transformedtriangles = []
        for i in mesh.triangles: #Transform triangles indevidualy
            
            tempvec0 = copy(i.vects[0])
            tempvec1 = copy(i.vects[1])
            tempvec2 = copy(i.vects[2])

            rotvec0 = multiplymatrixvector(tempvec0, self.rotz)
            rotvec1 = multiplymatrixvector(tempvec1, self.rotz)
            rotvec2 = multiplymatrixvector(tempvec2, self.rotz)

            nrotvec0 = multiplymatrixvector(rotvec0, self.rotx)
            nrotvec1 = multiplymatrixvector(rotvec1, self.rotx)
            nrotvec2 = multiplymatrixvector(rotvec2, self.rotx)

            normal = calcnormal(Triangle3d([nrotvec0,nrotvec1,nrotvec2])) #find the normal of the triangle as is for lighing 
            tlightvector = self.lightvector # get light vector
            lightnormallen = math.sqrt(tlightvector.x*tlightvector.x + tlightvector.y*tlightvector.y + tlightvector.z*tlightvector.z) 
            tlightvector.x /= lightnormallen 
            tlightvector.y /= lightnormallen
            tlightvector.z /= lightnormallen # make light vector a unit vector 
            dotprod = normal.x * tlightvector.x + normal.y * tlightvector.y + normal.z * tlightvector.z #dontproduct to see how much light hits face
            mcolor = getshade(dotprod,self.colorRGB,self.ambientlight) #find the color resulting from the light 

            nrotvec0.z += self.zoffset #offset the face into the screen, trick to avoid math for cameras, for now
            nrotvec1.z += self.zoffset
            nrotvec2.z += self.zoffset

            if nrotvec0.z > 0 and nrotvec1.z > 0 and nrotvec2.z > 0:

                transvec0 = multiplymatrixvector(nrotvec0, self.trans) #Translate triangle from 3d to 2d(pixels)
                transvec1 = multiplymatrixvector(nrotvec1, self.trans)
                transvec2 = multiplymatrixvector(nrotvec2, self.trans)

                transtriangle = Triangle3d([transvec0,transvec1,transvec2]) #reassemble triangle
                normal = calcnormal(transtriangle) #find normal

                
                if transvec0.z >=0 and transvec1.z >=0 and transvec2.z >=0 and ((normal.x * (transtriangle.vects[0].x - self.vcam.x) + normal.y * (transtriangle.vects[0].y -self.vcam.y) + normal.z * (transtriangle.vects[0].z - self.vcam.z)) < 0 ):
                    transvec0.x += 1 
                    transvec0.y += 1
                    transvec1.x += 1
                    transvec1.y += 1
                    transvec2.x += 1
                    transvec2.y += 1

                    transvec0.x *= 0.5 * SW #scale to screen size
                    transvec0.y *= 0.5 * SH
                    transvec1.x *= 0.5 * SW
                    transvec1.y *= 0.5 * SH
                    transvec2.x *= 0.5 * SW
                    transvec2.y *= 0.5 * SH 

                    newtransformedtriangle = Triangle3d([transvec0,transvec1,transvec2])
                    newtransformedtriangle.color = mcolor
                    transformedtriangles.append(newtransformedtriangle) #add valid triangles to the list of transformed triangles
                else:
                    pass
                    #print("toss")
                
        for tri in transformedtriangles: #update all of the average z for the triangles to rendered, sorth them from furthest to closest 
            tri.getaveZ()
        sortedmesh = sorted(transformedtriangles,key=lambda x: x.aveZ, reverse= True)
        

        for triangle in sortedmesh:
            
            transvec0 = triangle.vects[0]
            transvec1 = triangle.vects[1]
            transvec2 = triangle.vects[2]

            if wireframe: #Draw triangles 
                arcade.draw_triangle_outline(transvec0.x,transvec0.y,transvec1.x, transvec1.y,transvec2.x, transvec2.y,arcade.color.WHITE)
            else:
                arcade.draw_triangle_filled(transvec0.x,transvec0.y,transvec1.x, transvec1.y,transvec2.x, transvec2.y,triangle.color)
                #arcade.draw_triangle_outline(transvec0.x,transvec0.y,transvec1.x, transvec1.y,transvec2.x, transvec2.y,arcade.color.BLACK)
    
    def on_update(self):
        self.ztheta += self.dztheta
        self.xtheta += self.dxtheta
        self.rotz[0][0] = math.cos(self.ztheta)
        self.rotz[0][1] = math.sin(self.ztheta)
        self.rotz[1][0] = -math.sin(self.ztheta)
        self.rotz[1][1] = math.cos(self.ztheta)

        self.rotx[1][1] = math.cos(self.xtheta)
        self.rotx[1][2] = math.sin(self.xtheta)
        self.rotx[2][1] = -math.sin(self.xtheta)
        self.rotx[2][2] = math.cos(self.xtheta)

    def translateupdateX(self, distance):
        for i in self.mesh.triangles:
            for p in i.vects:
                p.x += distance
                #print('CURRENT X: ' + str(p.x) + "Current y: " + str(p.y))
                
    def translateupdateY(self, distance):
        for i in self.mesh.triangles:
            for p in i.vects:
                p.y += distance

    def translateupdateZ(self, distance):
        for i in self.mesh.triangles:
            for p in i.vects:
                p.z += distance

    def scaleTriangles(self, DeltaScale):
        self.mscale += DeltaScale
        print(self.mscale)
        for i in self.mesh.triangles:
            i.scale(self.mscale)


def multiplymatrixvector( Vector: TriVec3d, TransMatrix: list[:]): #multply vectorss and matrix, simplified, only works for this aplication 
    #print(Vector)
    x = (Vector.x * TransMatrix[0][0]) + (Vector.y * TransMatrix[1][0]) + (Vector.z * TransMatrix[2][0]) + (TransMatrix[3][
        0])
    y = Vector.x * TransMatrix[0][1] + Vector.y * TransMatrix[1][1] + Vector.z * TransMatrix[2][1] + TransMatrix[3][
        1]
    z = Vector.x * TransMatrix[0][2] + Vector.y * TransMatrix[1][2] + Vector.z  * TransMatrix[2][2] + TransMatrix[3][
        2]
    w = Vector.x * TransMatrix[0][3] + Vector.y * TransMatrix[1][3] + Vector.z * TransMatrix[2][3] + TransMatrix[3][
        3]

    if w != 0:
        x = x / w
        y = y / w
        z = z / w
    return TriVec3d(x,y,z)#
    #return [x, y, z]

def calcnormal(triangle): # calcualte normal of a face
    line0x = triangle.vects[1].x - triangle.vects[0].x
    line0y = triangle.vects[1].y - triangle.vects[0].y
    line0z = triangle.vects[1].z - triangle.vects[0].z

    line1x = triangle.vects[2].x - triangle.vects[0].x
    line1y = triangle.vects[2].y - triangle.vects[0].y
    line1z = triangle.vects[2].z - triangle.vects[0].z

    normalx = line0y * line1z - line0z * line1y
    normaly = line0z * line1x - line0x * line1z
    normalz = line0x * line1y - line0y * line1x
    len = math.sqrt(normalx*normalx + normaly*normaly + normalz*normalz)
    normalx /= len
    normaly /= len
    normalz /= len
    return(TriVec3d(normalx,normaly,normalz))

def getshade(lum, color, ambientlight): #get shade of face based on "lumanance"
    max = 255
    c0 = color[0]
    c1 = color[1]
    c2 = color[2]

    if lum < 0:
        lum = 0

    c0 *= lum
    c1 *= lum
    c2 *= lum

    c0 += ambientlight[0]
    c1 += ambientlight[1]
    c2 += ambientlight[2]

    if c0 > color[0]:
        c0 = color[0]
    if c1 > color[1]:
        c1 = color[1]
    if c2 > color[2]:
        c2 = color[2]

    return[int(c0),int(c1),int(c2)]

def main(): #basic and broken test mesh
    TriangleT1 = Triangle3d((TriVec3d(0, 1, 0), TriVec3d(0, 1, 1), TriVec3d(1, 1, 1)))
    TriangleT2 = Triangle3d((TriVec3d(0, 1, 0), TriVec3d(1, 1, 1), TriVec3d(1, 1, 0)))

    TriangleS1 = Triangle3d((TriVec3d(0, 0, 0), TriVec3d(0, 1, 0), TriVec3d(1, 1, 0)))
    TriangleS2 = Triangle3d((TriVec3d(0, 0, 0), TriVec3d(1, 1, 0), TriVec3d(1, 0, 0)))

    TriangleE1 = Triangle3d((TriVec3d(1, 0, 0), TriVec3d(1, 1, 0), TriVec3d(1, 1, 1)))
    TriangleE2 = Triangle3d((TriVec3d(1, 0, 0), TriVec3d(1, 1, 1), TriVec3d(1, 0, 1)))

    TriangleN1 = Triangle3d((TriVec3d(1, 0, 1), TriVec3d(1, 1, 1), TriVec3d(0, 1, 1)))
    TriangleN2 = Triangle3d((TriVec3d(1, 0, 1), TriVec3d(0, 1, 1), TriVec3d(0, 0, 1)))

    TriangleW1 = Triangle3d((TriVec3d(0, 0, 1), TriVec3d(0, 1, 1), TriVec3d(0, 1, 0)))
    TriangleW2 = Triangle3d((TriVec3d(0, 0, 1), TriVec3d(0, 1, 0), TriVec3d(0, 0, 0)))

    TriangleB1 = Triangle3d((TriVec3d(1, 0, 1), TriVec3d(0, 0, 1), TriVec3d(0, 0, 0)))
    TriangleB2 = Triangle3d((TriVec3d(1, 0, 1), TriVec3d(0, 0, 0), TriVec3d(1, 0, 0)))

    MyMesh = Mesh3d([TriangleT1,TriangleT2,TriangleS1,TriangleS2,TriangleE1,TriangleE2,TriangleN1,TriangleN2,TriangleW1,TriangleW2,TriangleB1,TriangleB2])


if __name__ == "__main__":
    main()