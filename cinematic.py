import pyglet
import gameEngine

class Cinematic:
    def __init__(self):
        self.lastOnDrawTime = 0
        self.dt = 1
        self.W_HEIGHT = gameEngine.GameEngine.W_HEIGHT
        self.W_WIDTH = gameEngine.GameEngine.W_WIDTH
        self.mainDrawingBatch = pyglet.graphics.Batch()
        self.borderTop = Border("top")
        self.borderBot = Border("bot")
        self.borderTop.batch = self.mainDrawingBatch
        self.borderBot.batch = self.mainDrawingBatch
         
            
    def run(self, dt):
        self.borderTop.animate(self.dt)
        self.borderBot.animate(self.dt)
        self.dt = dt
        self.mainDrawingBatch.draw()
        
class Border(pyglet.sprite.Sprite):
    def __init__(self, pos):  
        self.W_HEIGHT = gameEngine.GameEngine.W_HEIGHT
        self.W_WIDTH = gameEngine.GameEngine.W_WIDTH
        super(Border, self).__init__(pyglet.image.create(self.W_WIDTH, self.W_HEIGHT/4, pyglet.image.SolidColorImagePattern((0,0,0,255))))
        self.pos = pos
        if(pos == "bot"):
            self.y = -2*self.W_HEIGHT/4
        elif(pos == "top"):
            self.y = self.W_HEIGHT + self.height
            
    def animate(self,dt):
        if(self.pos == "bot"):
            if(self.y < self.W_HEIGHT/4 - self.height):
                self.y += 20 * dt
        elif(self.pos == "top"):
            if(self.y > self.W_HEIGHT - self.height +2):
                self.y -= 20 * dt