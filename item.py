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
        
        self.type = itemType
        self.value = value
        if itemType == "chest":
            self.SIZE = 48
            self.sprite = pyglet.sprite.Sprite(pyglet.image.load("data/sprites/chest.png"))
        else:
            self.SIZE = 24
            self.sprite = pyglet.sprite.Sprite(pyglet.image.load("data/sprites/item.png"))

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

        self.sprite.x = self.x - self.SIZE/2
        self.sprite.y = self.y + 5 * decal - self.SIZE/2
        self.sprite.draw()
