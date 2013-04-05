# coding=utf-8
import pyglet
import gameEngine
import xml.etree.ElementTree as ET
import time

class Cinematic:
    def __init__(self, filename = None):
        # ---- Variables ---- #
        self.lastOnDrawTime = time.time()
        self.dt = 0
        self.time = 0
        self.endTime = 1000
        self.W_HEIGHT = gameEngine.GameEngine.W_HEIGHT
        self.W_WIDTH = gameEngine.GameEngine.W_WIDTH
        self.mainDrawingBatch = pyglet.graphics.Batch() # Batch que l'on va draw
        self.elements = [] # Elements de la cinématique
        # Construction
        self.constructFromFile()

    def constructFromFile(self, filename =None):
        """
        Construction d'une cinematique a partir d'un fichier xml
        """
        fileName = "Cin/1.xml" 
        # On parse le XML
        tree = ET.parse(fileName)
        root = tree.getroot()
        for child in root:
            if(child.tag == "border"): # Si on veut une bordure
                self.elements.append(Border(self.mainDrawingBatch,ch = [childs for childs in child],**child.attrib))
            if(child.tag == "image"): # Si c'est une image
                self.elements.append(Image(self.mainDrawingBatch,ch = [childs for childs in child], **child.attrib))
            if(child.tag == "end"):
                if(child.attrib['time']):
                    self.endTime = int(child.attrib["time"])
                    print self.endTime
            
    def run(self): # Fonction pour afficher notre cinematique a l'écran
        self.dt = time.time() - self.lastOnDrawTime # Calcul de dt
        self.time += self.dt
        for elmt in self.elements:
            elmt.animate(self.dt) # On anime tous les elements
        self.lastOnDrawTime = time.time()  
        self.mainDrawingBatch.draw()
        print int(self.time) , self.endTime
        if(int(self.time) > self.endTime):
            return False
        
        
#########################################################   
#                     Bordure                           #
#########################################################
class Border(pyglet.sprite.Sprite):
    """
    Dessine une bordure noire a l'écran a la position pos
    Si il y a une balise <textChange>Text</textChange>, "Text" sera placé au milieu de la bordure
    textSize = Taille de la police
    height = Hauteur de la bordure
    width = Largeur
    velY = Vitesse
    maxY = y maximum de la bordure (coté bas de la bordure)
    """
    
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
            
        # Parsage des childs avec des petits oignons
        self.child = ch
        self.toDoChangeText = {}
        for elmt in self.child:
            if elmt.tag == "textChange":
                self.toDoChangeText[elmt.attrib['time']] = elmt.text
            
    def animate(self,dt):
        """
        Anime le tout selon les parametres definis auparavant
        """
        self.time += dt
        if(self.pos == "bot"): # Bordure en bas
            if(int(self.y) < self.maxY):
                self.y += self.velY * dt
        elif(self.pos == "top"): # En haut
            if(int(self.y) > self.maxY):
                self.y -= self.velY * dt
        if(self.text != None): # Si il y a du texte
            for elmt in self.toDoChangeText:
                if(int(self.time) >= int(elmt)):
                    self.text.text = self.toDoChangeText[elmt] # On le change
            self.text.y = self.y + self.height /2 # Et on le place au centre
            self.text.x = self.x + self.width /2

###############################################
#                   Image                     #
###############################################
class Image(pyglet.sprite.Sprite):
    """
    Dessine une image "path" a la position (x,y)
    Si il y a une balise <move x="350" y="325" timeStart="2" timeStop="3"/> 
    l'image bouge jusqu'en (x,y) a partir du temps timeStart jusqu'au temps timeStop
    """
    def __init__(self, batch,ch = None, path = None, x= 250, y = 250):
        self._batch = batch
        super(Image, self).__init__(pyglet.image.load(path))
        # ---- Position ---- #
        self.x = int(x)
        self.y = int(y)
        # ---- Temps ---- #
        self.time = 0
        self.firstAnim = True
        
        # ---- Parsage des enfants avec des petits pois ---- #
        self.child = ch
        self.toDoMovement = {}
        for elmt in self.child:
            if elmt.tag == "move": # Si on demande de move
                attrib = {}
                for i in elmt.attrib:
                    attrib[i] = elmt.attrib[i] 
                self.toDoMovement[elmt.attrib['timeStart']] = attrib # Alors on le mets dans le todo
                
    def animate(self, dt):
        """
        Anime le tout selon les parametres definis auparavant
        """
        
        self.time += dt
        delete = ""
        if self.firstAnim: # Si c'est le premier appel
            self.actualX = self.x # On sauvegarde x et y
            self.actualY = self.y

        for elmt in self.toDoMovement: # On regarde la liste de todo
            if(int(self.time) >= int(elmt)) and ((int(self.time) <= int(self.toDoMovement[elmt]['timeStop']))) and not self.firstAnim: # Si on est entre le timeStart et le timeStop d'un move, on bouge l'image
                    self.x += dt * (int(self.toDoMovement[str(int(elmt))]['x']) - self.actualX) / (int(self.toDoMovement[str(int(elmt))]['timeStop']) - int(self.toDoMovement[str(int(elmt))]['timeStart']))
                    self.y += dt * (int(self.toDoMovement[str(int(elmt))]['y']) - self.actualY) / (int(self.toDoMovement[str(int(elmt))]['timeStop']) - int(self.toDoMovement[str(int(elmt))]['timeStart']))
            if(int(self.time) >= int(self.toDoMovement[elmt]['timeStop'])): # Si on a depassé le timeStop, la tache est faite, on prepare la deletion de cette derniere
                self.actualX = self.x # Et on enregistre la nouvelle position
                self.actualY = self.y
                delete=str(int(elmt))
            if(self.firstAnim): # Si on passe une fois ici, ce n'est plus le premier appel
                self.firstAnim = False
        if(self.toDoMovement.has_key(delete)): # On delete le todo
            self.toDoMovement.pop(delete)
        
