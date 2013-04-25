#-*- encoding: utf-8 -*-
import math, time
import pyglet
import gameEngine
import random
import IA
import item
import vector
from random import Random
# ---------------------------------------------------

class Entity(object):
    """
    Classe generale d'une entitée
    """
    def __init__(self, x=0, y=0, xVel=0, yVel=0):
        self.x = int(x)
        self.y = int(y)
        self.xVel = xVel
        self.yVel = yVel

    def simulate(self, dt=1):
        pass
            
    def move(self, x,y, gameMap ,dt):
        if not gameMap.collide( self.x - self.width/2 + x * dt * self.speed, self.y - self.height/2 + y * dt * self.speed, self.width, self.height):
            self.x += int(x * dt * self.speed)
            self.y += int(y * dt * self.speed)
            
# ---------------------------------------------------

class Enemy(Entity):
    """
    Ennemie pour tester l'IA, il essaie juste de toucher le joueur
    """
    def __init__(self, x, y, gameMap):
        # - Objets -
        Entity.__init__(self, x, y)

        # - Constantes -
        self.width = 48
        self.height = 48
        self.speed = 300
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load("sprites/blarg.png").get_texture())
        self.type = "enemy"
        
        # - Mouvements -
        self.blocked = False
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load("sprites/blarg.png").get_texture())
        self.x = int(x)
        self.y = int(y)
        
        # - IA -
        self.IA = IA.IA(self.x, self.y, gameMap)
        self.caseX = self.x / 64
        self.caseY = self.y / 64
        
        # - Caracs -
        self.hp = 100
        self.fireRate = 10.0
        self.bulletSpeed = 500.0
        self.attack = 1

    def render(self):
        self.sprite.x = self.x - self.width/2
        self.sprite.y = self.y - self.height/2
        self.sprite.draw()
        
    def move(self, x,y, gameMap ,dt, target):
        if not gameMap.collide( self.x - self.width/2 + x * dt * self.speed, self.y - self.height/2 + y * dt * self.speed, self.width, self.height):
            # Si il ne collisione pas, il se déplace normalement
            self.x += int(x * dt * self.speed)
            self.y += int(y * dt * self.speed)
            self.caseX = (self.x+32) / 64
            self.caseY = (self.y+32) / 64
            
    def hit(self):
        self.hp -= 10
        
    def shoot(self, x, y, bulletList):
        print x,y,bulletList
        if random.random() < self.fireRate/200:
            aimDirection = vector.Vector2(x - self.x, y - self.y).getUnitary()
            bulletList.append(Bullet(self.x, self.y, aimDirection.x * self.bulletSpeed, aimDirection.y * self.bulletSpeed, self ))
            
            
    def loot(self):
        objet = random.randint(1,2)
        if objet == 1: # Shield
            itemToReturn = item.Shield(self.x,self.y, 50)    
        else:
            itemToReturn = item.Life(self.x, self.y, 50)
        return itemToReturn

# ---------------------------------------------------     

class Player(Entity):
    """ 
    Joueur
    """
    def __init__(self, x, y):
        # - Objets -
        Entity.__init__(self, x, y)
       
        # - Constantes -
        self.width = 48
        self.height = 48
        self.aimVector = vector.Vector2(0,0)
        self.mouthOffset = 7
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load("sprites/blarg.png").get_texture())
        self.sprite.x = gameEngine.GameEngine.W_WIDTH/2 - self.width/2
        self.sprite.y = gameEngine.GameEngine.W_HEIGHT/2 - self.height/2
        self.type = "player"
        # - Tir -
        self.isFiring = False
        self.lastShoot = time.time()
    
        # - Caractéristiques -
        self.maxHp = 100.0
        self.hp = 100.0
        self.speed = 30.0
        self.shieldCapacity = 50.0
        self.shield = 50.0
        self.fireRate = 50.0
        self.resistance = 10
        self.attack = 10
        
        
    def aim(self, x, y):
        """
        Détermine le vecteur directeur de la droite passant par 
        le centre de l'écran et le pointeur de la souris.
        On le détermine en divisant le vecteur définit
        par le centre de l'écran et le cursor par sa norme.
        """
        centerX = gameEngine.GameEngine.W_WIDTH/2
        centerY = gameEngine.GameEngine.W_HEIGHT/2 + self.mouthOffset
        
        self.aimVector.set(x-centerX, y-centerY)
        self.aimVector = self.aimVector.getUnitary()

    
    def shoot(self, bullets):
        if self.isFiring and time.time() - self.lastShoot > 1/self.fireRate:
            self.lastShoot = time.time()
            bullets.append(Bullet( self.x, self.y + self.mouthOffset, self.aimVector.x*1000, self.aimVector.y*1000, self ))
    
    def hit(self, attack):
        # pour le moment on se contente de dégager de la vie
        if self.hp - attack > 0: 
            self.hp -= attack
        else:
            self.hp =  0
        
    def render(self):
        self.sprite.x = self.x - self.width/2
        self.sprite.y = self.y - self.height/2
        self.sprite.draw()

    
# ---------------------------------------------------   

class Bullet(Entity):
    SIZE = 10
    
    def __init__(self, x,y, xVel, yVel, owner):
        # - Objet -
        super(Bullet, self).__init__(x, y, xVel, yVel)
        
        # - Constantes -
        self.width = 10
        self.height = 10
        self.speed = 1
        self.range = 1000
        self.initX = x
        self.initY = y
        self.owner = owner
        
    def simulate(self,gameMap,player, ennemies, dt=0.1):
        norm = math.sqrt((self.initX - self.x)**2 + (self.initY - self.y)**2)
        if not gameMap.collide( self.x - self.width/2 + self.xVel * dt * self.speed, self.y - self.height/2 + self.yVel * dt * self.speed, self.width, self.height) and norm < self.range:
            self.x += int(self.xVel * dt * self.speed)
            self.y += int(self.yVel * dt * self.speed)
        else:
            return False
        for en in ennemies:
            if self.collide(en):
                en.hit()
                return False
        if self.collide(player):
            player.hit(self.owner.attack)
            
    def collide(self, ent):
        """
                                == COLlIDE ==

        Voir gameMap.collide() pour les explications
        
        :param ent: ennemi avec lequel check les collisions
        :type ent: Ennemy
        """
        if ent.type != self.owner.type:
            # One does not simply understand what's written there
            if self.x <= ent.x <= self.x + self.width or self.x <= ent.x+ent.width <= self.x + self.width:
                if self.y <= ent.y <= self.y + self.height or self.y <= ent.y+ent.height <= self.y + self.height:
                    return True
                elif ent.y <= self.y <= ent.y+ent.height or ent.y <= self.y + self.height <= ent.y+ent.height:
                    return True
                
            elif ent.x <= self.x <= ent.x+ent.width or ent.x <= self.x + self.width <= ent.x+ent.width:
                if (self.y <= ent.y <= self.y + self.height) or (self.y <= ent.y+ent.height <= self.y + self.height):
                    return True
                elif ent.y <= self.y <= ent.y+ent.height or ent.y <= self.y + self.height <= ent.y+ent.height:
                    return True
                    
        return False