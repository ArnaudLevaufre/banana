#-*- encoding: utf-8 -*-
import pyglet
import gameEngine


class MainMenu():
    def __init__(self):
        """
        Créer le menu principal
        """
        width, height = gameEngine.getDinamicWindowSize()

        self._batch = pyglet.graphics.Batch()
        self.principalMenuText = pyglet.text.Label("Menu principal", font_size=40, batch=self._batch, anchor_x="center", anchor_y="top", x=width / 2, y=height - 10, color=(255, 255, 255, 255))
        self.colors = [[[33, 33, 33], [77, 77, 77]], [[77, 77, 77], [33, 33, 33]]]
        self.bg = pyglet.sprite.Sprite(pyglet.image.load("data/sprites/fond.png"))

        self.playColor = 0
        self.loadColor = 0
        self.quitColor = 0
        self.editColor = 0

        # Texte
        self.playText = pyglet.text.Label("Jouer", font_size=20, batch=self._batch, anchor_x="center", anchor_y="top", x=width / 2, y=self.principalMenuText.y - 160, color=(255, 255, 255, 255))
        self.loadText = pyglet.text.Label("Charger une partie", font_size=20, batch=self._batch, anchor_x="center", anchor_y="top", x=width / 2, y=self.playText.y - 50, color=(255, 255, 255, 255))
        self.editText = pyglet.text.Label("Editeur", font_size=20, batch=self._batch, anchor_x="center", anchor_y="top", x=width / 2, y=self.loadText.y - 50, color=(255, 255, 255, 255))
        self.quitText = pyglet.text.Label("Quitter", font_size=20, batch=self._batch, anchor_x="center", anchor_y="top", x=width / 2, y=self.editText.y - 50, color=(255, 255, 255, 255))

        self.returnState = "menu"

    def render(self):
        width, height = gameEngine.getDinamicWindowSize()

        # - mise a jour des psitions -
        self.principalMenuText.x, self.principalMenuText.y = width/2, height-10
        self.playText.x, self.playText.y = width/2, self.principalMenuText.y - 160
        self.loadText.x, self.loadText.y = width/2, self.playText.y - 50
        self.editText.x, self.editText.y = width/2, self.loadText.y - 50
        self.quitText.x, self.quitText.y = width/2, self.editText.y - 50

        self.bg.y = height / 2 - self.bg.height / 2
        self.bg.x = width / 2 - self.bg.width / 2
        self.bg.draw()

        # - Jouer -
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glColor3ub(self.colors[self.playColor][0][0], self.colors[self.playColor][0][1], self.colors[self.playColor][0][2])
        pyglet.gl.glVertex2i(self.playText.x - 180, self.playText.y - 37)
        pyglet.gl.glVertex2i(self.playText.x + 180, self.playText.y - 37)
        pyglet.gl.glColor3ub(self.colors[self.playColor][1][0], self.colors[self.playColor][1][1], self.colors[self.playColor][1][2])
        pyglet.gl.glVertex2i(self.playText.x + 180, self.playText.y + 1)
        pyglet.gl.glVertex2i(self.playText.x - 180, self.playText.y + 1)
        pyglet.gl.glEnd()

        # - Charger -
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glColor3ub(self.colors[self.loadColor][0][0], self.colors[self.loadColor][0][1], self.colors[self.loadColor][0][2])
        pyglet.gl.glVertex2i(self.loadText.x - 180, self.loadText.y - 37)
        pyglet.gl.glVertex2i(self.loadText.x + 180, self.loadText.y - 37)
        pyglet.gl.glColor3ub(self.colors[self.loadColor][1][0], self.colors[self.loadColor][1][1], self.colors[self.loadColor][1][2])
        pyglet.gl.glVertex2i(self.loadText.x + 180, self.loadText.y - 1)
        pyglet.gl.glVertex2i(self.loadText.x - 180, self.loadText.y - 1)
        pyglet.gl.glEnd()

        # - Edit -
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glColor3ub(self.colors[self.editColor][0][0], self.colors[self.editColor][0][1], self.colors[self.editColor][0][2])
        pyglet.gl.glVertex2i(self.editText.x - 180, self.editText.y - 37)
        pyglet.gl.glVertex2i(self.editText.x + 180, self.editText.y - 37)
        pyglet.gl.glColor3ub(self.colors[self.editColor][1][0], self.colors[self.editColor][1][1], self.colors[self.editColor][1][2])
        pyglet.gl.glVertex2i(self.editText.x + 180, self.editText.y - 1)
        pyglet.gl.glVertex2i(self.editText.x - 180, self.editText.y - 1)
        pyglet.gl.glEnd()

        #-Quitter
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glColor3ub(self.colors[self.quitColor][0][0], self.colors[self.quitColor][0][1], self.colors[self.quitColor][0][2])
        pyglet.gl.glVertex2i(self.quitText.x - 180, self.quitText.y - 37)
        pyglet.gl.glVertex2i(self.quitText.x + 180, self.quitText.y - 37)
        pyglet.gl.glColor3ub(self.colors[self.quitColor][1][0], self.colors[self.quitColor][1][1], self.colors[self.quitColor][1][2])
        pyglet.gl.glVertex2i(self.quitText.x + 180, self.quitText.y - 1)
        pyglet.gl.glVertex2i(self.quitText.x - 180, self.quitText.y - 1)
        pyglet.gl.glEnd()

        self._batch.draw()

        return self.returnState

    def on_mouse_press(self, x, y, button, modifiers):
        if(button == pyglet.window.mouse.LEFT):
            if x > self.playText.x - 180 and x < self.playText.x + 180 and y > self.playText.y - 45 and y < self.playText.y - 8:
                self.returnState = "playing"
            elif x > self.loadText.x - 180 and x < self.loadText.x + 180 and y > self.loadText.y - 45 and y < self.loadText.y - 8:
                self.returnState = "playing"
            elif x > self.editText.x - 180 and x < self.editText.x + 180 and y > self.editText.y - 45 and y < self.editText.y - 8:
                self.returnState = "creator"
            elif x > self.quitText.x - 180 and x < self.quitText.x + 180 and y > self.quitText.y - 45 and y < self.quitText.y - 8:
                self.returnState = "quit"

    def on_mouse_motion(self, x, y, dx, dy):
        if x > self.playText.x - 180 and x < self.playText.x + 180 and y > self.playText.y - 45 and y < self.playText.y - 8:
            self.playColor = 1
        else:
            self.playColor = 0

        if x > self.loadText.x - 180 and x < self.loadText.x + 180 and y > self.loadText.y - 45 and y < self.loadText.y - 8:
            self.loadColor = 1
        else:
            self.loadColor = 0
        
        if x > self.editText.x - 180 and x < self.editText.x + 180 and y > self.editText.y - 45 and y < self.editText.y - 8:
            self.editColor = 1
        else:
            self.editColor = 0
        
        if x > self.quitText.x - 180 and x < self.quitText.x + 180 and y > self.quitText.y - 45 and y < self.quitText.y - 8:
            self.quitColor = 1
        else:
            self.quitColor = 0

    def setDefault(self):
        self.returnState = "menu"