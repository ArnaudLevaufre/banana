import pyglet
import gameEngine
import xml.etree.ElementTree as ET
import time
class Cinematic:
    def __init__(self):
        self.lastOnDrawTime = time.time()
        self.dt = 1
        self.W_HEIGHT = gameEngine.GameEngine.W_HEIGHT
        self.W_WIDTH = gameEngine.GameEngine.W_WIDTH
        self.mainDrawingBatch = pyglet.graphics.Batch()
        self.elements = []
        self.constructFromFile()

    def constructFromFile(self):
        fileName = "Cin/Cin1.xml" 
        tree = ET.parse(fileName)
        root = tree.getroot()
        for child in root:
            if(child.tag == "borderBot"):
                self.elements.append(Border("bot"))
            elif(child.tag == "borderTop"):
                self.elements.append(Border("top"))
                
        for elmt in self.elements:
            elmt.batch = self.mainDrawingBatch
            
    def run(self):
        self.dt = time.time() - self.lastOnDrawTime
        self.lastOnDrawTime = time.time()
        for elmt in self.elements:
            elmt.animate(self.dt)
        self.mainDrawingBatch.draw()

class Border(pyglet.sprite.Sprite):
    def __init__(self, pos):  
        print pos
        self.W_HEIGHT = gameEngine.GameEngine.W_HEIGHT
        self.W_WIDTH = gameEngine.GameEngine.W_WIDTH
        super(Border, self).__init__(pyglet.image.create(self.W_WIDTH, self.W_HEIGHT/4, pyglet.image.SolidColorImagePattern((0,0,0,255))))
        self.pos = pos
        if(pos == "bot"):
            self.y = -self.height
        elif(pos == "top"):
            self.y = self.W_HEIGHT
            
    def animate(self,dt):
        if(self.pos == "bot"):
            if(self.y < self.W_HEIGHT/4 - self.height):
                self.y += 20 * dt
                print self.y
        elif(self.pos == "top"):
            if(self.y > self.W_HEIGHT - self.height +2):
                self.y -= 20 * dt