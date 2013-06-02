# coding=utf-8
import pyglet
import game
import menu
import mapCreator as mc
import sys


class GameEngine(pyglet.window.Window):

    """
    == Classe principale de l'application ==

    C'est ici que l'on transmet tout les evenement
    clavier, souris, commande d'affichage.

    On est entierement guidé par la variable
    _state qui, celon ca valeur, nous indique
    l'état du programme, c'est à dire si nous
    somme dans le menu, dans l'éditeur, en
    jeu, etc ...
    Ainsi suivant le cas on transmet lesd
    evenement selement à la partie du
    programme qui nous intéresse.
    """

    W_WIDTH = 1024
    W_HEIGHT = 640

    def __init__(self):
        super(GameEngine, self).__init__(width=self.W_WIDTH, height=self.W_HEIGHT, resizable=True)

        #   =======
        # ~ OPTIONS ~
        #   =======

        # - Options generales -
        self.set_vsync(False)
        self.set_caption("Blarg")
        self.set_mouse_cursor(pyglet.window.ImageMouseCursor(pyglet.image.load('data/sprites/vis.png'), 8, 8))  # Curseur

        # - Couleur de fond -
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glClearColor(0.5, 0.75, 1, 1)

        # - Physique -
        pyglet.clock.schedule_interval(lambda x: False, 1/100000000.0)  # Debridage complet des FPS
        pyglet.clock.schedule_interval(self.physicEngine, 1/100.0)

        #   =========
        # ~ VARIABLES ~
        #   =========

        # - Input handler -

        self.keysHandler = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keysHandler)

        # - Etat -
        self._state = "menu"

        # - Objets -
        self._menu = menu.MainMenu()

    def physicEngine(self, dt):
        """
        Moteur physique principal, il fait appel au fonctions
        chargés de calculer les déplacement ainsi que celles
        calculant les différents macanismes du jeu. Elle
        transmet à chaque fois dt, indispensable dans
        les calculs de déplacement afin de garder une vitesse
        constante.
        """

        if self._state == "new":
            self._game = game.Game()
            self._state = "playing"

        elif self._state == "continue":
            self._game = game.Game(isContinue=True)
            self._state = "playing"

        elif self._state == "rapid":
            self._levelSelector = menu.LevelSelector()
            self._state = "levelSelector"

        elif self._state == "levelSelector" and self._levelSelector.choosenLevel is not None:
            self._game = game.Game(loadLevel=self._levelSelector.choosenLevel)
            self._state = "playing"

        elif self._state == "playing" and self._game:
            self._game.simulate(dt, self.keysHandler)

        elif self._state == "creator" and self._creator:
            self._creator.refresh(dt, self.keysHandler)

        elif self._state == "askNewCreator":
            self._creator = mc.App()
            self._state = "creator"

    def on_draw(self):
        """
        Fonction d'affichage principale.
        Elle commande l'appel de l'affichage
        des diférents éléments du jeux, de l'éditeur
        ou du menu celon les cas.
        """

        self.clear()
        # ----------------------------
        if self._state == "playing" and self._game:
            self._state = self._game.render()
        elif self._state == "menu":
            self._state = self._menu.render()
            self._menu.setDefault()
        elif self._state == "quit":
            self.close()
            sys.exit()  # sinon quelques erreurs en sortie de jeux du a des trucs inexistants.
        elif self._state == "creator":
            self._state = self._creator.render()
        elif self._state == "levelSelector":
            self._levelSelector.render()

        # -----------------------------

    def on_mouse_press(self, x, y, button, modifiers):
        # - Passage des evenements aux autres objets
        if self._state == "playing":
            self._game.on_mouse_press(x, y, button, modifiers)

        elif self._state == "menu":
            self._menu.on_mouse_press(x, y, button, modifiers)

        elif self._state == "creator":
            self._creator.on_mouse_press(x, y, button, modifiers)

        elif self._state == "levelSelector":
            self._levelSelector.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        # - Passage des evenements aux autres objets
        if self._state == "playing":
            self._game.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # - Passage des evenements aux autres objets
        if self._state == "playing":
            self._game.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        elif self._state == "creator":
            self._creator.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        # - Passage des evenements aux autres objets
        if self._state == "menu":
            self._menu.on_mouse_motion(x, y, dx, dy)
        elif self._state == "creator":
            self._creator.on_mouse_motion(x, y, dx, dy)
        elif self._state == "playing":
            self._game.on_mouse_motion(x, y, dx, dy)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self._state == "creator":
            self._creator.on_mouse_scroll(x, y, scroll_x, scroll_y)

        if self._state == "levelSelector":
            self._levelSelector.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_key_press(self, symbol, modifier):
        if symbol == pyglet.window.key.F1 and self._state == "playing":
            self._game.ui.toggleDevTool()
        elif self._state == "creator":
            self._creator.on_key_press(symbol, modifier)
        elif self._state == "playing":
            self._game.on_key_press(symbol, modifier)

    def on_text(self, text):
        if self._state == "creator":
            self._creator.on_text(text)

    def on_text_motion(self, motion):
        if self._state == "creator":
            self._creator.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self._state == "creator":
            self._creator.on_text_motion_select(motion)

    def start(self):
        pyglet.app.run()


def getDinamicWindowSize():
    """
    Fonction permetant de récupérer la taille
    de la fenetre sans avoir a transmetre l'object Window
    """
    if len(pyglet.app.windows) != 0:
        for window in pyglet.app.windows:
            return window.width, window.height
    else:
        return 0, 0
