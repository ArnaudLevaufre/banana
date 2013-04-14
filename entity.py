#-*- encoding: utf-8 -*-
import math, time
import pyglet
import gameEngine

class Entity(object):
    def __init__(self, x=0, y=0, xVel=0, yVel=0):
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel

    def simulate(self, dt=1):
        if self.xVel != 0:
            self.x += self.xVel * dt
        if self.yVel != 0:
            self.y += self.yVel * dt
            
class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x=0, y=0, xVel=0, yVel=0)
        self.width = 48
        self.height = 48
        self.aimVector = [0,0]
        self.mouthOffset = 7
        self.isFiring = False
        self.lastShoot = time.time()
        
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load("sprites/blarg.png").get_texture())
        self.sprite.x = gameEngine.GameEngine.W_WIDTH/2 - self.width/2
        self.sprite.y = gameEngine.GameEngine.W_HEIGHT/2 - self.height/2
        
        # Caractéristiques du joueur.
        self.maxHp = 100
        self.hp = 100
        self.speed = 30
        self.shieldCapacity = 50
        self.shield = 50
        self.fireRate = 20.0
    
    def getHp(self):
        return self.hp
    
    def getMaxHp(self):
        return self.maxHp
    
    def aim(self, x, y):
        """
        Détermine le vecteur directeur de la droite passant par 
        le centre de l'écran et le pointeur de la souris.
        On le détermine en divisant le vecteur définit
        par le centre de l'écran et le cursor par sa norme.
        """
        centerX = gameEngine.GameEngine.W_WIDTH/2
        centerY = gameEngine.GameEngine.W_HEIGHT/2 + self.mouthOffset
        
        norm = math.sqrt( (x - centerX)**2 + (y - centerY)**2 )
        
        print self.x, gameEngine.GameEngine.W_WIDTH/2
        self.aimVector[0] = (x - centerX) / norm
        self.aimVector[1] = (y - centerY) / norm
    
    def shoot(self, bullets):
        if self.isFiring and time.time() - self.lastShoot > 1/self.fireRate:
            self.lastShoot = time.time()
            bullets.append(Bullet( self.x, self.y + self.mouthOffset, self.aimVector[0]*1000, self.aimVector[1]*1000, "player" ))
        
        
    def move(self, x,y, gameMap ,dt):
        
        if not gameMap.collide( self.x - self.width/2 + x * dt * self.speed, self.y - self.height/2 + y * dt * self.speed, self.width, self.height):
            self.x += int(x * dt * self.speed)
            self.y += int(y * dt * self.speed)
                    
    def render(self):
        self.sprite.x = self.x - self.width/2
        self.sprite.y = self.y - self.height/2
        self.sprite.draw()


class Npc(object):
    def __init__(self,x,y):
        super(Npc, self).__init__(x,y)
        
        
    def move(self, map):
        pass
    
    def render(self):
        pass
    
    def kill(self):
        pass
    
class Bullet(Entity):
    SIZE = 10
    
    def __init__(self, x,y, xVel, yVel, owner):
        super(Bullet, self).__init__(x, y, xVel, yVel)
        self.owner = owner
