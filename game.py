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
import math

# ---------------------------------------------------


class Game(object):
    def __init__(self, isContinue=False, loadLevel=None):
        """
        Classe de gestion du jeux. Il s'agit ni plus ni moins que du moteur de jeux.
        Game va donc être en charge de créer une instance de niveau, une instance de Map, 
        gérer les ennemies, le joueur, les projectiles.
        
        :param isContinue: Permet de savoir si le joueur continue la partie déja existante. 
        :param  loadLevel: si différent de False, il s'agit d'une partie rapide.
        
        :type isContinue: bool
        :type  loadLevel: None ou str
        """
        
        self.camera = Camera()
        self.ui = ui.UI()
        self.level = level.Level()
        self.save = save.Save()
        
        if not isContinue and not loadLevel:
            # - creer nouvelle partie -
            self.level.load("Z1-N1")
            self.lvl = 1
            
        elif loadLevel is not None:
            self.level.campaign = False
            self.level.load(str(loadLevel))
            
        elif isContinue:
            self.save.load()
            self.level.load(self.save.lvl)
            self.lvl = self.save.lvl
            self.level.player.loadFromSave(self.save)

        self.map = self.level.map
        self.player = self.level.player
        self.bullets = []
        self.batch = pyglet.graphics.Batch()

        self.returnState = "playing"

        if self.level.cinematique is not None:
            self.cinematiqueIsPlaying = True
        else:
            self.cinematiqueIsPlaying = False

        self.deadLabel = pyglet.text.Label("GAME OVER !\n\nPRESS ANY KEY TO CONTINUE", font_size=20, anchor_x="center", width=500, multiline=True, anchor_y="center", color=(255, 255, 255, 255))

        self.tick = 0
        self.gameEnded = False
        self.dead = False

    def simulate(self, dt, keysHandler):
        """
        Fonction pricipale de simulation du jeux en cours.
        On vérifira les actions clavier est on fera bouger le joueur
        lorsque nécéssaire.
        La simulation du déplacement des ennemies ainsi que des projectile
        est appelé ici.
        Enfin nous trouverons la base de la gestion des items.
        Dans le cas particulier ou la cinématique est joué on ne fait rien.
        
        :param dt: l'interval entre deux appel de la fonction
        :param keysHandler: une liste des touches qui sont enfoncés
        
        :type dt: float
        :type keyHandler: dict
        """
        
        self.tick += 1
        if self.cinematiqueIsPlaying is False and not self.dead:
            # si on ne joue pas de cinématiques.

            self.playerdx, self.playerdy = self.player.x, self.player.y
            
            if keysHandler[key.Z]:
                # déplacement vers le haut
                self.player.move(0, 10, self.map, dt)
            elif keysHandler[key.S]:
                # déplacement vers le bas
                self.player.move(0, -10, self.map, dt)

            if keysHandler[key.Q]:
                # déplacement à gauche
                self.player.move(-10, 0, self.map, dt)
            elif keysHandler[key.D]:
                # déplacement à droite
                self.player.move(10, 0, self.map, dt)
            
            # calcul du dx et dy de la position du joueur. Ces valeurs serivirons dans le cadre des tirs ennemis
            self.playerdx, self.playerdy = self.player.x - self.playerdx, self.player.y - self.playerdy

            # commande d'affichage du panel des infos
            if keysHandler[key.TAB]:
                self.ui.toggleMenu(True)
            else:
                self.ui.toggleMenu(False)

            # vérification de la mort du joueur
            if int(self.player.hp) <= 0:
                pyglet.gl.glClearColor(0, 0, 0, 1)
                self.dead = True

            # tir du joueur
            if self.player.isFiring:
                self.player.shoot(self.bullets, self.batch)

            # regénération de mucus
            self.player.increaseMucus()

            # simulation des projectiles
            for bullet in self.bullets:
                if bullet.simulate(self.map, self.player, self.level.enemies, dt) is False:
                    self.bullets.remove(bullet)

            # calcul de la position de tir des ennemis
            targetPosX = self.player.x + self.playerdx * (self.player.speed - 1)
            targetPosY = self.player.y + self.playerdy * (self.player.speed - 1)
            
            # Simulation des ennemis
            for ent in self.level.enemies:  
                ent.shoot(targetPosX, targetPosY, self.bullets, self.batch)
                try:
                    if ent.hp < 0:  # Si l'ennemi est mort
                        self.level.enemies.remove(ent)
                        loot = ent.loot()
                        if loot is not None:
                            self.level.items.append(loot)
                    elif self.tick % 4 == 0 and 64 < math.sqrt((self.player.x - ent.x)**2 + (self.player.y - ent.y)**2) < 30*64 and ent.canMove:
                        ent.IA._recompute_path(self.player.x, self.player.y, ent.caseX, ent.caseY)
                    elif 64 > math.sqrt((self.player.x - ent.x)**2 + (self.player.y - ent.y)**2) and random.random() < ent.fireRate/50:
                        self.player.hit(ent.attack)
                    ent.move((ent.IA.path[-2][0] - ent.caseX), (ent.IA.path[-2][1]-ent.caseY), self.map, dt)
                except:
                    pass

            # gesion de items
            for item in self.level.items:
                if item.collide(self.player):
                    self.level.items.remove(item)
                    if item.type == "chest":
                        chest = entity.Enemy(item.x - map.Tile.SIZE, item.y - map.Tile.SIZE, "chest", self.map, self.level.gridMap, self.level.suc)
                        if random.randint(0, 1) == 1:
                            self.level.enemies.append(chest)  # Rajouter le coffre comme monstre
                        else:
                            self.level.items.append(chest.loot())
                    else:
                        self.level.player.pick(item)

            # Fin du niveau, quand tout les ennemis sont vaincus
            if self.level.enemies == []:
                # Si le niveau est fini, on save la partie
                if self.level.nextLevel != "":
                    self.lvl = self.level.nextLevel
                    if self.level.campaign:
                        self.player.save(self.save, self.lvl)
                        self.save.save()

                    # On passe au suivant
                    self.reload()
                else:
                    print "coucou"
                    self.camera.reset()
                    self.returnState = "menu"
            else:
                self.camera.setPos(self.player.x, self.player.y)

    def reload(self):
        """ rechargement du niveau """
        try:
            if not self.gameEnded:
                self.camera = Camera()
                self.ui = ui.UI()
                self.level = level.Level()
                self.level.load(str(self.lvl))
                self.player = self.level.player
                self.map = self.level.map
                self.bullets = []
                self.cinematiqueIsPlaying = True
                self.tick = 0
        except:
            self.gameEnded = True

    def on_mouse_press(self, x, y, button, modifiers):
        # toggle le tir du joueur lorsque l'on click gauche
        if button == pyglet.window.mouse.LEFT:
            self.player.isFiring = True
            self.player.aim(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        # reset le tir du joueur quand on relache le click gauche
        if button == pyglet.window.mouse.LEFT:
            self.player.isFiring = False

    def on_mouse_drag(self, x, y, dx, dy, button, mod):
        # On met à jour la position de la visée quand on bouge la souris 
        # avec le click gauche enfoncé.
        if button == pyglet.window.mouse.LEFT:
            self.player.aim(x, y)
        
    def on_mouse_motion(self, x,y, dx, dy):
        self.player.aim(x,y)

    def on_key_press(self, symbol, modifier):
        if self.dead:
            # rechargement de la partie si le joueur est mort.
            pyglet.gl.glClearColor(0.5, 0.75, 1, 1)
            self.dead = False
            self.reload()
            self.player.hp = self.player.maxHp

    def render(self):
        """ Affichage des éléments du jeu """
        
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

        return self.returnState


# ---------------------------------------------------


class Camera:
    """
    Classe gérant la caméra. 
    Lorsque l'on veut centrer la caméra sur quelque chose
    on réalise un translation du plan. (Tout ceci
    est géré par openGL, et heureusement vue les 
    matrices qu'il y à deriere) 
    """
    
    def __init__(self):
        self.x = 0
        self.y = 0

    def setPos(self, x, y):
        self.x = x
        self.y = y

        width, height = gameEngine.getDinamicWindowSize()

        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslated(width/2 - x, height/2 - y, 0)

    def reset(self):
        width, height = gameEngine.getDinamicWindowSize()
        self.setPos(width / 2, height / 2)
