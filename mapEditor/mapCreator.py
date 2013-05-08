#-*- encoding:utf-8 -*-

import pyglet
import pyglet.window.key as key

# ============================================ #
# =                 SETTINGS                 = #

MAP_NAME="EXPORT"
TILE_SIZE = 64
TILEMAP_IMAGE_PATH = "../data/sprites/tile-map.jpg"


COLLISIONABLE = [
"False", "True", "True", "False", "False", "False", "False", "False",
"False", "False", "False", "False", "False", "False", "False", "False",
"False", "False", "False", "False", "False", "False", "False", "False",
"False", "False", "False", "False", "False", "False", "False", "False",
"False", "False", "False", "False", "False", "False", "False", "False",
"False", "False", "False", "False", "False", "False", "False", "False",
"False", "False", "False", "False", "False", "False", "False", "False",
"False", "False", "False", "False", "False", "False", "False", "False",
]


class App(pyglet.window.Window):
	W_WIDTH = 1280
	W_HEIGHT = 720

	def __init__(self):
		super(App, self).__init__()
		self.set_size(self.W_WIDTH,self.W_HEIGHT)

		# - refresh screen and input.
		pyglet.clock.schedule_interval(self.refresh, 1/100.0)


		# - Input handler -
		self.keysHandler = pyglet.window.key.KeyStateHandler()
		self.push_handlers(self.keysHandler)

		# - variables -
		self.offsetPos = Pos(0,0)
		self.camera = Camera()
		self.cursorPos = Pos(0,0)
		self.selectedPos = Pos(0,0)
		self.selectedCase = Pos(0,0) # type pos mais enfait il s'agira de corrdonées de tableaux
		self.map = []
		self.textures = TextureList()
		self.textures.loadFromImage(TILEMAP_IMAGE_PATH)
		self.selectedTexture = 10

		# - batchs et autre options graphiques
		pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
		pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
		pyglet.gl.glClearColor(0.5, 0.75, 1, 1)


		self.batch = pyglet.graphics.Batch()

	def refresh(self, dx):
		if self.keysHandler[key.Z]:
			self.offsetPos.y += 10
		elif self.keysHandler[key.S]:
			self.offsetPos.y -= 10

		if self.keysHandler[key.Q]:
			self.offsetPos.x -= 10
		elif self.keysHandler[key.D]:
			self.offsetPos.x += 10

		# mise a jour de la position de la camera.
		self.camera.setPos(self.offsetPos.x + self.W_WIDTH/2, self.offsetPos.y + self.W_HEIGHT/2)

	def on_draw(self):
		self.clear()


		# - Tracé de la grille -
		
		pyglet.gl.glBegin(pyglet.gl.GL_LINES)

		for i in xrange(self.offsetPos.x, self.offsetPos.x + self.W_WIDTH):
			if i % TILE_SIZE == 0:
				# Ligne rouge en x = 0
				if i == 0:
					pyglet.gl.glColor4f(1, 0, 0, 1)
				else: 
					pyglet.gl.glColor4f(0, 0, 0, 1)

				pyglet.gl.glVertex2i(i, self.offsetPos.y)
				pyglet.gl.glVertex2i(i, self.offsetPos.y + self.W_HEIGHT)

		for i in xrange(self.offsetPos.y, self.offsetPos.y + self.W_HEIGHT):
			if i % TILE_SIZE == 0:
				# ligne rouge en y = 0
				if i == 0:
					pyglet.gl.glColor4f(1, 0, 0, 1)
				else: 
					pyglet.gl.glColor4f(0, 0, 0, 1)

				pyglet.gl.glVertex2i(self.offsetPos.x, i)
				pyglet.gl.glVertex2i(self.offsetPos.x + self.W_WIDTH, i)

		pyglet.gl.glEnd()

		# render de la map
		self.batch.draw()

		# Highlight de la case selectionnée.
		
		pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
		pyglet.gl.glColor4f(1, 1, 1, 0.2)
		pyglet.gl.glVertex2i(self.selectedCase.x * TILE_SIZE, self.selectedCase.y * TILE_SIZE)
		pyglet.gl.glVertex2i(self.selectedCase.x * TILE_SIZE + TILE_SIZE, self.selectedCase.y * TILE_SIZE )
		pyglet.gl.glVertex2i(self.selectedCase.x * TILE_SIZE + TILE_SIZE, self.selectedCase.y * TILE_SIZE + TILE_SIZE)
		pyglet.gl.glVertex2i(self.selectedCase.x * TILE_SIZE, self.selectedCase.y * TILE_SIZE + TILE_SIZE)
		pyglet.gl.glColor4f(1, 1, 1, 1)
		pyglet.gl.glEnd()


		# Draw selected texture.

		pyglet.gl.glBegin(pyglet.gl.GL_POLYGON)
		pyglet.gl.glColor4f(0, 0, 0, 0.75)
		pyglet.gl.glVertex2i(self.offsetPos.x, self.offsetPos.y)
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE/2 + 30, self.offsetPos.y)
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE + 25, self.offsetPos.y + self.W_HEIGHT/2 - TILE_SIZE/2 - 10)
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE + 25, self.offsetPos.y + self.W_HEIGHT/2 + TILE_SIZE/2 + 10)
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE/2 + 30, self.offsetPos.y + self.W_HEIGHT)
		pyglet.gl.glVertex2i(self.offsetPos.x, self.offsetPos.y + self.W_HEIGHT)
		pyglet.gl.glEnd()

		pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
		pyglet.gl.glColor4f(0, 0, 0, 1)
		pyglet.gl.glVertex2i(self.offsetPos.x, self.offsetPos.y + self.W_HEIGHT/2 - (10 + TILE_SIZE / 2) )
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE + 25, self.offsetPos.y + self.W_HEIGHT/2 - (10 + TILE_SIZE / 2) )
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE + 25, self.offsetPos.y + self.W_HEIGHT/2 + (10 + TILE_SIZE / 2))
		pyglet.gl.glVertex2i(self.offsetPos.x, self.offsetPos.y + self.W_HEIGHT/2 + (10 + TILE_SIZE / 2))
		pyglet.gl.glColor4f(1, 1, 1, 1)
		pyglet.gl.glEnd()

		for i in range(self.selectedTexture - 5, self.selectedTexture + 5):
			if i >= len(self.textures.textures):
				sprite = pyglet.sprite.Sprite(self.textures.get(i - len(self.textures.textures)))
			elif i < 0 :
				sprite = pyglet.sprite.Sprite(self.textures.get(len(self.textures.textures) + i))
			else :
				sprite = pyglet.sprite.Sprite(self.textures.get(i))

			sprite.scale =  1 - abs(self.selectedTexture - i) / 10.0
			sprite.x = self.offsetPos.x + 10
			sprite.y = y=self.offsetPos.y + self.W_HEIGHT / 2 - (self.selectedTexture - i) * (TILE_SIZE + 12) - TILE_SIZE/2 * sprite.scale
			sprite.draw()
	

	def on_mouse_motion(self, x, y, dx, dy):
		self.cursorPos.set(x,y)

		selectedPos = Pos(self.offsetPos.x + self.cursorPos.x , self.offsetPos.y + self.cursorPos.y)
		selectedPos.x -= selectedPos.x%TILE_SIZE
		selectedPos.y -= selectedPos.y%TILE_SIZE

		# calcul de la case selectionnée en fonction de sa position.
		self.selectedCase.set(selectedPos.x / TILE_SIZE, selectedPos.y / TILE_SIZE)

	def on_mouse_press(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT:

			# On check si il n'y a pas déja une tile, et on la surpprime si c'est le cas
			for tile in self.map:
				if tile.x == self.selectedCase.x * TILE_SIZE and tile.y == self.selectedCase.y * TILE_SIZE:
					self.map.remove(tile)
			
			self.map.append( Tile( self.selectedCase.x, self.selectedCase.y, False, self.selectedTexture, self.textures, self.batch ))
		
		if button == pyglet.window.mouse.RIGHT:
			for tile in self.map:
				if tile.x == self.selectedCase.x * TILE_SIZE and tile.y == self.selectedCase.y * TILE_SIZE:
					self.selectedTexture = tile.texture

	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if button == pyglet.window.mouse.LEFT:
			self.on_mouse_motion(x,y,dx,dy)
			self.on_mouse_press(x,y,button, modifiers)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if scroll_y > 0:
			if self.selectedTexture + 1 < len(self.textures.textures) :
				self.selectedTexture += 1
			else:
				self.selectedTexture = 0
		else:
			if self.selectedTexture > 0 :
				self.selectedTexture -= 1
			else:
				self.selectedTexture = len(self.textures.textures) - 1

	def on_key_press(self, symbol, modifiers):
		if symbol == key.E:
			exportMap(self.map)

	def run(self):
		pyglet.app.run()

# ----------------------------------

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def setPos(self, x, y):
        self.x = x
        self.y = y
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glOrtho(x - app.W_WIDTH/2, x + app.W_WIDTH/2, y - app.W_HEIGHT/2, y + app.W_HEIGHT/2, -1, 1)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

# ----------------------------------

class Pos(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def set(self, x,y):
		self.x = x
		self.y = y

# ----------------------------------

class TextureList(object):
	def __init__(self):
		self.textures = []

	def loadFromImage(self, imagePath):
		tileSheet = pyglet.image.load(imagePath)
		imageGrid = pyglet.image.ImageGrid(tileSheet, tileSheet.width/64, tileSheet.height / 64)

		# on réordonne les tiles de maniere plus propre
		# c'est a dire du haut à gauche jusqu'en bas à droite
		for y in range(tileSheet.height/64 - 1, 1, -1):
			for x in range(tileSheet.width/64):
				self.textures.append(imageGrid[y*(tileSheet.height/64) + x])

	def get(self, nbr):
		return self.textures[nbr]

# ----------------------------------

class Tile:
    def __init__(self, x, y, collision, type, textures, batch):
        self.x = int(x) * TILE_SIZE
        self.y = int(y) * TILE_SIZE
        self.texture = int(type)
        self.sprite = pyglet.sprite.Sprite(textures.get(type), batch=batch, x=self.x, y=self.y)

        if collision == "True":
            self.collision = True
        else:
            self.collision = False

# ----------------------------------


def exportMap(map, mapName=MAP_NAME):

	# - Calcul de la taille de la map -
	minX = 0
	maxX = 0
	minY = 0
	maxY = 0

	for tile in map:
		if tile.x < minX:
			minX = tile.x
		elif tile.x > maxX:
			maxX = tile.x

		if tile.y < minY:
			minY = tile.y
		elif tile.y > maxY:
			maxY = tile.y

	# - Superession d'éventuel ofset -
	if minX < 0:
		for tile in map:
			tile.x = tile.x + abs(minX)

	if minY < 0:
		for tile in map:
			tile.y = tile.y + abs(minY)

	# - export en fichier xml -

	try:
		file = open(mapName, "w+")
		file.write("<?xml version=\"1.0\" ?>\n")
		file.write("<map sizeX=\"%i\" sizeY=\"%i\">\n" % ( (maxX - minX)/TILE_SIZE, (maxY - minY)/TILE_SIZE ) )

		for tile in map:
			file.write("\t<tile x=\"%i\" y=\"%i\" collision=\"%s\" type=\"%i\" />\n" % (tile.x / TILE_SIZE, tile.y / TILE_SIZE, COLLISIONABLE[tile.texture], tile.texture))

		file.write("</map>\n")
		print "Map succesfully exported as " + mapName

	except:
		print "Error while exporting map."



if __name__ == "__main__":
	app = App()
	app.run()
