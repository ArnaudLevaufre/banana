#-*- encoding: utf-8 -*-

import pyglet, pyglet.window.key as key, os, sys
import gameEngine, entity

from pyglet.gl import *

class Game:
    def __init__(self):

        self.uiBatch = pyglet.graphics.Batch()

        self.player = entity.Player(0,0)
        self.map = Map()
        self.map.load("001", self.player)
        self.map.setRelativePos(-self.player.x, -self.player.y)
        
    def simulate(self, dt, keysHandler):
        if keysHandler[key.Z]:
            self.player.move(0,10, self.map,dt)
        elif keysHandler[key.S]:
            self.player.move(0, -10, self.map, dt)
        
        if keysHandler[key.Q]:
            self.player.move(-10, 0, self.map,dt)
        elif keysHandler[key.D]:
            self.player.move(10, 0, self.map,dt)

        
        self.map.setRelativePos( -self.player.x, -self.player.y)
    def on_mouse_press(self,x, y, button, modifiers):
        if(button == pyglet.window.mouse.LEFT):
            print x,y
            
    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        if(buttons == pyglet.window.mouse.LEFT):
            print x,y
            
    def render(self):       
        self.uiBatch = pyglet.graphics.Batch() # On actualise
        
        self.uiBatch.add(4, pyglet.gl.GL_QUADS, None,
        ('v2i', (0,gameEngine.GameEngine.W_HEIGHT-16,self.player.hp*2,gameEngine.GameEngine.W_HEIGHT-16,self.player.hp*2,gameEngine.GameEngine.W_HEIGHT,0,gameEngine.GameEngine.W_HEIGHT)),
        ('c3B',(255,0,0,255,0,0,255,0,0,255,0,0))
        )
        self.player.hp -= 1        

        self.map.render()
        self.uiBatch.draw()
        self.player.render()
        
        glBegin(GL_LINES)
        glVertex2i(0,0)
        glVertex2i(1024,640)
        glVertex2i(0,640)
        glVertex2i(1024,0)
        glEnd()

class Map:
    """
    La carte est sibolisée par une matrice de chiffres
    représentant les éléments graphiques tels que les murs.
  
    """
    
    
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.xRelative = 0
        self.yRelative = 0
        self.map = []
        self.textures = []
        self.tileSize = 64
        self.loadTextures()
        self.load("001")
                
    def loadTextures(self):
        tileSheet = pyglet.image.load("sprites/tile-map.bmp")
        imageGrid = pyglet.image.ImageGrid(tileSheet, tileSheet.width/64, tileSheet.height/64)
        
        # on réordonne les tiles de miniere plus propre
        # c'est a dire du haut a gauche jusqu'en bas a droite
        for y in range(tileSheet.height/64 - 1, 1, -1):
            for x in range(tileSheet.width/64):
                self.textures.append(imageGrid[y*(tileSheet.height/64) + x].get_texture())
        
    def setRelativePos(self, x, y):
        self.xRelative = int(x) + gameEngine.GameEngine.W_WIDTH/2
        self.yRelative = int(y) + gameEngine.GameEngine.W_HEIGHT/2
        
    def load(self, filename, player=None):
        if os.path.isfile("maps/"+filename):
            file = open("maps/"+filename)
            
            section = None
            for line in file:
                line = line[:-1]
                # detection de la section
                if line == "[INIT]":
                    section = "init"
                elif line == "[MAP]":
                    section = "map"
                
                if section == "init":
                    if line != "" and line != "[INIT]":
                        splited = line.split("=")
                        if splited[0] == "PLAYERPOS" and player != None:
                            player.x = int(splited[1].split(":")[0]) * self.tileSize
                            player.y = int(splited[1].split(":")[1]) * self.tileSize

                if section == "map":
                    if line != "" and line != "[MAP]":
                        try:
                            args = line.split(" ")
                            tile = args[0].split(":")
                            tile[0], tile[1] = int(tile[0]), int(tile[1])
                            self.map.append(Tile(tile[0]*self.tileSize, tile[1]*self.tileSize, args[1], int(args[2])))
                        except:
                            print "Erreur: impossible de charger la carte [ "+filename+" ] le fichier est mal formé."
                            sys.exit()
                            
            file.close()
    def colide(self, x,y,w,h):
        """
                                == COLIDE ==
        
        La fonction colide permet de savoir si l'objet défnis par ses
        coordonées et ses dimensions passées en paramètres se trouve
        sur le sol ou non.
        Lorsqu'aucune colision n'est détecté on retourne False
        Si une colision est détectée alors on renvoie True
        
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
            if x >= tile.x and x <= tile.x + self.tileSize:
                if y >= tile.y and y <= tile.y + self.tileSize:
                    if tile.type != "FLOOR":
                        print "collide", tile.type
                        return True
            if x+w >= tile.x and x+w <= tile.x + self.tileSize:
                if y+h >= tile.y and y+h <= tile.y + self.tileSize:
                    if tile.type != "FLOOR":
                        print "collide", tile.type
                        return True
        return False
    def render(self):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        
        for tile in self.map:
            glBindTexture(self.textures[tile.texture].target, self.textures[tile.texture].texture.id)
            pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
            glTexCoord2i(0,0)
            glVertex2i(self.xRelative + tile.x, self.yRelative + tile.y)
            glTexCoord2i(1,0)
            glVertex2i(self.xRelative + tile.x + self.tileSize, self.yRelative + tile.y)
            glTexCoord2i(1,1)
            glVertex2i(self.xRelative + tile.x + self.tileSize, self.yRelative + tile.y + self.tileSize)
            glTexCoord2i(0,1)
            glVertex2i(self.xRelative + tile.x, self.yRelative + tile.y + self.tileSize)
            pyglet.gl.glEnd()
        
        glDisable(GL_TEXTURE_2D)
            

class Tile:
    def __init__(self, x, y, type, texture):
        self.x = x
        self.y = y
        self.texture = int(texture)
        self.type = type
    
    


        
