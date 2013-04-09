import pyglet
import gameEngine

class Entity():
    def __init__(self, x=0, y=0, xVel=0, yVel=0):
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
    
    def simulate(self, dt=1):
        if self.xVel != 0:
            self.x += self.xVel * dt
        if self.yVel != 0:
            self.y += self.yVel * dt
            
class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x=0, y=0, xVel=0, yVel=0)
        self.hp = 100
        self.width = 48
        self.height = 48
        
        self.texture = pyglet.image.load("sprites/blarg.png").get_texture()

    def move(self, x,y, gameMap ,dt):
        if not gameMap.colide( self.x - (self.width - 20)/2 + x * dt * 50, self.y - self.height/2 + y * dt * 50, self.width - 20, self.height):
            self.x += x * dt * 50
            self.y += y * dt * 50
            
    def render(self):
        w = gameEngine.GameEngine.W_WIDTH
        h = gameEngine.GameEngine.W_HEIGHT
        
        # voir la vraie taille!
#        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
#        pyglet.gl.glVertex2i( w/2 - self.width/2, h/2 - self.width/2 )
#        pyglet.gl.glVertex2i( w/2 + self.width/2, h/2 - self.width/2 )
#        pyglet.gl.glVertex2i( w/2 + self.width/2, h/2 + self.width/2 )
#        pyglet.gl.glVertex2i( w/2 - self.width/2, h/2 + self.width/2 )
#        pyglet.gl.glEnd()
        
        pyglet.gl.glEnable(pyglet.gl.GL_TEXTURE_2D)
        pyglet.gl.glBindTexture(self.texture.target, self.texture.id)
        
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glTexCoord2i(0,0)
        pyglet.gl.glVertex2i( w/2 - self.width/2, h/2 - self.width/2 )
        pyglet.gl.glTexCoord2i(1,0)
        pyglet.gl.glVertex2i( w/2 + self.width/2, h/2 - self.width/2 )
        pyglet.gl.glTexCoord2i(1,1)
        pyglet.gl.glVertex2i( w/2 + self.width/2, h/2 + self.width/2 )
        pyglet.gl.glTexCoord2i(0,1)
        pyglet.gl.glVertex2i( w/2 - self.width/2, h/2 + self.width/2 )
        pyglet.gl.glEnd()
        
                
        pyglet.gl.glDisable(pyglet.gl.GL_TEXTURE_2D)
        
class Npc(object):
    def __init__(self,x,y):
        super(Npc, self).__init__(x,y)
        
        
    def move(self, map):
        pass
    
    def render(self):
        pass
    
    def kill(self):
        pass
    
        