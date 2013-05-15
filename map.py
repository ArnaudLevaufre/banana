#-*- encoding:utf-8 -*-
import pyglet
import os
import xml.etree.ElementTree as xml

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
        imageGrid = pyglet.image.ImageGrid(tileSheet, tileSheet.width/64, tileSheet.height / 64)

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
                    self.map.append(Tile(**child.attrib))
                    if(child.attrib['collision'] == "True"):
                        self.collidable.append((int(child.attrib["x"]), int(child.attrib["y"])))
                    # On ajoute la texture de la case dans le batch
                    self.sprites.append(pyglet.sprite.Sprite(self.textures[int(child.attrib["type"])], x=int(child.attrib["x"])*Tile.SIZE, y=int(child.attrib["y"])*Tile.SIZE, batch=self.batch))
        else:
            print "couldn't load the map ["+fileName+"]. No such file."

    def collide(self, x, y, w, h):
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

        # Ici nous recherchon a obtenir un impact minimal
        # sur les performances, c'est pourqu'oi nous
        # retardons au maximum la déclarations de variables.
        # dans certains cas, on économise donc 1 ou 2 déclarations

        # dx, dy, dxw, dyh représent des coordonnées en terme de case.
        dx = int(x / Tile.SIZE)
        dy = int(y / Tile.SIZE)

        if (dx, dy) in self.collidable:
            # coin bas gauche
            return True
        
        dxw = int((x + w) / Tile.SIZE)
        if (dxw, dy) in self.collidable:
            # coin bas droit
            return True

        dyh = int((y + h) / Tile.SIZE)
        if (dxw, dyh) in self.collidable:
            # coin haut droit
            return True

        if (dx, dyh) in self.collidable:
            # coin haut gauche
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
