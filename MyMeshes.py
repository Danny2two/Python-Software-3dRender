import math
import arcade
import numpy
from Engine import *
from STLParser import *
frametimes = [0,0,0,0,0,0,0,0,0,0]

SW = 1000
SH = 800

'''
This is the file that you should use to parse your 3d object file and start the engine. 
Just replace path with the path to your obj, or use one of the ones provided.
THIS IS MEANT FOR LOW POLY MODELS greater that about 5000 polygons might work but it will be SLOW
- I recommend using this site https://lowpoly3d.xyz/ to reduce the polygons of models.
    If your model will not work run it through the site as it can strip somethings that confuse my parser off
    of the model. 

Multiple files can be parsed and added to a list, they will all render in the same window 
****Multiple objects are not really supported well but it will "work"


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
#THIS IS WHERE YOU ENTER IN YOR MODEL TO BE RENDERED. often very small scales are needed to see properly
MyMesh2 = parseOBJ("LowPolyStatue1872.obj", 0, 0.01) #path to obj, z offeset, scale
MyMeshList = [MyMesh2]

        


class MWindow(arcade.Window):
    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        self.framecount = 0
        self.set_mouse_visible(True)
        self.set_vsync(True)
        self.set_update_rate(1/60) #1 / (TARGET FRAMERATE)
        arcade.set_background_color(arcade.color.BLACK)
        self.baseOBJ = MyMeshList[0]
        self.baseOBJ.colorRGB = [0,200,200] #Set the color of the model 
        self.baseOBJ.lightvector = TriVec3d(0,1,-1) #sets the direction of the lights
        self.myobjects = MyMeshList



    def on_draw(self):
        arcade.start_render()
        for object in self.myobjects:
          object.on_draw(object.mesh)
        arcade.draw_text(str(numpy.average(frametimes)) + " FPS",5,SH-20,arcade.color.PURPLE,12) #Draw Framerate

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
            #print("up")
            for i in self.myobjects:
                i.translateupdateZ(-0.5)
            

        if symbol == 115:
            #print("down")
            for i in self.myobjects:
                i.translateupdateZ(0.5)
           

        if symbol == 97:
            #print("left")
            for i in self.myobjects:
                i.translateupdateX(0.1)
           

        if symbol == 100:
            #print("right")
            for i in self.myobjects:
                i.translateupdateX(-.1)

        if symbol == 65362:
            for i in self.myobjects:
                i.scaleTriangles(0.1)

        if symbol == 65364:
            for i in self.myobjects:
                i.scaleTriangles(-0.1)
         

        if symbol == 113:
            #print("rotL")
            for i in self.myobjects:
                i.dxtheta -= 0.01
        if symbol == 101:
            #print("rotR")
            for i in self.myobjects:
                i.dxtheta += 0.01
        if symbol == 116:
            #print("rotL")
            for i in self.myobjects:
                i.dztheta += 0.01
        if symbol == 103:
            #print("rotL")
            for i in self.myobjects:
                i.dztheta -= 0.01
        

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        for i in self.myobjects:
            i.ztheta += -dx/360
            i.xtheta += dy/360

def main():
    mywindow = MWindow(SW, SH, "3D Test")
    print(
        "CONTROLS:  Click and drag to rotate \n Q or E and T or G Will cause the model to spin \n Up arrow and down arrow scale the model \n WSAD move the model but this is broken")
    arcade.run()

if __name__ == "__main__":
    main()