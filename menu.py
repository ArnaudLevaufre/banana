#-*- encoding: utf-8 -*-
import pyglet
import gameEngine
import os


class MainMenu():
    def __init__(self):
        """
        Créer le menu principal
        """

        if os.path.isfile("data/save/save.data"):
            self.existingSave = True
        else:
            self.existingSave = False

        width, height = gameEngine.getDinamicWindowSize()

        self._batch = pyglet.graphics.Batch()
        self.principalMenuText = pyglet.text.Label("Menu principal", font_size=40, batch=self._batch, anchor_x="center", anchor_y="top", x=width / 2, y=height - 10, color=(255, 255, 255, 255))
        self.colors = [[[33, 33, 33], [77, 77, 77]], [[77, 77, 77], [33, 33, 33]]]
        self.bg = pyglet.sprite.Sprite(pyglet.image.load("data/sprites/fond.png"))

        self.newColor = 0
        self.continueColor = 0
        self.rapidColor = 0
        self.quitColor = 0
        self.editColor = 0

        # Texte
        self.newText = pyglet.text.Label("Nouvelle partie", font_size=20, batch=self._batch, anchor_x="center", anchor_y="top", x=width / 2, y=self.principalMenuText.y - 160, color=(255, 255, 255, 255))
        self.continueText = pyglet.text.Label("Continuer", font_size=20, batch=self._batch, anchor_x="center", anchor_y="top", x=width / 2, y=self.newText.y - 50, color=(255, 255, 255, 255))
        self.rapidText = pyglet.text.Label("Partie rapide", font_size=20, batch=self._batch, anchor_x="center", anchor_y="top", x=width / 2, y=self.continueText.y - 50, color=(255, 255, 255, 255))
        if not self.existingSave:
            self.rapidText.y = self.newText.y - 50
            self.continueText.text = ""
        self.editText = pyglet.text.Label("Editeur", font_size=20, batch=self._batch, anchor_x="center", anchor_y="top", x=width / 2, y=self.rapidText.y - 50, color=(255, 255, 255, 255))
        self.quitText = pyglet.text.Label("Quitter", font_size=20, batch=self._batch, anchor_x="center", anchor_y="top", x=width / 2, y=self.editText.y - 50, color=(255, 255, 255, 255))

        self.returnState = "menu"

    def render(self):
        width, height = gameEngine.getDinamicWindowSize()

        # - mise a jour des positions -
        self.principalMenuText.x, self.principalMenuText.y = width/2, height-10
        self.newText.x, self.newText.y = width/2, self.principalMenuText.y - 160
        self.continueText.x, self.continueText.y = width/2, self.newText.y - 50
        self.rapidText.x, self.rapidText.y = width / 2, self.continueText.y - 50
        if not self.existingSave:
            self.rapidText.y = self.newText.y - 50
        self.editText.x, self.editText.y = width/2, self.rapidText.y - 50
        self.quitText.x, self.quitText.y = width/2, self.editText.y - 50

        self.bg.y = height / 2 - self.bg.height / 2
        self.bg.x = width / 2 - self.bg.width / 2
        self.bg.draw()

        # - New -
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glColor3ub(self.colors[self.newColor][0][0], self.colors[self.newColor][0][1], self.colors[self.newColor][0][2])
        pyglet.gl.glVertex2i(self.newText.x - 180, self.newText.y - 37)
        pyglet.gl.glVertex2i(self.newText.x + 180, self.newText.y - 37)
        pyglet.gl.glColor3ub(self.colors[self.newColor][1][0], self.colors[self.newColor][1][1], self.colors[self.newColor][1][2])
        pyglet.gl.glVertex2i(self.newText.x + 180, self.newText.y + 1)
        pyglet.gl.glVertex2i(self.newText.x - 180, self.newText.y + 1)
        pyglet.gl.glEnd()

        # - Continue -
        if self.existingSave:
            pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
            pyglet.gl.glColor3ub(self.colors[self.continueColor][0][0], self.colors[self.continueColor][0][1], self.colors[self.continueColor][0][2])
            pyglet.gl.glVertex2i(self.continueText.x - 180, self.continueText.y - 37)
            pyglet.gl.glVertex2i(self.continueText.x + 180, self.continueText.y - 37)
            pyglet.gl.glColor3ub(self.colors[self.continueColor][1][0], self.colors[self.continueColor][1][1], self.colors[self.continueColor][1][2])
            pyglet.gl.glVertex2i(self.continueText.x + 180, self.continueText.y - 1)
            pyglet.gl.glVertex2i(self.continueText.x - 180, self.continueText.y - 1)
            pyglet.gl.glEnd()

        # - Rapid -
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glColor3ub(self.colors[self.rapidColor][0][0], self.colors[self.rapidColor][0][1], self.colors[self.rapidColor][0][2])
        pyglet.gl.glVertex2i(self.rapidText.x - 180, self.rapidText.y - 37)
        pyglet.gl.glVertex2i(self.rapidText.x + 180, self.rapidText.y - 37)
        pyglet.gl.glColor3ub(self.colors[self.rapidColor][1][0], self.colors[self.rapidColor][1][1], self.colors[self.rapidColor][1][2])
        pyglet.gl.glVertex2i(self.rapidText.x + 180, self.rapidText.y - 1)
        pyglet.gl.glVertex2i(self.rapidText.x - 180, self.rapidText.y - 1)
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
            if x > self.newText.x - 180 and x < self.newText.x + 180 and y > self.newText.y - 45 and y < self.newText.y - 8:
                self.returnState = "new"
            elif x > self.continueText.x - 180 and x < self.continueText.x + 180 and y > self.continueText.y - 45 and y < self.continueText.y - 8 and self.existingSave:
                self.returnState = "continue"
            elif x > self.rapidText.x - 180 and x < self.rapidText.x + 180 and y > self.rapidText.y - 45 and y < self.rapidText.y - 8:
                self.returnState = "rapid"
            elif x > self.editText.x - 180 and x < self.editText.x + 180 and y > self.editText.y - 45 and y < self.editText.y - 8:
                self.returnState = "creator"
            elif x > self.quitText.x - 180 and x < self.quitText.x + 180 and y > self.quitText.y - 45 and y < self.quitText.y - 8:
                self.returnState = "quit"

    def on_mouse_motion(self, x, y, dx, dy):
        if x > self.newText.x - 180 and x < self.newText.x + 180 and y > self.newText.y - 45 and y < self.newText.y - 8:
            self.newColor = 1
        else:
            self.newColor = 0

        if x > self.continueText.x - 180 and x < self.continueText.x + 180 and y > self.continueText.y - 45 and y < self.continueText.y - 8:
            self.continueColor = 1
        else:
            self.continueColor = 0

        if x > self.rapidText.x - 180 and x < self.rapidText.x + 180 and y > self.rapidText.y - 45 and y < self.rapidText.y - 8:
            self.rapidColor = 1
        else:
            self.rapidColor = 0

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
