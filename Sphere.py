from Engine import *


tri0 = TriVec3d(-0.5,0,0)
tri1 = TriVec3d(0,0.5,0)
tri2 = TriVec3d(0,0,0.5)
tri3 = TriVec3d(0.5,0,0)
tri4 = TriVec3d(0,-0.5,0)

#Upper half
face0 = Triangle3d([tri2,tri1,tri0])
face1 = Triangle3d([tri2,tri3,tri1])
face2 = Triangle3d([tri2,tri4,tri3])
face3 = Triangle3d([tri2,tri0,tri4])


tri5 = TriVec3d(0,0,-0.5)

#Lower half
face4 = Triangle3d([tri1,tri5,tri0])
face5 = Triangle3d([tri3,tri5,tri1])
face6 = Triangle3d([tri4,tri5,tri3])
face7 = Triangle3d([tri0,tri5,tri4])

#Octahedron base
basemesh = Mesh3d([face0,face1,face2,face3,face4,face5,face6,face7])




#While my engine can only render polygons at the moment 
#we can aproximate a sphere with lots of triangles
#Starting with a octahedron with its vertexes on the surface of a sphere with a radius 0.5
#We can then subdivide each face and then place the new vertexes on the edge of the sphere
#with more and more subdivisions we can aproximate a sphere more closely 
class sphere(Object3d):
    def __init__(self,radius: float, lod: int, center: TriVec3d):
        self.mesh = basemesh
        self.radius = radius
        self.center = center

        self.sphereScale(radius)


        super().__init__(self.mesh)


    def subdivide(self,NumberOfSubDivs: int):

        newMesh = Mesh3d([])
        count = 0
        for triangle in self.mesh.triangles:
            
            point01 = midpoint(triangle.vects[0],triangle.vects[1])
            point12 = midpoint(triangle.vects[1],triangle.vects[2])
            point20 = midpoint(triangle.vects[2],triangle.vects[0])
            
            normalizeANDmultiply(point01, self.radius)
            normalizeANDmultiply(point12, self.radius)
            normalizeANDmultiply(point20, self.radius)

            ntri0 = Triangle3d([triangle.vects[0], point01, point20])
            ntri1 = Triangle3d([point01, triangle.vects[1], point12])
            ntri2 = Triangle3d([point20, point12, triangle.vects[2]])
            ntri3 = Triangle3d([point20, point01, point12])

            newMesh.triangles.append(ntri0)
            newMesh.triangles.append(ntri1)
            newMesh.triangles.append(ntri2)
            newMesh.triangles.append(ntri3)
            count+= 4


        print("Subdivide finished with " + str(count) + " triangles.")
        self.mesh = newMesh

    def sphereScale(self, radius: float):
        for triangle in self.mesh.triangles:
            for vect in triangle.vects:
                normalizeANDmultiply(vect, radius)

    def translate(self, newCenter: TriVec3d):
        diffx = self.center.x - newCenter.x
        diffy = self.center.y - newCenter.y
        diffz = self.center.z - newCenter.z

        self.center = newCenter

        for tri in self.mesh.triangles:
            for vect in tri:
                vect.x += diffx
                vect.y += diffy
                vect.x += diffz
        
    
def midpoint(vector1: TriVec3d, vector2: TriVec3d):
    #print("Midpoint")
    x = (vector1.x + vector2.x)/2
    y = (vector1.y + vector2.y)/2
    z = (vector1.z + vector2.z)/2
    #print("Midpoint: (" + str(x) + ", " + str(y) + ", " + str(z))
    return TriVec3d(x, y, z)

def normalizeANDmultiply(vector: TriVec3d, radius: float):
    x = vector.x
    y = vector.y
    z = vector.z

    len = math.sqrt(x*x + y*y + z*z)

    vector.x /= len 
    vector.y /= len 
    vector.z /= len 

    vector.x *= radius
    vector.y *= radius
    vector.z *= radius




if __name__ == "__main__":
    print("Start from Mymeshes.py!")


        