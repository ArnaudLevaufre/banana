# coding=utf-8
import pyglet
import gameEngine
import xml.etree.ElementTree as ET
import time

class Cinematic(object):
    def __init__(self, filename = None):
        """
        Créér une cinématique a partir du fichier XML filename
        
        :param filename: Chemin du fichier
        
        :type filename: str
        """
        # ---- Variables ---- #
        self._lastOnDrawTime = time.time()
        self._dt = 0
        self._time = 0
        self._endTime = 1000
        self.W_HEIGHT = gameEngine.GameEngine.W_HEIGHT
        self.W_WIDTH = gameEngine.GameEngine.W_WIDTH
        self._mainDrawingBatch = pyglet.graphics.Batch() # Batch que l'on va draw
        self._elements = [] # Elements de la cinématique
        # Construction
        self.constructFromFile()

    def constructFromFile(self, filename =None):
        """
        Construction d'une cinematique a partir d'un fichier xml
        
        :param filename: Chemin du fichier XML
        
        :type filename: str
        """
        
        fileName = "Cin/1.xml" 
        # On parse le XML
        tree = ET.parse(fileName)
        root = tree.getroot()
        for child in root:
            if(child.tag == "border"): # Si on veut une bordure
                self._elements.append(Border(self._mainDrawingBatch,ch = [childs for childs in child],**child.attrib))
            if(child.tag == "image"): # Si c'est une image
                self._elements.append(Image(self._mainDrawingBatch,ch = [childs for childs in child], **child.attrib))
            if(child.tag == "end"):
                if(child.attrib['time']):
                    self._endTime = int(child.attrib["time"])
            
    def run(self): # Fonction pour afficher notre cinematique a l'écran
        
        self._dt = time.time() - self._lastOnDrawTime # Calcul de dt
        self._time += self._dt
        for elmt in self._elements:
            elmt.animate(self._dt) # On anime tous les elements
        self._lastOnDrawTime = time.time()  
        self._mainDrawingBatch.draw()
        print int(self._time) , self._endTime
        if(int(self._time) > self._endTime):
            return False
        
        
#########################################################   
#                     Bordure                           #
#########################################################
class Border(pyglet.sprite.Sprite):
        
    def __init__(self,batch,ch = None,text = "", textSize = "24", pos = "bot", height = None, width = None, velY = 80, maxY = None):
        """
        Dessine une bordure noire a l'écran a la position pos
        Si il y a une balise <textChange>Text</textChange>, "Text" sera placé au milieu de la bordure
        
        :param textSize: Taille de la police
        :param height: Hauteur de la bordure
        :param width: Largeur
        :param velY: Vitesse en Y
        :param maxY: Y maximum de la bordure (coté bas de la bordure)
        
        :type textSize: int
        :type height: int
        :type width: int
        :type velY: int|float
        :type maxY: int
        """
        
        # ---- Constantes ---- #
        self._batch = batch
        self.W_HEIGHT = gameEngine.GameEngine.W_HEIGHT
        self.W_WIDTH = gameEngine.GameEngine.W_WIDTH
        
        # ---- Temps ---- #
        self._time = 0
        
        # ---- Taille ---- #
        if(height == None):
            height = self.W_HEIGHT/4
        if(width == None):
            width = self.W_WIDTH
            
        # ---- Vitesse ---- #
        self._velY = int(velY)
        
        # ---- Image ---- #
        super(Border, self).__init__(pyglet.image.create(width, height, pyglet.image.SolidColorImagePattern((0,0,0,255))))
        
        # ---- Position ---- #
        self.pos = pos
        if(pos == "bot"):
            self.y = -self.height
            if(maxY == None):
                self._maxY = 0
            else:
                self._maxY = int(maxY)
        elif(pos == "top"):
            if(maxY == None):
                self._maxY = self.W_HEIGHT - self.height +2
            else:
                self._maxY = int(maxY)
            self.y = self.W_HEIGHT 
               
        # ---- Texte ---- #
        if(text != None):
            # ---- Contenu ---- #
            self.textContent = text
            # ---- Size ---- #
            self.textSize = int(textSize)
            self.text = pyglet.text.Label(self.textContent,font_size=self.textSize, batch=self._batch,anchor_x ="center", anchor_y="center",x=self.width/2, y=self.height/2, color=(255,255,255,255))
        else:
            self.text = None
            
        # Parsage des childs avec des petits oignons
        self._toDoChangeText = {}
        for elmt in ch:
            if elmt.tag == "textChange":
                self._toDoChangeText[elmt.attrib['time']] = elmt.text
            
    def animate(self,dt):
        """
        Anime le tout selon les parametres definis auparavant
        """
        self._time += dt
        
        if(self.pos == "bot"): # Bordure en bas
            if(int(self.y) < self._maxY):
                self.y += self._velY * dt       
        elif(self.pos == "top"): # En haut
            if(int(self.y) > self._maxY):
                self.y -= self._velY * dt
                
        if(self.text != None): # Si il y a du texte
            for elmt in self._toDoChangeText:
                if(int(self._time) >= int(elmt)):
                    self.text.text = self._toDoChangeText[elmt] # On le change
                    self.text.y = self.y + self.height /2 # Et on le place au centre
                    self.text.x = self.x + self.width /2

