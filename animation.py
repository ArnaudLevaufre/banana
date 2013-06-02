#-*- encoding:utf-8 -*-

import time
import pyglet


class AnimationGroup(object):
    """
    Class de gestion des animations customisé (celle de pyglet ne proposant pas ce que nous souhaitons)
    Ainsi on peut gérer les animations par groupe.
    """
    def __init__(self):
        self.animationList = []
        self.selectedAnimation = 0

    def setFrameRate(self, frameRate):
        for anim in self.animationList:
            anim.frameRate = frameRate

    def setIdleState(self):
        for anim in self.animationList:
            anim.idle = True

    def unsetIdleState(self):
        for anim in self.animationList:
            anim.idle = False

    def createFromImage(self, image, tileWidth, tileHeight):
        """
        Créer une animation à partir d'une image.

        :type image: Image from pyglet.image.load
        :type tileWidth: int
        :type tileHeight: int
        """

        tileLine = pyglet.image.ImageGrid(image, image.height / tileHeight, 1)

        # calcul du nombre de ligne:
        nbrLine = image.height / tileHeight

        for i in range(nbrLine):
            # création de l'animation
            anim = Animation()
            anim.createFromImage(tileLine[i], tileWidth)
            # ajout l'animation dans la liste.
            self.animationList.append(anim)

    def selectAnimation(self, nbr):
        if nbr < len(self.animationList):
            self.selectedAnimation = nbr

    def render(self, x, y):
        self.animationList[self.selectedAnimation].render(x, y)


class Animation(object):
    """
    Classe gérant l'animation. Un fichier image
    peut être directement parsé afin de créer une animation
    automatiquement.
    """
    def __init__(self, frameRate=1):
        self.frames = []
        self.lastFrameChange = time.time()
        self.currentFrame = 0
        self.frameRate = frameRate
        self.idle = False

    def createFromImage(self, image, tileWidth):
        frameList = pyglet.image.ImageGrid(image, 1, image.width / tileWidth)

        # conversion en sprites
        for frame in frameList:
            self.frames.append(pyglet.sprite.Sprite(frame))

    def render(self, x, y):
        # Changement de la frame si nécéssaire
        if not self.idle:
            if time.time() - self.lastFrameChange >= self.frameRate:
                self.lastFrameChange = time.time()

                # on assure un bon cycle d'animation
                if self.currentFrame + 1 < len(self.frames):
                    self.currentFrame += 1
                else:
                    self.currentFrame = 0
        else:
            self.currentFrame = 0

        # Positionement du sprite et affichage
        self.frames[self.currentFrame].x = x
        self.frames[self.currentFrame].y = y
        self.frames[self.currentFrame].draw()
