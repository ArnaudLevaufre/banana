#-*- encoding:utf-8 -*-
import pyglet, os, xml.etree.ElementTree as xml

# ---------------------------------------------------
class Map(object):
    """
    La carte est un tableau d'objets Tile
    """
    
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.map = []
        self.textures = []
        self.sprites = []
        
        # -IA -
        self.sizeX = 0
        self.sizeY = 0
        self.collidable = []
        
        self.loadTextures()
        
    def loadTextures(self):
        tileSheet = pyglet.image.load("data/sprites/tile-map.jpg")
        imageGrid = pyglet.image.ImageGrid(tileSheet, tileSheet.width/64, tileSheet.height/64)
        
        # on réordonne les tiles de maniere plus propre
        # c'est a dire du haut à gauche jusqu'en bas à droite
        for y in range(tileSheet.height/64 - 1, 1, -1):
            for x in range(tileSheet.width/64):
                self.textures.append(imageGrid[y*(tileSheet.height/64) + x])

    def load(self, fileName):
        if os.path.isfile("data/maps/"+fileName):
            xmlTree = xml.parse("data/maps/"+fileName)
            root = xmlTree.getroot()
            self.sizeX = int(root.attrib['sizeX'])
            self.sizeY = int(root.attrib['sizeY'])
            for child in root:
                if child.tag == "tile":
                    # On ajoute la case dans le tableau représentant la carte
                    self.map.append(Tile( **child.attrib ))
                    if(child.attrib['collision'] == "True"):
                        self.collidable.append((int( child.attrib["x"]),int(child.attrib["y"])))
#                     pyglet.text.Label( str((child.attrib["x"],child.attrib["y"])),x=int(child.attrib["x"])*Tile.SIZE +32, y=int(child.attrib["y"])*Tile.SIZE +32 , batch=self.batch, anchor_x="center", anchor_y="center", bold=True, font_size=8)                     
                    # On ajoute la texture de la case dans le batch
                    self.sprites.append(pyglet.sprite.Sprite(self.textures[int(child.attrib["type"])], x=int(child.attrib["x"])*Tile.SIZE, y=int(child.attrib["y"])*Tile.SIZE , batch=self.batch ))
        else:
            print "couldn't load the map ["+fileName+"]. No such file."
                            
    def collide(self, x,y,w,h):
        """
                                == COLlIDE ==
        
        La fonction collide permet de savoir si l'objet défnis par ses
        coordonées et ses dimensions passées en paramètres se trouve
        sur le sol ou non.
        Lorsqu'aucune collision n'est détecté on retourne False
        Si une collision est détectée alors on renvoie True
        
        :param x: Position x de l'objet
        :param y: Position y de l'objet
        :param w: Largeur de l'objet
        :param h: Hauteur de l'objet
        
        :type x: int | float
        :type y: int | float
        :type w: int | float
        :type h: int | float
        
        :rtype: bool
        """
        # One does not simply understand what's written there
        for tile in self.map:
            if tile.collision == True:
                if tile.x <= x <= tile.x + Tile.SIZE or tile.x <= x+w <= tile.x + Tile.SIZE:
                    # Si la position gauche (x) ou la position droite (x+w)
                    # est comprise entre le bord gauche et droite de la tile.
                    if tile.y <= y <= tile.y + Tile.SIZE or tile.y <= y+h <= tile.y + Tile.SIZE:
                        # [1] Si la position du bas (y) ou la position du haut (y+h) 
                        # est comprise entre le bord haut et le bord bas de la tile.
                        return True
                    elif y <= tile.y <= y+h or y <= tile.y + Tile.SIZE <= y+h:
                        # [2] si le bord bas (tile.y) ou le bord haut(tile.y+Tile.SIZE) est 
                        # compris entre le position du bas (y) et la position du haut 
                        # (y+h) de l'objet à tester.
                        return True
                    
                elif x <= tile.x <= x+w or x <= tile.x + Tile.SIZE <= x+w:
                    # Si le bord gauche ou le bord droit de la tile est compris
                    # entre la position gauche et droite de l'objet à tester.
                    if (tile.y <= y <= tile.y + Tile.SIZE) or (tile.y <= y+h <= tile.y + Tile.SIZE):
                        # Voir [1]
                        return True
                    elif y <= tile.y <= y+h or y <= tile.y + Tile.SIZE <= y+h:
                        # voir [2]
                        return True
                    
        return False
    
    def render(self):
        self.batch.draw()

# ----------------------------------

class Tile:
    SIZE = 64
    
    def __init__(self, x, y, collision, type):
        self.x = int(x) * self.SIZE
        self.y = int(y) * self.SIZE
        self.texture = int(type)
        
        if collision == "True":
            self.collision = True
        else:
            self.collision = False