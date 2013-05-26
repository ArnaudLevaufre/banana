#-*- encoding: utf-8 -*-
import pyglet
import pyglet.window.key as key
import gameEngine
import entity
import ui
import map
import level
import random
import save
# ---------------------------------------------------


class Game(object):
    def __init__(self, isContinue=False, loadLevel=False):
        """ Si loadLevel vaut False, c'est la campagne
        """
        self.lvl = 2
        self.camera = Camera()
        self.ui = ui.UI()
        self.level = level.Level()
        self.save = save.Save()
        if not isContinue and not loadLevel:
            self.level.load("1")
        elif loadLevel is not False:
            self.level.campaign = False
            self.level.load(str(loadLevel))
        elif isContinue:
            self.save.load()
            self.level.load(self.save.lvl)

        self.map = self.level.map
        self.player = self.level.player
        self.bullets = []
        self.batch = pyglet.graphics.Batch()

        if self.level.cinematique is not None:
            self.cinematiqueIsPlaying = True
        else:
            self.cinematiqueIsPlaying = False

        self.deadLabel = pyglet.text.Label("GAME OVER !\n\nPRESS ANY KEY TO CONTINUE", font_size=20, anchor_x="center", width=500, multiline=True, anchor_y="center", color=(255, 255, 255, 255))

        self.tick = 0
        self.gameEnded = False
        self.dead = False

    def simulate(self, dt, keysHandler):
        self.tick += 1
        if self.cinematiqueIsPlaying is False and not self.dead:
            self.playerdx, self.playerdy = self.player.x, self.player.y

            if keysHandler[key.Z]:
                self.player.move(0, 10, self.map, dt)
            elif keysHandler[key.S]:
                self.player.move(0, -10, self.map, dt)

            if keysHandler[key.Q]:
                self.player.move(-10, 0, self.map, dt)
            elif keysHandler[key.D]:
                self.player.move(10, 0, self.map, dt)

            self.playerdx, self.playerdy = self.player.x - self.playerdx, self.player.y - self.playerdy

            if keysHandler[key.TAB]:
                self.ui.toggleMenu(True)
            else:
                self.ui.toggleMenu(False)

            # Mort ?
            if self.player.hp <= 0:
                pyglet.gl.glClearColor(0, 0, 0, 1)
                self.dead = True

            # tir du joueur
            if self.player.isFiring:
                self.player.shoot(self.bullets, self.batch)

            self.player.increaseMucus()

            for bullet in self.bullets:
                if bullet.simulate(self.map, self.player, self.level.enemies, dt) is False:
                    self.bullets.remove(bullet)

            targetPosX = self.player.x + self.playerdx * 10
            targetPosY = self.player.y + self.playerdy * 10

            for ent in self.level.enemies:  # Simulation des ennemis
                ent.shoot(targetPosX, targetPosY, self.bullets, self.batch)
                try:
                    if ent.hp < 0:  # Si l'ennemi est mort
                        self.level.enemies.remove(ent)
                        loot = ent.loot()
                        if loot is not None:
                            self.level.items.append(loot)
                    if self.tick % 4 == 0 and ((self.player.x - ent.x)**2 + (self.player.y - ent.y)**2) < 280000 and ent.canMove:
                        ent.IA._recompute_path(self.player.x, self.player.y, ent.caseX, ent.caseY)
                    ent.move((ent.IA.path[-2][0] - ent.caseX), (ent.IA.path[-2][1]-ent.caseY), self.map, dt, ent.IA.path[-2])
                except:
                    pass

            for item in self.level.items:
                if item.collide(self.player):
                    self.level.items.remove(item)
                    if item.type == "shield":
                        self.player.shieldCapacity = item.value
                        self.player.shield = item.value
                    elif item.type == "life":
                        if self.player.hp + item.value > self.player.maxHp:
                            self.player.hp = self.player.maxHp
                        else:
                            self.player.hp += item.value
                    elif item.type == "attack":
                        self.player.attack += item.value
                    elif item.type == "speed":
                        self.player.speed += item.value
                    elif item.type == "hpMax":
                        self.player.maxHp += item.Value
                        self.player.hp += item.value
                    elif item.type == "mucus":
                        if self.player.mucus + item.value > self.player.mucusMax:
                            self.player.mucus = self.player.mucusMax
                        else:
                            self.player.mucus += item.value
                    elif item.type == "mucusMax":
                        self.player.mucusMax += item.value
                        self.player.mucus += item.value
                    elif item.type == "fireRate":
                        self.player.fireRate += item.value
                    elif item.type == "resistance":
                        self.player.resistance += item.value
                    elif item.type == "chest":
                        chest = entity.Enemy(item.x - map.Tile.SIZE, item.y - map.Tile.SIZE, "chest", self.map, self.level.gridMap, self.level.suc)
                        if random.randint(0, 1) == 1:
                            self.level.enemies.append(chest)  # Rajouter le coffre comme monstre
                        else:
                            self.level.items.append(chest.loot())

            if self.level.enemies == []:
                self.lvl += 1
                self.reload()
            # on repositionne la carte.
            self.camera.setPos(self.player.x, self.player.y)

    def reload(self):
        # On load le level self.lvl
        try:
            if not self.gameEnded:
                self.camera = Camera()
                self.ui = ui.UI()
                self.level = level.Level()
                self.level.load(str(self.lvl))
                self.player.x, self.player.y = self.level.player.x, self.level.player.y  # On mets le joueur à la bonne place
                self.map = self.level.map
                self.bullets = []
                self.cinematiqueIsPlaying = True
                self.tick = 0
        except:
            self.gameEnded = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.player.isFiring = True
            self.player.aim(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.player.isFiring = False

    def on_mouse_drag(self, x, y, dx, dy, button, mod):
        if button == pyglet.window.mouse.LEFT:
            self.player.aim(x, y)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.aim(x, y)

    def on_key_press(self, symbol, modifier):
        if self.dead:
            pyglet.gl.glClearColor(0.5, 0.75, 1, 1)
            self.dead = False
            self.reload()
            self.player.hp = self.player.maxHp

    def render(self):
        if self.cinematiqueIsPlaying is False and not self.dead:
            self.map.render()
            self.player.render()
            self.batch.draw()

            for ent in self.level.enemies:
                ent.render()

            for item in self.level.items:
                item.render()
            self.ui.render(self.camera.x, self.camera.y, self.player)
        elif self.cinematiqueIsPlaying:
            width, height = gameEngine.getDinamicWindowSize()
            self.camera.setPos(width/2, height/2)
            self.cinematiqueIsPlaying = self.level.cinematique.run()
        elif self.dead:
            width, height = gameEngine.getDinamicWindowSize()
            self.camera.setPos(width / 2, height / 2)
            self.deadLabel.x, self.deadLabel.y = width / 2 + 50, height / 2
            self.deadLabel.draw()

# ---------------------------------------------------


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def setPos(self, x, y):
        self.x = x
        self.y = y

        width, height = gameEngine.getDinamicWindowSize()

        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslated(width/2 - x, height/2 - y, 0)
