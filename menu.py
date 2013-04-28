#-*- encoding: utf-8 -*-
import pyglet
import gameEngine

class MainMenu():
    def __init__(self):
        """
        Créer le menu principal
        """
        
        self._batch = pyglet.graphics.Batch()
        self.principalMenuText = pyglet.text.Label("Menu principal",font_size=40, batch=self._batch,anchor_x ="center", anchor_y="top",x=gameEngine.GameEngine.W_WIDTH/2, y=gameEngine.GameEngine.W_HEIGHT-10, color=(255,255,255,255))
       
        # Texte

        self.playText = pyglet.text.Label("Jouer",font_size=20, batch=self._batch,anchor_x ="center", anchor_y="top",x=gameEngine.GameEngine.W_WIDTH/2, y=self.principalMenuText.y -80, color=(255,255,255,255))
       
        self.loadText = pyglet.text.Label("Charger une partie",font_size=20, batch=self._batch,anchor_x ="center", anchor_y="top",x=gameEngine.GameEngine.W_WIDTH/2, y=self.playText.y -50, color=(255,255,255,255))
       
        self.quitText = pyglet.text.Label("Quitter",font_size=20, batch=self._batch,anchor_x ="center", anchor_y="top",x=gameEngine.GameEngine.W_WIDTH/2, y=self.loadText.y -50, color=(255,255,255,255))      
        
        self.returnState = "menu"
        
    def render(self):
        # - Jouer -
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glColor3ub(33,33,33)
        pyglet.gl.glVertex2i(self.playText.x-180, self.playText.y-32)  
        pyglet.gl.glColor3ub(33,33,33)     
        pyglet.gl.glVertex2i(self.playText.x+180,self.playText.y-32)
        pyglet.gl.glColor3ub(77,77,77)
        pyglet.gl.glVertex2i(self.playText.x+180,self.playText.y - 4 )
        pyglet.gl.glColor3ub(77,77,77)
        pyglet.gl.glVertex2i(self.playText.x-180,self.playText.y - 4)
        pyglet.gl.glEnd()
        # - Charger -
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glColor3ub(33,33,33)
        pyglet.gl.glVertex2i(self.loadText.x-180, self.loadText.y-32)  
        pyglet.gl.glColor3ub(33,33,33)     
        pyglet.gl.glVertex2i(self.loadText.x+180,self.loadText.y-32)
        pyglet.gl.glColor3ub(77,77,77)
        pyglet.gl.glVertex2i(self.loadText.x+180,self.loadText.y -4)
        pyglet.gl.glColor3ub(77,77,77)
        pyglet.gl.glVertex2i(self.loadText.x-180,self.loadText.y-4)
        pyglet.gl.glEnd()
        #-Quitter
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glColor3ub(33,33,33)
        pyglet.gl.glVertex2i(self.quitText.x-180, self.quitText.y-32)  
        pyglet.gl.glColor3ub(33,33,33)     
        pyglet.gl.glVertex2i(self.quitText.x+180,self.quitText.y-32)
        pyglet.gl.glColor3ub(77,77,77)
        pyglet.gl.glVertex2i(self.quitText.x+180,self.quitText.y -4)
        pyglet.gl.glColor3ub(77,77,77)
        pyglet.gl.glVertex2i(self.quitText.x-180,self.quitText.y-4)
        pyglet.gl.glEnd()
        self._batch.draw()

        return self.returnState
        
    def on_mouse_press(self,x, y, button, modifiers):
        if(button == pyglet.window.mouse.LEFT):
            if x > self.playText.x - 180 and x < self.playText.x + 180 and y > self.playText.y - 45 and y < self.playText.y - 8:
                self.returnState = "playing"
            if x > self.loadText.x - 180 and x < self.loadText.x + 180 and y > self.loadText.y - 45 and y < self.loadText.y - 8:
                self.returnState = "playing"
            elif x > self.quitText.x - 180 and x < self.quitText.x + 180 and y > self.quitText.y - 45 and y < self.quitText.y - 8:
                self.returnState = "quit"
    
    def on_mouse_motion(self,x, y, dx, dy):
        pass