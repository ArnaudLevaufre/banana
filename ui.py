import pyglet
import gameEngine

class UI(object):
    def __init__(self):
        self.hpTexture = pyglet.image.load("sprites/hp.png").get_texture()
        self.shieldTexture = pyglet.image.load("sprites/shield.png").get_texture()
    
    def render(self,x,y, player):
        # Barre de vie
        pyglet.gl.glEnable(pyglet.gl.GL_TEXTURE_2D)
        pyglet.gl.glBindTexture(self.hpTexture.target, self.hpTexture.id)
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        
        pyglet.gl.glTexCoord2i(0,1)
        pyglet.gl.glVertex2i(x-gameEngine.GameEngine.W_WIDTH/2,y+16-gameEngine.GameEngine.W_HEIGHT/2)
        pyglet.gl.glTexCoord2i(1,1)
        pyglet.gl.glVertex2i(x-gameEngine.GameEngine.W_WIDTH/2+int(player.hp)*2,y+16-gameEngine.GameEngine.W_HEIGHT/2)
        pyglet.gl.glTexCoord2i(1,0)
        pyglet.gl.glVertex2i(x-gameEngine.GameEngine.W_WIDTH/2+int(player.hp)*2,y-gameEngine.GameEngine.W_HEIGHT/2)
        pyglet.gl.glTexCoord2i(0,0)
        pyglet.gl.glVertex2i(x-gameEngine.GameEngine.W_WIDTH/2,y-gameEngine.GameEngine.W_HEIGHT/2)

        pyglet.gl.glDisable(pyglet.gl.GL_TEXTURE_2D)
        pyglet.gl.glEnd()
        # -----------------------------------------------------------------------------------------------------
        # Barre bouclier
        pyglet.gl.glEnable(pyglet.gl.GL_TEXTURE_2D)
        pyglet.gl.glBindTexture(self.shieldTexture.target, self.shieldTexture.id)
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        
        pyglet.gl.glTexCoord2i(0,1)
        pyglet.gl.glVertex2i(x-gameEngine.GameEngine.W_WIDTH/2,y+33-gameEngine.GameEngine.W_HEIGHT/2)
        pyglet.gl.glTexCoord2i(1,1)
        pyglet.gl.glVertex2i(x-gameEngine.GameEngine.W_WIDTH/2+int(player.shield)*2,y+33-gameEngine.GameEngine.W_HEIGHT/2)
        pyglet.gl.glTexCoord2i(1,0)
        pyglet.gl.glVertex2i(x-gameEngine.GameEngine.W_WIDTH/2+int(player.shield)*2,y-gameEngine.GameEngine.W_HEIGHT/2+17)
        pyglet.gl.glTexCoord2i(0,0)
        pyglet.gl.glVertex2i(x-gameEngine.GameEngine.W_WIDTH/2,y-gameEngine.GameEngine.W_HEIGHT/2+17)

        pyglet.gl.glDisable(pyglet.gl.GL_TEXTURE_2D)
        pyglet.gl.glEnd()