#-*- encoding: utf-8 -*-
import pyglet
import pyglet.window.key as key
import gameEngine
import entity
import ui
import map
import level
import math
import random

# ---------------------------------------------------


class Game(object):
    def __init__(self):

        self.lvl = 1
        self.camera = Camera()
        self.ui = ui.UI()
        self.level = level.Level()
        self.level.load("1")
        self.map = self.level.map
        self.player = self.level.player
        self.bullets = []
        self.cinematiqueIsPlaying = True
        self.tick = 0

    def simulate(self, dt, keysHandler):
        self.tick += 1
        if self.cinematiqueIsPlaying is False:
            self.playerdx, self.playerdy = self.player.x, self.player.y

            if keysHandler[key.Z]:
                self.player.move(0, 10, self.map, dt)
            elif keysHandler[key.S]:
                self.player.move(0, -10, self.map, dt)

            if keysHandler[key.Q]:
                self.player.move(-10, 0, self.map, dt)
            elif keysHandler[key.D]:
                self.player.move(10, 0, self.map, dt)

            if keysHandler[key.TAB]:
                self.ui.toggleMenu(True)
            else:
                self.ui.toggleMenu(False)

            self.playerdx = self.player.x - self.playerdx
            self.playerdy = self.player.y - self.playerdy

            # tir du joueur
            self.player.shoot(self.bullets)

            self.player.increaseMucus()

            for bullet in self.bullets:
                if bullet.simulate(self.map, self.player, self.level.enemies, dt) is False:
                    self.bullets.remove(bullet)

            for ent in self.level.enemies:  # Simulation des ennemis
                ent.shoot(self.player.x + self.playerdx*10, self.player.y + self.playerdy * 10, self.bullets)
                try:
                    if ent.hp < 0:  # Si l'ennemi est mort
                        self.level.enemies.remove(ent)
                        loot = ent.loot()
                        if loot is not None:
                            self.level.items.append(loot)

                    if self.tick % 4 == 0 and math.sqrt((self.player.x - ent.x)**2 + (self.player.y - ent.y)**2) < 64*8:
                        ent.IA._recompute_path(self.player.x, self.player.y, ent.caseX, ent.caseY)
                    ent.move((ent.IA.path[-2][0] - ent.caseX), (ent.IA.path[-2][1]-ent.caseY), self.map, dt, ent.IA.path[-2])
                except:
                    pass

            for item in self.level.items:
                if item.collide(self.player):
                    self.level.items.remove(item)
                    if item.type == "shield":
                        self.player.shieldCapacity += item.value
                        self.player.shield += item.value
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
                        chest = entity.Enemy(item.x - map.Tile.SIZE, item.y - map.Tile.SIZE, "chest", self.map)
                        if random.randint(0, 1) == 1:
                            print "ennemi"
                            self.level.enemies.append(chest)  # Rajouter le coffre comme monstre
                        else:
                            self.level.items.append(chest.loot())

            if self.level.enemies == []:
                print "FINI"
                self.lvl += 1
                self.reload()
            # on repositionne la carte.
            self.camera.setPos(self.player.x, self.player.y)

    def reload(self):
        # On load le level self.lvl
        try:
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
            print "FIN"

    def on_mouse_press(self, x, y, button, modifiers):
        if(button == pyglet.window.mouse.LEFT):
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

    def render(self):
        if self.cinematiqueIsPlaying is False:
            self.map.render()
            self.ui.render(self.camera.x, self.camera.y, self.player)
            self.player.render()

            for bullet in self.bullets:
                if self.player.x - gameEngine.GameEngine.W_WIDTH/2 < bullet.x < self.player.x + gameEngine.GameEngine.W_WIDTH/2 and self.player.y - gameEngine.GameEngine.W_HEIGHT/2 < bullet.y < self.player.y + gameEngine.GameEngine.W_WIDTH/2:
                    pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
                    pyglet.gl.glVertex2d(bullet.x - bullet.SIZE / 2, bullet.y - bullet.SIZE / 2)
                    pyglet.gl.glVertex2d(bullet.x - bullet.SIZE / 2 + entity.Bullet.SIZE, bullet.y - bullet.SIZE / 2)
                    pyglet.gl.glVertex2d(bullet.x - bullet.SIZE / 2 + entity.Bullet.SIZE, bullet.y - bullet.SIZE/2 + entity.Bullet.SIZE)
                    pyglet.gl.glVertex2d(bullet.x - bullet.SIZE / 2, bullet.y - bullet.SIZE/2 + entity.Bullet.SIZE)
                    pyglet.gl.glEnd()
                else:
                    self.bullets.remove(bullet)

            for ent in self.level.enemies:
                ent.render()

            for item in self.level.items:
                item.render()
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
