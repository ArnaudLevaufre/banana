#-*- encoding: utf-8 -*-

import pyglet, pyglet.window.key as key, os, sys
import gameEngine, entity

from pyglet.gl import *

class Game:
    def __init__(self):
#        self.map
#        self.player
#        self.NPCs 
#        self.entity
#        self.level
#        self.camera
        self.uiBatch = pyglet.graphics.Batch()
        image = pyglet.image.load('sprites/vis.png')
        
        
        self.map = Map()
        self.cursor = pyglet.sprite.Sprite(image, gameEngine.GameEngine.W_WIDTH/2, gameEngine.GameEngine.W_HEIGHT/2, batch = self.uiBatch)
        self.player = entity.Player(200,200)
        
    def simulate(self, dt, keysHandler):
        if keysHandler[key.Z]:
            self.player.move(0,10, dt)
        elif keysHandler[key.S]:
            self.player.move(0, -10, dt)
        
        if keysHandler[key.Q]:
            self.player.move(-10, 0, dt)
        elif keysHandler[key.D]:
            self.player.move(10, 0, dt)
        
        self.map.setRelativePos( -self.player.x, -self.player.y)
    
    def on_mouse_motion(self,x,y,dx,dy):
        self.cursor.x = x - self.cursor.width / 2
        self.cursor.y = y - self.cursor.height / 2
        
    def render(self):        
        xCenter = gameEngine.GameEngine.W_WIDTH / 2
        yCenter = gameEngine.GameEngine.W_HEIGHT / 2
        
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        
        pyglet.gl.glVertex2i( xCenter, yCenter )
        pyglet.gl.glVertex2i( xCenter, yCenter + 16 )
        pyglet.gl.glVertex2i( xCenter + 16, yCenter + 16 )
        pyglet.gl.glVertex2i( xCenter + 16, yCenter )
        pyglet.gl.glEnd()
        
        self.map.render()
        self.uiBatch.draw()
        
class Map:
    """
    La carte est sibolisée par une matrice de chiffres
    représentant les éléments graphiques tels que les murs.
    Elle est divisé en case de 16 pixels par 16 pixels
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
        self.xRelative = int(x)
        self.yRelative = int(y)
        
    def load(self, filename):
        if os.path.isfile("maps/"+filename):
            file = open("maps/"+filename)
            
            section = None
            for line in file:
                # detection de la section
                if line == "[INIT]\n":
                    section = "init"
                elif line == "[MAP]\n":
                    section = "map"
                
                if section == "init":
                    pass
                
                if section == "map":
                    if line != "\n" and line != "[MAP]\n":
#                        try:
                        args = line.split(" ")
                        tile = args[0].split(":")
                        tile[0], tile[1] = int(tile[0]), int(tile[1])
                        self.map.append(Tile(tile[1]*self.tileSize, tile[0]*self.tileSize, args[1], None))
#                        except:
#                            print "Erreur: impossible de charger la carte [ "+filename+" ] le fichier est mal formé."
#                            sys.exit()
                            
            file.close()

    def render(self):
        glBindTexture(self.textures[0].target, self.textures[0].texture.id)
            
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        
        for tile in self.map:
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
            

class Tile:
    def __init__(self, x, y, type, texture):
        self.x = x
        self.y = y
        self.texture = texture
        self.type = type
    
    


        
