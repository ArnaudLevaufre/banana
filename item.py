#-*- encoding:utf-8 -*-

import pyglet
import math
import time


class Item(object):
    
    def __init__(self, x, y, itemType, value):
        """
        Constructeur des objects de type items
        
        :param x: position en x de l'item
        :param y: position en y de l'item
        :param itemType: le type d'item (hp, shield etc...)
        :param value: la quantitée de bonus donnée.
        
        :type x: int
        :type y: int
        :type itemType: str
        :type value: float
        """
        
        self.x = x
        self.y = y
        self.SIZE = 24
        self.type = itemType
        self.value = value

    def collide(self, ent):
        """
        Voir entity.Bullets.collide()

        :param ent: player avec lequel check les collisions
        :type ent: Player
        """
        
        if self.x <= ent.x <= self.x + self.SIZE or self.x <= ent.x + ent.width <= self.x + self.SIZE:
            if self.y <= ent.y <= self.y + self.SIZE or self.y <= ent.y + ent.height <= self.y + self.SIZE:
                return True
            elif ent.y <= self.y <= ent.y + ent.height or ent.y <= self.y + self.SIZE <= ent.y + ent.height:
                return True

        elif ent.x <= self.x <= ent.x + ent.width or ent.x <= self.x + self.SIZE <= ent.x + ent.width:
            if (self.y <= ent.y <= self.y + self.SIZE) or (self.y <= ent.y + ent.height <= self.y + self.SIZE):
                return True
            elif ent.y <= self.y <= ent.y + ent.height or ent.y <= self.y + self.SIZE <= ent.y + ent.height:
                return True

        return False

    def render(self):
        if self.type == "chest":
            decal = 0
        else:
            decal = math.sin(5 * time.time())

        # Pour l'instant nous n'affichons qu'on carré.
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glVertex2d(self.x - self.SIZE / 2, self.y - self.SIZE / 2 + 5 * decal)
        pyglet.gl.glVertex2d(self.x - self.SIZE / 2 + self.SIZE, self.y - self.SIZE / 2 + 5 * decal)
        pyglet.gl.glVertex2d(self.x - self.SIZE / 2 + self.SIZE, self.y - self.SIZE / 2 + self.SIZE + 5 * decal)
        pyglet.gl.glVertex2d(self.x - self.SIZE / 2, self.y - self.SIZE / 2 + self.SIZE + 5 * decal)
        pyglet.gl.glEnd()
