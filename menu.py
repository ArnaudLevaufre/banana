#-*- encoding: utf-8 -*-
import pyglet
import gameEngine

class Menu(object):
    def __init__(self):
        self._batch = pyglet.graphics.Batch()
        
    def on_mouse_press(self,x, y, button, modifiers):
        pass
            
    def on_mouse_motion(self,x, y, dx, dy):
        pass
            
            
class MainMenu(Menu):
    def __init__(self):
        """
        Créer le menu principal
        """
        
        super(MainMenu,self).__init__()
        self.principalMenuText = pyglet.text.Label("Menu principal",font_size=40, batch=self._batch,anchor_x ="center", anchor_y="top",x=gameEngine.GameEngine.W_WIDTH/2, y=gameEngine.GameEngine.W_HEIGHT-10, color=(255,255,255,255))
        # Texte
        self.playText = pyglet.text.Label("Jouer",font_size=30, batch=self._batch,anchor_x ="center", anchor_y="top",x=gameEngine.GameEngine.W_WIDTH/2, y=self.principalMenuText.y -80, color=(255,255,255,255))
        self.loadText = pyglet.text.Label("Charger une partie",font_size=30, batch=self._batch,anchor_x ="center", anchor_y="top",x=gameEngine.GameEngine.W_WIDTH/2, y=self.playText.y -50, color=(255,255,255,255))
        self.quitText = pyglet.text.Label("Quitter",font_size=30, batch=self._batch,anchor_x ="center", anchor_y="top",x=gameEngine.GameEngine.W_WIDTH/2, y=self.loadText.y -50, color=(255,255,255,255))      
        
        self.returnState = "menu"
        
    def render(self):
        self._batch.draw()
        return self.returnState
        
    def on_mouse_press(self,x, y, button, modifiers):
        if(button == pyglet.window.mouse.LEFT):
            if x > self.playText.x - 50 and x < self.playText.x + 50 and y > self.playText.y - 45 and y < self.playText.y - 8:
                self.returnState = "playing"
            elif x > self.quitText.x - 65 and x < self.quitText.x + 65 and y > self.quitText.y - 45 and y < self.quitText.y - 8:
                self.returnState = "quit"
        