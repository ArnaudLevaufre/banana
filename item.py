import pyglet
import math
import time


class Item(object):
    def __init__(self, x, y, itemType, value):
        self.x = x
        self.y = y
        self.SIZE = 24
        self.type = itemType
        self.value = value

    def collide(self, ent):
        """
                        == COLlIDE ==

        Voir gameMap.collide() pour les explications

        :param ent: player avec lequel check les collisions
        :type ent: Player
        """
        # One does not simply understand what's written there
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

        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glVertex2d(self.x - self.SIZE / 2, self.y - self.SIZE / 2 + 5 * decal)
        pyglet.gl.glVertex2d(self.x - self.SIZE / 2 + self.SIZE, self.y - self.SIZE / 2 + 5 * decal)
        pyglet.gl.glVertex2d(self.x - self.SIZE / 2 + self.SIZE, self.y - self.SIZE / 2 + self.SIZE + 5 * decal)
        pyglet.gl.glVertex2d(self.x - self.SIZE / 2, self.y - self.SIZE / 2 + self.SIZE + 5 * decal)
        pyglet.gl.glEnd()
