import pyglet
import math
class Item(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y 

    def render(self):
        pass
    
class Shield(Item):
    def __init__(self, x, y):
        # - Objets -
        super(Shield,self ).__init__(x,y)

        # - Constantes -
        self.type = "shield"
        self.value = 50
        self.SIZE = 48
        
        # - Divers -
        self.tick = 0
    def render(self):
        self.tick +=1
        
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glVertex2d(self.x - self.SIZE/2 ,self.y - self.SIZE/2 + math.cos(0.2*self.tick))
        pyglet.gl.glVertex2d(self.x - self.SIZE/2 + self.SIZE ,self.y - self.SIZE/2+ math.cos(0.2*self.tick))
        pyglet.gl.glVertex2d(self.x - self.SIZE/2 + self.SIZE, self.y - self.SIZE/2 + self.SIZE+ math.cos(0.2*self.tick))
        pyglet.gl.glVertex2d(self.x - self.SIZE/2 ,self.y - self.SIZE/2 + self.SIZE+ math.cos(0.2*self.tick))
        pyglet.gl.glEnd()