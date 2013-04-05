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
        
    def move(self, x,y,dt):
        # il faut d'abord check si il peut bouger
        self.x += x * dt * 100
        self.y += y * dt * 100