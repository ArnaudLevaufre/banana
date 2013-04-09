import pyglet
import gameEngine

class Entity(object):
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
    def move(self, x,y, gameMap ,dt):
        if not gameMap.colide(self.x - self.width/2 + x * dt * 50, self.y - self.height/2 + y * dt * 50, self.width, self.height):
            self.x += x * dt * 50
            self.y += y * dt * 50
    def render(self):
        w = gameEngine.GameEngine.W_WIDTH
        h = gameEngine.GameEngine.W_HEIGHT
        
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glVertex2i( w/2 - self.width/2, h/2 - self.width/2 )
        pyglet.gl.glVertex2i( w/2 + self.width/2, h/2 - self.width/2 )
        pyglet.gl.glVertex2i( w/2 + self.width/2, h/2 + self.width/2 )
        pyglet.gl.glVertex2i( w/2 - self.width/2, h/2 + self.width/2 )
        pyglet.gl.glEnd()