###############################################
#                   Image                     #
###############################################
class Image(pyglet.sprite.Sprite):

    def __init__(self, batch,ch = None, path = None, x= 250, y = 250):
        """
        Dessine une image "path" a la position (x,y)
        Si il y a une balise <move x="350" y="325" timeStart="2" timeStop="3"/> 
        l'image bouge jusqu'en (x,y) a partir du temps timeStart jusqu'au temps timeStop
        
        :param batch: Batch dans lequel inserer notre sprite
        :param ch: Enfants, pour avoir les transitions
        :param path: Chemin vers l'image
        :param x: x initial
        :param y: y initial
        
        :type batch: Batch
        :type ch: XML
        :type path: str
        :type x: str | int
        :type y: str | int
        """
        self._batch = batch
        super(Image, self).__init__(pyglet.image.load(path))
        # ---- Position ---- #
        self.x = int(x)
        self.y = int(y)
        
        # ---- Temps ---- #
        self._time = 0
        self._firstAnim = True
        
        # ---- Parsage des enfants avec des petits pois ---- #
        self._toDoMovement = {}
        for elmt in ch:
            if elmt.tag == "move": # Si on demande de move
                attrib = {}
                for i in elmt.attrib:
                    attrib[i] = elmt.attrib[i] 
                self._toDoMovement[elmt.attrib['timeStart']] = attrib # Alors on le mets dans le todo
                
    def animate(self, dt):
        """
        Anime le tout selon les parametres definis auparavant
        """
        
        self._time += dt
        delete = ""
        if self._firstAnim: # Si c'est le premier appel
            self._actualX = self.x # On sauvegarde x et y
            self._actualY = self.y

        for elmt in self._toDoMovement: # On regarde la liste de todo
            if(int(self._toDoMovement[elmt]['timeStop']) >= int(self._time) >= int(elmt)) and not self._firstAnim: # Si on est entre le timeStart et le timeStop d'un move, on bouge l'image
                    self.x += dt * (int(self._toDoMovement[str(int(elmt))]['x']) - self._actualX) / (int(self._toDoMovement[str(int(elmt))]['timeStop']) - int(self._toDoMovement[str(int(elmt))]['timeStart']))
                    self.y += dt * (int(self._toDoMovement[str(int(elmt))]['y']) - self._actualY) / (int(self._toDoMovement[str(int(elmt))]['timeStop']) - int(self._toDoMovement[str(int(elmt))]['timeStart']))
            if(int(self._time) >= int(self._toDoMovement[elmt]['timeStop'])): # Si on a depassé le timeStop, la tache est faite, on prepare la deletion de cette derniere
                self._actualX = self.x # Et on enregistre la nouvelle position
                self._actualY = self.y
                delete=str(int(elmt))
            if(self._firstAnim): # Si on passe une fois ici, ce n'est plus le premier appel
                self._firstAnim = False
        if(self._toDoMovement.has_key(delete)): # On delete le todo
            self._toDoMovement.pop(delete)
        
