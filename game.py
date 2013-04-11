#-*- encoding: utf-8 -*-
import pyglet, pyglet.window.key as key, os, xml.etree.ElementTree as xml
import gameEngine, entity, ui


class Game:
    def __init__(self):
        
        self.uiBatch = pyglet.graphics.Batch()
        self.camera = Camera()
        self.ui = ui.UI()
        self.player = entity.Player(0,0)
        self.map = Map()
        self.map.load("001", self.player)
        self.bullets = []
        
        
        
    def simulate(self, dt, keysHandler):
        if keysHandler[key.Z]:
            self.player.move(0,10, self.map,dt)
        elif keysHandler[key.S]:
            self.player.move(0, -10, self.map, dt)
        
        if keysHandler[key.Q]:
            self.player.move(-10, 0, self.map,dt)
        elif keysHandler[key.D]:
            self.player.move(10, 0, self.map,dt)
            
        if keysHandler[key.TAB]:
            self.ui.toggleMenu(True)
        else:
            self.ui.toggleMenu(False)
        
        # tir du joueur
        self.player.shoot(self.bullets)
        
        for bullet in self.bullets:
            bullet.simulate(dt)
                
        # on repositionne la carte.
        self.camera.setPos(self.player.x, self.player.y)
        
    def on_mouse_press(self,x, y, button, modifiers):
        if(button == pyglet.window.mouse.LEFT):
            self.player.isFiring = True
            self.player.aim(x,y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.player.isFiring = False
            
    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        if(buttons == pyglet.window.mouse.LEFT):
            self.player.aim(x,y)
            
    def render(self):
        
        self.map.render()
        self.player.hp -= 0.1
        print self.player.hp
        self.ui.render(self.camera.x, self.camera.y, self.player)
        self.player.render()
        
        for bullet in self.bullets:
            pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
            pyglet.gl.glVertex2d(bullet.x,bullet.y)
            pyglet.gl.glVertex2d(bullet.x + entity.Bullet.SIZE ,bullet.y)
            pyglet.gl.glVertex2d(bullet.x + entity.Bullet.SIZE, bullet.y + entity.Bullet.SIZE)
            pyglet.gl.glVertex2d(bullet.x ,bullet.y + entity.Bullet.SIZE)
            pyglet.gl.glEnd()

class Map:
    """
    La carte est un tableau d'objets Tile
    """
    
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.xRelative = 0
        self.yRelative = 0
        self.map = []
        self.textures = []
        self.tileSize = 64
        self.loadTextures()
                
    def loadTextures(self):
        tileSheet = pyglet.image.load("sprites/tile-map.jpg")
        imageGrid = pyglet.image.ImageGrid(tileSheet, tileSheet.width/64, tileSheet.height/64)
        
        # on réordonne les tiles de maniere plus propre
        # c'est a dire du haut à gauche jusqu'en bas à droite
        for y in range(tileSheet.height/64 - 1, 1, -1):
            for x in range(tileSheet.width/64):
                self.textures.append(imageGrid[y*(tileSheet.height/64) + x].get_texture())

    def load(self, fileName, player=None):
        
        if os.path.isfile("maps/"+fileName):
            xmlTree = xml.parse("maps/"+fileName)
            root = xmlTree.getroot()
            
            for child in root:
                self.map.append(Tile( **child.attrib ))
            
            # on place le joueur sur la carte si il est donné en paramètre
            if player:
                player.x = int( root.attrib["playerpos"].split(":")[0] ) * Tile.SIZE
                player.y = int( root.attrib["playerpos"].split(":")[1] ) * Tile.SIZE
        else:
            print "couldn't load the map ["+fileName+"]. No such file."  
                            
    def collide(self, x,y,w,h):
        """
                                == COLlIDE ==
        
        La fonction collide permet de savoir si l'objet défnis par ses
        coordonées et ses dimensions passées en paramètres se trouve
        sur le sol ou non.
        Lorsqu'aucune collision n'est détecté on retourne False
        Si une collision est détectée alors on renvoie True
        
        :param x: Position x de l'objet
        :param y: Position y de l'objet
        :param w: Largeur de l'objet
        :param h: Hauteur de l'objet
        
        :type x: int | float
        :type y: int | float
        :type w: int | float
        :type h: int | float
        
        :rtype: bool
        """
        # One does not simply understand what's written there
        for tile in self.map:
            if tile.collision == True:
                if (tile.x <= x <= tile.x + self.tileSize) or (tile.x <= x+w <= tile.x + self.tileSize):
                    # Si la position gauche (x) ou la position droite (x+w)
                    # est comprise entre le bord gauche et droite de la tile.
                    if (tile.y <= y <= tile.y + self.tileSize) or (tile.y <= y+h <= tile.y + self.tileSize):
                        # Si la position du bas (y) ou la position du haut (y+h) 
                        # est comprise entre le bord haut et le bord bas de la tile.
                        return True
        return False
    
    def render(self):
        pyglet.gl.glEnable(pyglet.gl.GL_TEXTURE_2D)

        
        for tile in self.map:
            if self.xRelative + tile.x > -self.tileSize  and self.xRelative + tile.x < gameEngine.GameEngine.W_WIDTH and self.yRelative + tile.y > -self.tileSize and self.yRelative + tile.y < gameEngine.GameEngine.W_HEIGHT:
                pyglet.gl.glBindTexture(self.textures[tile.texture].target, self.textures[tile.texture].texture.id)
                pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
                pyglet.gl.glTexCoord2i(0,0)
                pyglet.gl.glVertex2i(self.xRelative + tile.x, self.yRelative + tile.y)
                pyglet.gl.glTexCoord2i(1,0)
                pyglet.gl.glVertex2i(self.xRelative + tile.x + self.tileSize, self.yRelative + tile.y)
                pyglet.gl.glTexCoord2i(1,1)
                pyglet.gl.glVertex2i(self.xRelative + tile.x + self.tileSize, self.yRelative + tile.y + self.tileSize)
                pyglet.gl.glTexCoord2i(0,1)
                pyglet.gl.glVertex2i(self.xRelative + tile.x, self.yRelative + tile.y + self.tileSize)
                pyglet.gl.glEnd()
        
        pyglet.gl.glDisable(pyglet.gl.GL_TEXTURE_2D)
            

class Tile:
    SIZE = 64
    
    def __init__(self, x, y, collision, type):
        self.x = int(x) * self.SIZE
        self.y = int(y) * self.SIZE
        self.texture = int(type)
        
        if collision == "True":
            self.collision = True
        else:
            self.collision = False

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
    


        
