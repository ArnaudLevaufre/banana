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
            if(child.tag == "border"): # Si on veut une bordure bot
                self.elements.append(Border(self.mainDrawingBatch,ch = [childs for childs in child],**child.attrib))
            elif(child.tag == "image"):
                self.elements.append(Image(self.mainDrawingBatch,ch = [childs for childs in child], **child.attrib))
#         for elmt in self.elements: # On ajoute tout dans le batch
#             elmt.batch = self.mainDrawingBatch
            
    def run(self): # Fonction pour afficher notre cinematique a l'écran
        self.dt = time.time() - self.lastOnDrawTime
        for elmt in self.elements:
            elmt.animate(self.dt) # On anime tous les elements
        self.lastOnDrawTime = time.time()  
        self.mainDrawingBatch.draw()
        
        
#########################################################   
#                     Bordure                           #
#########################################################
class Border(pyglet.sprite.Sprite):
    def __init__(self,batch,ch = None,text = "", textSize = "24", pos = "bot", height = None, width = None, velY = 80, maxY = None):
        # ---- Constantes ---- #
        self._batch = batch
        self.W_HEIGHT = gameEngine.GameEngine.W_HEIGHT
        self.W_WIDTH = gameEngine.GameEngine.W_WIDTH
        # ---- Temps ---- #
        self.time = 0
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
        # ---- Texte ---- #
        if(text != None):
            # ---- Contenu ---- #
            self.textContent = text
            # ---- Size ---- #
            self.textSize = int(textSize)
            self.text = pyglet.text.Label(self.textContent,font_size=self.textSize, batch=self._batch,anchor_x ="center", anchor_y="center",x=self.width/2, y=self.height/2, color=(255,255,255,255))
            print self.textContent
        else:
            self.text = None
        # Parsage des childs :D
        self.child = ch
        self.toDoChangeText = {}
        for elmt in self.child:
            if elmt.tag == "textChange":
                self.toDoChangeText[elmt.attrib['time']] = elmt.text
            
    def animate(self,dt):
        self.time += dt
        if(self.pos == "bot"):
            if(int(self.y) < self.maxY):
                self.y += self.velY * dt
        elif(self.pos == "top"):
            if(int(self.y) > self.maxY):
                self.y -= self.velY * dt
        if(self.text != None):
            for elmt in self.toDoChangeText:
                if(int(self.time) >= int(elmt)):
                    self.text.text = self.toDoChangeText[elmt]
            self.text.y = self.y + self.height /2
            self.text.x = self.x + self.width /2

###############################################
#                   Image                     #
###############################################
class Image(pyglet.sprite.Sprite):
    def __init__(self, batch,ch = None, path = None, x= 250, y = 250):
        self._batch = batch
        super(Image, self).__init__(pyglet.image.load(path))
        self.x = int(x)
        self.y = int(y)
        # ---- Temps ---- #
        self.time = 0
        self.child = ch
        self.toDoMovement = {}
        for elmt in self.child:
            if elmt.tag == "move":
                attrib = {}
                for i in elmt.attrib:
                    attrib[i] = elmt.attrib[i]
                self.toDoMovement[elmt.attrib['timeStart']] = attrib
                
    def animate(self, dt):
        self.time += dt
        delete = ""
        print self.toDoMovement
        for elmt in self.toDoMovement:
            if(int(self.time) >= int(elmt)):
                self.x= int(self.toDoMovement[str(int(self.time))]['x'])
                self.y = int(self.toDoMovement[str(int(self.time))]['y'])
                delete=str(int(self.time))
        if(self.toDoMovement.has_key(delete)):
            self.toDoMovement.pop(delete)
        
