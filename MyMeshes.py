import math
import arcade
import numpy
from Engine import *
from STLParser import *
frametimes = [0,0,0,0,0,0,0,0,0,0]

SW = 1000
SH = 800

'''
#Testcube
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
'''


#MyMesh = Mesh3d([TriangleT1,TriangleT2,TriangleS1,TriangleS2,TriangleE1,TriangleE2,TriangleN1,TriangleN2,TriangleW1,TriangleW2,TriangleB1,TriangleB2])


#MyMesh2 = parseOBJ("Statue.obj",0,0.01)
#MyMesh2 = parseOBJ("XYZCUBE.obj", 0, .01)
#MyMesh2 = parseOBJ("teapotsimp.obj", 0, 0.1)
MyMesh2 = parseOBJ("Model.obj", 0, 0.004)
#MyMesh2 = parseOBJ("Charmander.obj", 0, 0.01)
MyMeshList = [MyMesh2]

        


class MWindow(arcade.Window):
    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        self.framecount = 0
        self.set_mouse_visible(True)
        self.set_vsync(True)
        self.set_update_rate(1/60)
        arcade.set_background_color(arcade.color.BLACK)
        self.baseOBJ = MyMeshList[0]
        self.baseOBJ.colorRGB = [0,200,200]
        self.myobjects = MyMeshList



    def on_draw(self):
        arcade.start_render()
        for object in self.myobjects:
          object.on_draw(object.mesh)
        arcade.draw_text(str(numpy.average(frametimes)),5,SH-20,arcade.color.PURPLE,12)

    def update(self, delta_time: float):
        for object in self.myobjects:
            object.on_update()
        
        if self.framecount >= 10:
            self.framecount = 0
        frametimes[self.framecount] = (1/ delta_time)
        self.framecount += 1

        pass


    def on_key_press(self, symbol, modifiers: int):
        print(symbol)

        if symbol == 119:
            print("up")
            for i in self.myobjects:
                i.translateupdateZ(-0.5)
            

        if symbol == 115:
            print("down")
            for i in self.myobjects:
                i.translateupdateZ(0.5)
           

        if symbol == 97:
            print("left")
            for i in self.myobjects:
                i.translateupdateX(0.1)
           

        if symbol == 100:
            print("right")
            for i in self.myobjects:
                i.translateupdateX(-.1)

        if symbol == 65362:
            for i in self.myobjects:
                i.scaleTriangles(0.1)

        if symbol == 65364:
            for i in self.myobjects:
                i.scaleTriangles(-0.1)
         

        if symbol == 113:
            print("rotL")
            for i in self.myobjects:
                i.dxtheta -= 0.01
        if symbol == 101:
            print("rotR")
            for i in self.myobjects:
                i.dxtheta += 0.01
        if symbol == 116:
            print("rotL")
            for i in self.myobjects:
                i.dztheta += 0.01
        if symbol == 103:
            print("rotL")
            for i in self.myobjects:
                i.dztheta -= 0.01
        

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        for i in self.myobjects:
            i.ztheta += -dx/360
            i.xtheta += dy/360

def main():
    mywindow = MWindow(SW, SH, "3D Test")
    print(
        "CONTROLS: ")
    arcade.run()

if __name__ == "__main__":
    main()