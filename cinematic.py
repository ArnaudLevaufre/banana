# coding=utf-8
import pyglet
import gameEngine
import xml.etree.ElementTree as ET
import time


class Cinematic:
    
    def __init__(self, filename = None):
        # ---- Variables ---- #
        self.lastOnDrawTime = time.time()
        self.dt = 1
        self.W_HEIGHT = gameEngine.GameEngine.W_HEIGHT
        self.W_WIDTH = gameEngine.GameEngine.W_WIDTH
        self.mainDrawingBatch = pyglet.graphics.Batch()
        self.elements = []
        # Construction
        self.constructFromFile()

    def constructFromFile(self):
        """
        Construction d'une cinematique a partir d'un fichier xml
        """
        fileName = "Cin/Cin1.xml" 
        # On parse le XML
        tree = ET.parse(fileName)
        root = tree.getroot()
        for child in root:
            if(child.tag == "borderBot"): # Si on veut une bordure bot
                self.elements.append(Border("bot", **child.attrib))
            elif(child.tag == "borderTop"): # Bordure top
                self.elements.append(Border("top", **child.attrib))
                
        for elmt in self.elements: # On ajoute tout dans le batch
            elmt.batch = self.mainDrawingBatch
            
    def run(self): # Fonction pour afficher notre cinematique a l'écran
        self.dt = time.time() - self.lastOnDrawTime
        self.lastOnDrawTime = time.time()
        for elmt in self.elements:
            elmt.animate(self.dt) # On anime tous les elements
        self.mainDrawingBatch.draw()


#########################################################   
#                     Bordure                           #
#########################################################
class Border(pyglet.sprite.Sprite):
    def __init__(self, pos, height = None, width = None, velY = 80, maxY = None):
        # ---- Constantes ---- #
        self.W_HEIGHT = gameEngine.GameEngine.W_HEIGHT
        self.W_WIDTH = gameEngine.GameEngine.W_WIDTH
        # ---- Taille ---- #
        if(height == None):
            height = self.W_HEIGHT/4
        if(width == None):
            width = self.W_WIDTH
        # ---- Vitesse ---- #
        self.velY = int(velY)
        # ---- Image ---- #
        super(Border, self).__init__(pyglet.image.create(width, height, pyglet.image.SolidColorImagePattern((0,0,0,255))))
        # ---- Position ---- #
        self.pos = pos
        if(pos == "bot"):
            self.y = -self.height
            if(maxY == None):
                self.maxY = 0
            else:
                self.maxY = int(maxY)
        elif(pos == "top"):
            if(maxY == None):
                self.maxY = self.W_HEIGHT - self.height +2
            else:
                self.maxY = int(maxY)
            self.y = self.W_HEIGHT
        print self.maxY

    def animate(self,dt):
        if(self.pos == "bot"):
            if(int(self.y) < self.maxY):
                self.y += self.velY * dt
        elif(self.pos == "top"):
            if(int(self.y) > self.maxY):
                self.y -= self.velY * dt