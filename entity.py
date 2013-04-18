#-*- encoding: utf-8 -*-
import math, time
import pyglet
import gameEngine
import game

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
        if self.xVel != 0:
            self.x += self.xVel * dt
        if self.yVel != 0:
            self.y += self.yVel * dt
            
    def move(self, x,y, gameMap ,dt):
        if not gameMap.collide( self.x - self.width/2 + x * dt * self.speed, self.y - self.height/2 + y * dt * self.speed, self.width, self.height):
            self.x += int(x * dt * self.speed)
            self.y += int(y * dt * self.speed)
            
# ---------------------------------------------------

class Enemy(Entity):
    """
    Ennemie pour tester l'IA, il essaie juste de toucher le joueur
    """
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.width = 48
        self.height = 48
        self.speed = 30
        self.blocked = False
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load("sprites/blarg.png").get_texture())
        self.x = int(x)  * game.Tile.SIZE
        self.y = int(y)  * game.Tile.SIZE 
        
    def render(self):
        self.sprite.x = self.x - self.width/2
        self.sprite.y = self.y - self.height/2
        self.sprite.draw()
        
    def move(self, x,y, gameMap ,dt, recurs = False):   
        if not gameMap.collide( self.x - self.width/2 + x * dt * self.speed, self.y - self.height/2 + y * dt * self.speed, self.width, self.height):
            # Si il ne collisione pas, il se déplace normalement
            self.x += int(x * dt * self.speed)
            self.y += int(y * dt * self.speed)
            self.blocked = False
        if not recurs:
            if gameMap.collide( self.x - self.width/2 + x * dt * self.speed, self.y - self.height/2, self.width, self.height):
                # Si c'est en x que l'on collide, on se déplace en y dans la direction vers le joueur
                if(y >= 0 or self.blocked == "top" and not self.blocked == "bot"):
                    self.move(0,10, gameMap ,dt, True)
                    self.blocked = "top"
                elif(y < 0 or self.blocked == "bot" and not self.blocked == "top"):
                    self.move(0,-10, gameMap ,dt, True)
                    self.blocked= "bot"
            elif gameMap.collide( self.x - self.width/2 , self.y - self.height/2 + y * dt * self.speed, self.width, self.height):
                # Si c'est en y que l'on collide, on se déplace en x dans la direction vers le joueur
                if(x >= 0 or self.blocked == "right" and not self.blocked == "left"):  
                    self.move(10,0, gameMap ,dt, True)
                    self.blocked ="right"
                elif(x < 0 or self.blocked == "left" and not self.blocked == "right"):
                    self.move(-10,0, gameMap ,dt, True)
                    self.blocked = "left"
                
# ---------------------------------------------------     

class Player(Entity):
    """ 
    Joueur
    """
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
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
        
        try:
            self.aimVector[0] = (x - centerX) / norm
            self.aimVector[1] = (y - centerY) / norm
        except ZeroDivisionError:
            print "Do or do not, there is no try!"
            self.aimVector[0] = 0
            self.aimVector[1] = 1
    
    def shoot(self, bullets):
        if self.isFiring and time.time() - self.lastShoot > 1/self.fireRate:
            self.lastShoot = time.time()
            bullets.append(Bullet( self.x, self.y + self.mouthOffset, self.aimVector[0]*1000, self.aimVector[1]*1000, "player" ))
        
        
#     def move(self, x,y, gameMap ,dt):
#         
#         if not gameMap.collide( self.x - self.width/2 + x * dt * self.speed, self.y - self.height/2 + y * dt * self.speed, self.width, self.height):
#             self.x += int(x * dt * self.speed)
#             self.y += int(y * dt * self.speed)
                    
    def render(self):
        self.sprite.x = self.x - self.width/2
        self.sprite.y = self.y - self.height/2
        self.sprite.draw()

# ---------------------------------------------------

class Npc(object):
    def __init__(self,x,y):
        super(Npc, self).__init__(x,y)
        
        
    def move(self, map):
        pass
    
    def render(self):
        pass
    
    def kill(self):
        pass
    
# ---------------------------------------------------   

class Bullet(Entity):
    SIZE = 10
    
    def __init__(self, x,y, xVel, yVel, owner):
        self.initX = x
        self.initY = y
        self.height = 10
        self.width = 10
        self.speed = 1
        self.range = 200
        super(Bullet, self).__init__(x, y, xVel, yVel)
        self.owner = owner
        print self.initX
        
        
    def simulate(self,gameMap, dt=1):
        norm = math.sqrt((self.initX - self.x)**2 + (self.initY - self.y)**2)
        if not gameMap.collide( self.x - self.width/2 + self.xVel * dt * self.speed, self.y - self.height/2 + self.yVel * dt * self.speed, self.width, self.height) and norm < self.range:
            self.x += int(self.xVel * dt * self.speed)
            self.y += int(self.yVel * dt * self.speed)
        else:
            return False