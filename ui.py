#-*- encoding:utf-8 -*-

import pyglet
import gameEngine


class UI(object):
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.batchPanel = pyglet.graphics.Batch()
        self.menuOpened = False
        self.showDevTool = True

        # Proprietees de l'interface
        self.hpPos = {"x": 5, "y": 5}
        self.hpSize = {"x": 150, "y": 20}
        self.whiteSpacing = 4
        self.shieldPos = {"x": 5,  "y": 30}
        self.shieldSize = {"x": 150, "y": 20}
        self.sidePanelWidth = 160
        self.sidePanelHeight = 400

        # Labels
        self.hpLabel = pyglet.text.Label("100 / 100", x=0, y=0, batch=self.batch, anchor_x="right", anchor_y="center", bold=True, font_size=8)
        self.shieldLabel = pyglet.text.Label("50 / 50", x=0, y=0, batch=self.batch, anchor_x="right", anchor_y="center", bold=True, font_size=8)

        self.fpsShadow = pyglet.text.Label("", x=0, y=0, anchor_y="top", bold=True, color=(0, 0, 0, 255))
        self.fps = pyglet.text.Label("", x=0, y=0, anchor_y="top", bold=True)

        self.panelTitle = pyglet.text.Label("= INFOS =", anchor_x="center", bold=True, batch=self.batchPanel)
        self.attackText = pyglet.text.Label("Attaque: ", batch=self.batchPanel)
        self.resistanceText = pyglet.text.Label("Resistance: ", batch=self.batchPanel)
        self.speedText = pyglet.text.Label("Vitesse: ", batch=self.batchPanel)

        self.mucusTextShadow = pyglet.text.Label("100 / 100", x=0, y=0, font_size=18, bold=True ,anchor_x="right", batch=self.batch, color=(0, 0, 0, 255))
        self.mucusText = pyglet.text.Label("100 / 100", x=0, y=0, font_size=18, bold=True ,anchor_x="right", batch=self.batch)

    def toggleMenu(self, state):
        self.menuOpened = state

    def toggleDevTool(self):
        if self.showDevTool:
            self.showDevTool = False
        else:
            self.showDevTool = True

    def render(self, x, y, player):

        # - Définition des origines -
        width, height = gameEngine.getDinamicWindowSize()
        originX = int(x - width/2)
        originY = int(y - height/2)

        # - Barre de vie -
        self.drawBar(originX + self.hpPos["x"], originY + self.hpPos["y"], self.hpSize["x"], self.hpSize["y"], (1, 0, 0), 3, player.hp/player.maxHp)
        if int(player.shield) > 0:
            self.drawBar(originX + 5, originY + self.shieldPos["y"], self.shieldSize["x"], self.shieldSize["y"], (0.10, 0.5, 1), 3, player.shield/player.shieldCapacity)

        # - Mucus -
        self.mucusTextShadow.x = originX + width - 3
        self.mucusTextShadow.y = originY + 13
        self.mucusTextShadow.text = "%i / %i " % (player.mucus, player.mucusMax)
        self.mucusText.x = originX + width - 5
        self.mucusText.y = originY + 15
        self.mucusText.text = "%i / %i " % (player.mucus, player.mucusMax)

        if self.menuOpened:
            pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
            pyglet.gl.glColor4f(0, 0, 0, 0.33)
            pyglet.gl.glVertex2i(originX, y - self.sidePanelHeight/2)
            pyglet.gl.glVertex2i(originX + self.sidePanelWidth, y - self.sidePanelHeight / 2)
            pyglet.gl.glVertex2i(originX + self.sidePanelWidth, y + self.sidePanelHeight / 2)
            pyglet.gl.glVertex2i(originX, y + self.sidePanelHeight / 2)
            pyglet.gl.glEnd()

            pyglet.gl.glBegin(pyglet.gl.GL_LINE_STRIP)
            pyglet.gl.glColor4f(0, 0, 0, 1)
            pyglet.gl.glVertex2i(originX, y - self.sidePanelHeight/2)
            pyglet.gl.glVertex2i(originX + self.sidePanelWidth, y - self.sidePanelHeight/2)
            pyglet.gl.glVertex2i(originX + self.sidePanelWidth, y + self.sidePanelHeight/2)
            pyglet.gl.glVertex2i(originX, y + self.sidePanelHeight/2)
            pyglet.gl.glEnd()

            # - Update des positions et valeurs de infos panel -
            self.panelTitle.x = originX + self.sidePanelWidth/2
            self.panelTitle.y = originY + gameEngine.GameEngine.W_HEIGHT/2 + self.sidePanelHeight/2 - 20

            panelTop = originY + gameEngine.GameEngine.W_HEIGHT/2 + self.sidePanelHeight / 2

            self.attackText.x = originX + 5
            self.attackText.y = panelTop - 50
            self.attackText.text = "Attaque: %i" % player.attack

            self.resistanceText.x = originX + 5
            self.resistanceText.y = panelTop - 75
            self.resistanceText.text = "Resistance: %i" % player.resistance

            self.speedText.x = originX + 5
            self.speedText.y = panelTop - 100
            self.speedText.text = "Vitesse: %i" % player.speed

            self.batchPanel.draw()

        # - Redéfinition des positions du texte -
        self.hpLabel.x, self.hpLabel.y = originX + self.hpPos["x"] + self.hpSize["x"] - 6, originY + self.hpPos["y"] + self.hpSize["y"]/2
        self.shieldLabel.x, self.shieldLabel.y = originX + self.shieldPos["x"] + self.shieldSize["x"] - 6, originY + self.shieldPos["y"] + self.shieldSize["y"]/2
        self.hpLabel.text = str(int(player.hp)) + " / " + str(int(player.maxHp))

        if int(player.shield) > 0:
            self.shieldLabel.text = str(int(player.shield)) + " / " + str(int(player.shieldCapacity))
        else:
            self.shieldLabel.text = ""

        # - update des outils devs -
        if self.showDevTool:
            fps = str(round(pyglet.clock.get_fps(), 2))
            self.fpsShadow.x = originX + 3
            self.fpsShadow.y = originY + height - 1
            self.fpsShadow.text = "Fps: %s" % fps
            self.fps.x = originX + 2
            self.fps.y = originY + height
            self.fps.text = "Fps: %s" % fps

            # On draw a la main, les batchs sont foieux.
            self.fpsShadow.draw()
            self.fps.draw()

        self.batch.draw()

    def drawBar(self, x, y, width, height, color, border, progress):
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)

        if border:
            pyglet.gl.glColor3f(0, 0, 0)
            pyglet.gl.glVertex2i(x, y)
            pyglet.gl.glVertex2i(x + width, y)
            pyglet.gl.glVertex2i(x + width, y + height)
            pyglet.gl.glVertex2i(x, y + height)

            pyglet.gl.glColor3f(1, 1, 1)
            pyglet.gl.glVertex2i(x + 1, y + 1)
            pyglet.gl.glVertex2i(x + width - 1, y + 1)
            pyglet.gl.glVertex2i(x + width - 1, y + height - 1)
            pyglet.gl.glVertex2i(x + 1, y + height - 1)

            pyglet.gl.glColor3f(0, 0, 0)
            pyglet.gl.glVertex2i(x + border, y + border)
            pyglet.gl.glVertex2i(x + width - border, y + border)
            pyglet.gl.glVertex2i(x + width - border, y + height - border)
            pyglet.gl.glVertex2i(x + border, y + height - border)

            pyglet.gl.glColor3f(color[0], color[1], color[2])
            pyglet.gl.glVertex2i(x + border + 1, y + border + 1)
            pyglet.gl.glVertex2i(x + border + 1 + int((width - border * 2 - 2) * progress), y + border + 1)
            pyglet.gl.glVertex2i(x + border + 1 + int((width - border * 2 - 2) * progress), y + height - border - 1)
            pyglet.gl.glVertex2i(x + border + 1, y + height - border - 1)

        else:
            pyglet.gl.glColor3f(color[0], color[1], color[2])
            pyglet.gl.glVertex2i(x, y)
            pyglet.gl.glVertex2i(x + int((width - border * 2 - 2) * progress), y)
            pyglet.gl.glVertex2i(x + int((width - border * 2 - 2) * progress), y + height)
            pyglet.gl.glVertex2i(x, y + height)

        pyglet.gl.glEnd()
