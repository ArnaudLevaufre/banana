import pyglet
import gameEngine

class UI(object):
    def __init__(self):
        self.hpTexture = pyglet.image.load("sprites/hp.png").get_texture()
        self.shieldTexture = pyglet.image.load("sprites/shield.png").get_texture()
        self.menuOpened = False
        
        # Proprietees de l'interface
        self.hpSize = {"x":150, "y":20}
        self.whiteSpacing = 4
        self.shieldSize = [150,30]
        self.sidePanelWidth = 160
        self.sidePanelHeight = 400
        
    def toggleMenu(self, state):
        self.menuOpened = state
        
    def render(self,x,y, player):
        # Barre de vie
        originX = int(x - gameEngine.GameEngine.W_WIDTH/2)
        originY = int(y - gameEngine.GameEngine.W_HEIGHT/2)
        
        self.drawBar(originX + 10, originY + 10, self.hpSize["x"], self.hpSize["y"], (1,0,0), 3, player.hp/player.maxHp)
        self.drawBar(originX + 10, originY + self.hpSize["y"] + 12, self.hpSize["x"], self.hpSize["y"], (0.10,0.5,1), 3, player.shield/player.shieldCapacity)
        
        if self.menuOpened == True:

            pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
            pyglet.gl.glColor4f(0,0,0,0.33)
            pyglet.gl.glVertex2i(originX, y - self.sidePanelHeight/2)
            pyglet.gl.glVertex2i(originX + self.sidePanelWidth,y - self.sidePanelHeight/2 )
            pyglet.gl.glVertex2i(originX + self.sidePanelWidth,y + self.sidePanelHeight/2)
            pyglet.gl.glVertex2i(originX, y + self.sidePanelHeight/2)
            pyglet.gl.glEnd()

            pyglet.gl.glBegin(pyglet.gl.GL_LINE_STRIP)
            pyglet.gl.glColor4f(0,0,0,1)
            pyglet.gl.glVertex2i(originX, y - self.sidePanelHeight/2)
            pyglet.gl.glVertex2i(originX + self.sidePanelWidth,y - self.sidePanelHeight/2 )
            pyglet.gl.glVertex2i(originX + self.sidePanelWidth,y + self.sidePanelHeight/2)
            pyglet.gl.glVertex2i(originX, y + self.sidePanelHeight/2)
            pyglet.gl.glEnd()
            
    def drawBar(self,x,y, width, height, color, border, progress):

        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
    
        if border:
            pyglet.gl.glColor3f(0,0,0)
            pyglet.gl.glVertex2i(x, y)
            pyglet.gl.glVertex2i(x + width, y)
            pyglet.gl.glVertex2i(x + width, y + height)
            pyglet.gl.glVertex2i(x, y + height)
            
            pyglet.gl.glColor3f(1,1,1)
            pyglet.gl.glVertex2i(x + 1, y + 1)
            pyglet.gl.glVertex2i(x + width - 1 , y + 1)
            pyglet.gl.glVertex2i(x + width - 1 , y + height - 1)
            pyglet.gl.glVertex2i(x + 1, y + height - 1)
            
            pyglet.gl.glColor3f(0,0,0)
            pyglet.gl.glVertex2i(x + border, y + border)
            pyglet.gl.glVertex2i(x + width - border, y + border)
            pyglet.gl.glVertex2i(x + width - border, y + height - border)
            pyglet.gl.glVertex2i(x + border, y + height- border)
    
            pyglet.gl.glColor3f(color[0], color[1], color[2])
            pyglet.gl.glVertex2i(x + border + 1, y + border + 1)
            pyglet.gl.glVertex2i(x + border + 1 + int((width - border*2 - 2) * progress) , y + border + 1)
            pyglet.gl.glVertex2i(x + border + 1 + int((width - border*2 - 2) * progress), y + height - border - 1)
            pyglet.gl.glVertex2i(x + border + 1, y + height - border - 1)

        else:
            pyglet.gl.glColor3f(color[0], color[1], color[2])
            pyglet.gl.glVertex2i(x, y)
            pyglet.gl.glVertex2i(x + int((width - border*2 - 2) * progress) , y )
            pyglet.gl.glVertex2i(x + int((width - border*2 - 2) * progress), y + height)
            pyglet.gl.glVertex2i(x, y + height)
        
        pyglet.gl.glEnd()