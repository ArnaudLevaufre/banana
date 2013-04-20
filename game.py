#-*- encoding: utf-8 -*-
import pyglet, pyglet.window.key as key, os, xml.etree.ElementTree as xml
import gameEngine, entity, ui, map, level
import math

# ---------------------------------------------------

class Game:
    def __init__(self):

        self.camera = Camera()
        self.ui = ui.UI()
        self.level = level.Level()
        self.level.load("001")
        self.map = self.level.map
        self.player = self.level.player
        
        self.bullets = []
        self.cinematiqueIsPlaying = True
        
    def simulate(self, dt, keysHandler):
        if self.cinematiqueIsPlaying == False:
            if keysHandler[key.Z]:
                self.player.move(0,10, self.map,dt)
            elif keysHandler[key.S]:
                self.player.move(0, -10, self.map, dt)
            
            if keysHandler[key.Q]:
                self.player.move(-10, 0, self.map,dt)
            elif keysHandler[key.D]:
                self.player.move(10, 0, self.map,dt)
                
            if keysHandler[key.TAB]:
                self.ui.toggleMenu(True)
            else:
                self.ui.toggleMenu(False)
            
            # tir du joueur
            self.player.shoot(self.bullets)
            
            for bullet in self.bullets:
                if bullet.simulate(self.map, dt) == False:
                    self.bullets.remove(bullet)
                    
            # on repositionne la carte.
            self.camera.setPos(self.player.x, self.player.y)
        
    def on_mouse_press(self,x, y, button, modifiers):
        if(button == pyglet.window.mouse.LEFT):
            self.player.isFiring = True
            self.player.aim(x,y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.player.isFiring = False
            
    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        if(buttons == pyglet.window.mouse.LEFT):
            self.player.aim(x,y)
            
    def render(self):
        if self.cinematiqueIsPlaying == False:
            self.map.render()    
            self.ui.render(self.camera.x, self.camera.y, self.player)
            self.player.render()
    #         print "[BULLETS] <", len(self.bullets), ">"
    
            for bullet in self.bullets:
                if self.player.x - gameEngine.GameEngine.W_WIDTH/2 < bullet.x < self.player.x + gameEngine.GameEngine.W_WIDTH/2 and self.player.y - gameEngine.GameEngine.W_HEIGHT/2 < bullet.y < self.player.y + gameEngine.GameEngine.W_WIDTH/2:
                    pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
                    pyglet.gl.glVertex2d(bullet.x - bullet.SIZE/2 ,bullet.y - bullet.SIZE/2)
                    pyglet.gl.glVertex2d(bullet.x - bullet.SIZE/2 + entity.Bullet.SIZE ,bullet.y - bullet.SIZE/2)
                    pyglet.gl.glVertex2d(bullet.x - bullet.SIZE/2 + entity.Bullet.SIZE, bullet.y - bullet.SIZE/2 + entity.Bullet.SIZE)
                    pyglet.gl.glVertex2d(bullet.x - bullet.SIZE/2 ,bullet.y - bullet.SIZE/2 + entity.Bullet.SIZE)
                    pyglet.gl.glEnd()
                else:
                    self.bullets.remove(bullet)
        else:
            self.cinematiqueIsPlaying = self.level.cinematique.run()
# ---------------------------------------------------
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def setPos(self, x, y):
        self.x = x
        self.y = y
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glOrtho(x - gameEngine.GameEngine.W_WIDTH/2, x + gameEngine.GameEngine.W_WIDTH/2, y - gameEngine.GameEngine.W_HEIGHT/2, y + gameEngine.GameEngine.W_HEIGHT/2, -1, 1)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    


        
