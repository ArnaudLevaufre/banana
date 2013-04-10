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
        self.speed = 30
        
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load("sprites/blarg.png").get_texture())
        self.sprite.x = gameEngine.GameEngine.W_WIDTH/2 - self.sprite.width/2
        self.sprite.y = gameEngine.GameEngine.W_HEIGHT/2 - self.sprite.height/2
        
    def move(self, x,y, gameMap ,dt):
        if not gameMap.colide( self.x - self.width/2 + x * dt * self.speed, self.y - self.height/2 + y * dt * self.speed, self.width, self.height):
            self.x += x * dt * self.speed
            self.y += y * dt * self.speed
            
    def render(self):
        self.sprite.draw()
        
class Npc(object):
    def __init__(self,x,y):
        super(Npc, self).__init__(x,y)
        
        
    def move(self, map):
        pass
    
    def render(self):
        pass
    
    def kill(self):
        pass
    
        
