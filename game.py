#-*- encoding: utf-8 -*-

import pyglet, pyglet.window.key as key
import gameEngine, entity

class Game:
    def __init__(self):
#        self.map
#        self.player
#        self.NPCs 
#        self.entity
#        self.level
#        self.camera
        self.uiBatch = pyglet.graphics.Batch()
        self.map = Map()
#         self.cursor = pyglet.sprite.Sprite(image, gameEngine.GameEngine.W_WIDTH/2, gameEngine.GameEngine.W_HEIGHT/2, batch = self.uiBatch)

        self.player = entity.Player(200,200)
        
    def simulate(self, dt, keysHandler):
        if keysHandler[key.Z]:
            self.player.move(0,10)
        elif keysHandler[key.S]:
            self.player.move(0, -10)
        
        if keysHandler[key.Q]:
            self.player.move(-10, 0)
        elif keysHandler[key.D]:
            self.player.move(10, 0)
        
        self.map.setRelativePos( -self.player.x, -self.player.y)
    
    def on_mouse_motion(self,x,y,dx,dy):
        pass
#         self.cursor.x = x - self.cursor.width / 2
#         self.cursor.y = y - self.cursor.height / 2
        
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
        self.map = []
        self.xRelative = 0
        self.yRelative = 0
        self.tileSize = 48
        
    def setRelativePos(self, x, y):
        self.xRelative = x
        self.yRelative = y
        
    def load(self, filename):
        pass
    
    def render(self):
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glVertex2i( self.xRelative,self.yRelative )
        pyglet.gl.glVertex2i( self.xRelative ,self.yRelative + self.tileSize )
        pyglet.gl.glVertex2i( self.xRelative + self.tileSize, self.yRelative + self.tileSize )
        pyglet.gl.glVertex2i( self.xRelative + self.tileSize,self.yRelative )
        pyglet.gl.glEnd()
        
    