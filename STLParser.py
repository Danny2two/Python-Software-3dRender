from Engine import *
import os

def parseSTL(stl_path):
    myobjectfile = open(stl_path,"rt")

    vertexlist = []
    trianglelist = []

    invertex = False

    for line in myobjectfile:
        line = line.strip("\n")
        line = line.strip()
        #print(line)

        if line.startswith("vertex"):
            splitline = line.split(" ")
            #print(splitline)
            vertexlist.append(TriVec3d(float(splitline[1]),float(splitline[2]),float(splitline[3])))

        if line.startswith("outer loop"):
            invertex = True
        if line.startswith("outer loop"):
            invertex = False

        if line.startswith("endfacet"):
            trianglelist.append(Triangle3d(vertexlist))
            vertexlist = []
            
    createdmesh = Mesh3d(trianglelist)
    myobjectfile.close
    myobj = Object3d(createdmesh)
    return myobj

def parseOBJ(OBJ_path, Zoffset, scale):
    Zoffset = int(Zoffset)
    myobjectfile = open(OBJ_path,"rt")

    vertexlist = [0]
    trianglelist = []

    

    for line in myobjectfile:
        line = line.strip("\n")
        

        if line.startswith("v"):
            splitline = line.split(" ")
            print(splitline)
            vertexlist.append(TriVec3d(float(splitline[1]) * scale,float(splitline[2])* scale,((float(splitline[3]) * scale)+ float(Zoffset))))

       

        if line.startswith("f"):
            splitline = line.split(" ")
            print(splitline)
            trianglelist.append(Triangle3d([vertexlist[int(splitline[1])],vertexlist[int(splitline[2])],vertexlist[int(splitline[3])]]))
           
    createdmesh = Mesh3d(trianglelist)
    myobjectfile.close
    myobj = Object3d(createdmesh)
    return myobj

def parseGROUPSTL(path_to_folder_of_stls,scale):
    meshlist = []
    objlist = []
    polycount = 0
    for filename in os.listdir(path_to_folder_of_stls):
        with open(os.path.join(path_to_folder_of_stls, filename), 'rt') as f:
            myobjectfile = f

            vertexlist = []
            trianglelist = []

            invertex = False

            for line in myobjectfile:
                line = line.strip("\n")
                line = line.strip()
                #print(line)

                if line.startswith("vertex"):
                    splitline = line.split(" ")
                    #print(splitline)
                    vertexlist.append(TriVec3d(float(splitline[1]) * scale,float(splitline[2]) * scale,float(splitline[3])* scale))

                if line.startswith("outer loop"):
                    invertex = True
                if line.startswith("outer loop"):
                    invertex = False

                if line.startswith("endfacet"):
                    polycount += 1
                    trianglelist.append(Triangle3d(vertexlist))
                    vertexlist = []
                    
            createdmesh = Mesh3d(trianglelist)
            myobjectfile.close
            meshlist.append(createdmesh) 

    for mesh in meshlist:
        objlist.append(Object3d(mesh))
        print("Created list of Objects with " + str(len(meshlist)) + " meshes and " + str(polycount) + " polygons")
    return objlist
