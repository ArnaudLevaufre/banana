import time, math
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
        self.mainBatch = pyglet.graphics.Batch()
        image = pyglet.image.load('sprites/vis.png')
        print image
        self.cursor = pyglet.sprite.Sprite(image, gameEngine.GameEngine.W_WIDTH/2, gameEngine.GameEngine.W_HEIGHT/2, batch = self.mainBatch)
        self.player = entity.Player(200,200)
        self.camera = Camera()
        
    def simulate(self, dt, keysHandler):
        if keysHandler[key.Z]:
            self.player.move(0,10)
        elif keysHandler[key.S]:
            self.player.move(0, -10)
        
        if keysHandler[key.Q]:
            self.player.move(-10, 0)
        elif keysHandler[key.D]:
            self.player.move(10, 0)
        
        # on update la camera
        self.camera.moveTo(gameEngine.GameEngine.W_WIDTH/2 - self.player.x, gameEngine.GameEngine.W_HEIGHT/2 - self.player.y )

    
    def on_mouse_motion(self,x,y,dx,dy):
        print x,y
        print self.cursor.x
        self.cursor.x = x
        self.cursor.y = y
    def render(self):
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glVertex2i( self.player.x,self.player.y )
        pyglet.gl.glVertex2i( self.player.x,self.player.y + 10 )
        pyglet.gl.glVertex2i( self.player.x + 10,self.player.y + 10 )
        pyglet.gl.glVertex2i( self.player.x + 10,self.player.y )
        pyglet.gl.glEnd()
        self.mainBatch.draw()
        
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def moveTo(self, x, y):
        self.x = int(x)
        self.y = int(y)       
        pyglet.gl.glViewport(self.x,self.y, gameEngine.GameEngine.W_WIDTH , gameEngine.GameEngine.W_HEIGHT)
        
    def reset(self):
        self.move(0, 0)