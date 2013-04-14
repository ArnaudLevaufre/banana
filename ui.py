#-*- encoding:utf-8 -*-

import pyglet
import gameEngine

class UI(object):
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.menuOpened = False
        
        # Proprietees de l'interface
        self.hpPos = {"x":5, "y":5}
        self.hpSize = {"x":150, "y":20}
        self.whiteSpacing = 4
        self.shieldPos = {"x":5, "y":30}
        self.shieldSize = {"x":150,"y":20}
        self.sidePanelWidth = 160
        self.sidePanelHeight = 400
        
        # Labels
        self.hpLabel = pyglet.text.Label("100 / 100", batch=self.batch, anchor_x="right", anchor_y="center", bold=True, font_size=8)
        self.shieldLabel = pyglet.text.Label("50 / 50", batch=self.batch, anchor_x="right", anchor_y="center", bold=True, font_size=8 )
        
    def toggleMenu(self, state):
        self.menuOpened = state

    def render(self,x,y, player):
        # Barre de vie
        originX = int(x - gameEngine.GameEngine.W_WIDTH/2)
        originY = int(y - gameEngine.GameEngine.W_HEIGHT/2)
        
        self.drawBar(originX + self.hpPos["x"], originY + self.hpPos["y"], self.hpSize["x"], self.hpSize["y"], (1,0,0), 3, player.hp/player.maxHp)
        if int(player.shield) > 0:
            self.drawBar(originX + 5, originY + self.shieldPos["y"], self.shieldSize["x"], self.shieldSize["y"], (0.10,0.5,1), 3, player.shield/player.shieldCapacity)
        
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
        
        # redéfinition des positions du texte
        self.hpLabel.x, self.hpLabel.y = originX + self.hpPos["x"] + self.hpSize["x"] - 6, originY + self.hpPos["y"] + self.hpSize["y"]/2
        self.shieldLabel.x, self.shieldLabel.y = originX + self.shieldPos["x"] + self.shieldSize["x"] - 6, originY + self.shieldPos["y"] + self.shieldSize["y"]/2
        self.hpLabel.text = str(int(player.hp)) + " / " + str(int(player.maxHp))
        
        if int(player.shield) > 0:
            self.shieldLabel.text = str(int(player.shield)) + " / " + str(int(player.shieldCapacity))
        else:
            self.shieldLabel.text = ""
        
        self.batch.draw()
        
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