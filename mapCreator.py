#-*- encoding:utf-8 -*-

import gameEngine
"""
		== DOCUMENTATION [FR] ==

Controles :
-----------

Z : Aller en haut
S : Aller en bas 
Q : Aller vers la gauche
D : Aller vers la droite
SPACE : Doubler vitesse de déplacement

E : exporter la carte

CLIC GAUCHE : Poser texture selectionnée
CLIC DROITE : Selectionner texture depuis celles déja posés
MOLETTE HAUT: Parcourir texture
MOLETTE BAS : Parcourir texture
"""


import pyglet
import pyglet.window.key as key


# ============================================= #
# =                  SETTINGS                 = #

MAP_NAME="EXPORT"
TILE_SIZE = 64
TILEMAP_IMAGE_PATH = "data/sprites/tile-map.jpg"

W_WIDTH = 1024
W_HEIGHT = 640


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

# ============================================= #

class App(object):
	"""
	============================
	== Main application class ==
	============================
	"""

	def __init__(self):
	
		# - Input handler -
		# self.keysHandler = pyglet.window.key.KeyStateHandler()
		# self.push_handlers(self.keysHandler)

		# - variables -
		self.offsetPos = Pos(-W_WIDTH/2,-W_HEIGHT/2)
		self.camera = Camera()
		self.cursorPos = Pos(0,0)
		self.selectedPos = Pos(0,0)
		self.selectedCase = Pos(0,0)
		self.map = []
		self.textures = TextureList()
		self.textures.loadFromImage(TILEMAP_IMAGE_PATH)
		self.selectedTexture = 10
		self.batch = pyglet.graphics.Batch()
		self.returnState = "creator"

	def refresh(self, dt, keysHandler):
		"""
		Check if the user is pressing movement keys. If he does
		then we update the gloval offsetPos and the camera position
		"""
		# - Acceleration with spacebar -
		if keysHandler[key.SPACE]:
			speed = int(1500 * dt)
		else : speed = int(1000 * dt)

		# - up and down movement -
		if keysHandler[key.Z]:
			self.offsetPos.y += speed
		elif keysHandler[key.S]:
			self.offsetPos.y -= speed

		# - left and right movement -
		if keysHandler[key.Q]:
			self.offsetPos.x -= speed
		elif keysHandler[key.D]:
			self.offsetPos.x += speed

		# - Update camera pos -
		self.camera.setPos(self.offsetPos.x + W_WIDTH/2, self.offsetPos.y + W_HEIGHT/2)

	def render(self):
		"""
		Update screen.
		Daw map, grid, interface, texture selector.
		"""

		# - Display of the map -
		self.batch.draw()

		# - Highlight the selected case -
		pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
		pyglet.gl.glColor4f(1, 1, 1, 0.2)
		pyglet.gl.glVertex2i(self.selectedCase.x * TILE_SIZE, self.selectedCase.y * TILE_SIZE)
		pyglet.gl.glVertex2i(self.selectedCase.x * TILE_SIZE + TILE_SIZE, self.selectedCase.y * TILE_SIZE )
		pyglet.gl.glVertex2i(self.selectedCase.x * TILE_SIZE + TILE_SIZE, self.selectedCase.y * TILE_SIZE + TILE_SIZE)
		pyglet.gl.glVertex2i(self.selectedCase.x * TILE_SIZE, self.selectedCase.y * TILE_SIZE + TILE_SIZE)
		pyglet.gl.glColor4f(1, 1, 1, 1)
		pyglet.gl.glEnd()
		
		# - Display a grid over the map -
		pyglet.gl.glBegin(pyglet.gl.GL_LINES)

		for i in xrange(self.offsetPos.x, self.offsetPos.x + W_WIDTH):
			# we draw all vertical lines with a gap of TILE_SIZE between them
			# according to the offsetPos

			if i % TILE_SIZE == 0:
				# Draw red line on the x=0 pos
				if i == 0:
					pyglet.gl.glColor4f(1, 0, 0, 1)
				else: 
					pyglet.gl.glColor4f(0, 0, 0, 1)

				pyglet.gl.glVertex2i(i, self.offsetPos.y)
				pyglet.gl.glVertex2i(i, self.offsetPos.y + W_HEIGHT)

		for i in xrange(self.offsetPos.y, self.offsetPos.y + W_HEIGHT):
			# Same as previous for loop, but for horizontal lines

			if i % TILE_SIZE == 0:
				# draw a red line on y=0 pos
				if i == 0:
					pyglet.gl.glColor4f(1, 0, 0, 1)
				else: 
					pyglet.gl.glColor4f(0, 0, 0, 1)

				pyglet.gl.glVertex2i(self.offsetPos.x, i)
				pyglet.gl.glVertex2i(self.offsetPos.x + W_WIDTH, i)

		pyglet.gl.glEnd()

		# - Selection panel -
		pyglet.gl.glBegin(pyglet.gl.GL_POLYGON)
		pyglet.gl.glColor4f(0, 0, 0, 0.75)
		pyglet.gl.glVertex2i(self.offsetPos.x, self.offsetPos.y)
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE/2 + 30, self.offsetPos.y)
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE + 15, self.offsetPos.y + W_HEIGHT/2 - TILE_SIZE/2 - 10)
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE + 15, self.offsetPos.y + W_HEIGHT/2 + TILE_SIZE/2 + 10)
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE/2 + 30, self.offsetPos.y + W_HEIGHT)
		pyglet.gl.glVertex2i(self.offsetPos.x, self.offsetPos.y + W_HEIGHT)
		pyglet.gl.glEnd()

		# - selected item background -
		pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
		pyglet.gl.glColor4f(0, 0, 0, 1)
		pyglet.gl.glVertex2i(self.offsetPos.x, self.offsetPos.y + W_HEIGHT/2 - (10 + TILE_SIZE / 2) )
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE + 25, self.offsetPos.y + W_HEIGHT/2 - (10 + TILE_SIZE / 2) )
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE + 25, self.offsetPos.y + W_HEIGHT/2 + (10 + TILE_SIZE / 2))
		pyglet.gl.glVertex2i(self.offsetPos.x, self.offsetPos.y + W_HEIGHT/2 + (10 + TILE_SIZE / 2))
		pyglet.gl.glColor4f(1, 1, 1, 1)
		pyglet.gl.glEnd()

		# - selected item white lines -
		pyglet.gl.glBegin(pyglet.gl.GL_LINE_STRIP)
		pyglet.gl.glColor4f(1, 1, 1, 1)
		pyglet.gl.glVertex2i(self.offsetPos.x, self.offsetPos.y + W_HEIGHT/2 - (10 + TILE_SIZE / 2) )
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE + 25, self.offsetPos.y + W_HEIGHT/2 - (10 + TILE_SIZE / 2) )
		pyglet.gl.glVertex2i(self.offsetPos.x + TILE_SIZE + 25, self.offsetPos.y + W_HEIGHT/2 + (10 + TILE_SIZE / 2))
		pyglet.gl.glVertex2i(self.offsetPos.x, self.offsetPos.y + W_HEIGHT/2 + (10 + TILE_SIZE / 2))
		pyglet.gl.glColor4f(1, 1, 1, 1)
		pyglet.gl.glEnd()

		# - Draw the textures in the selection panel -
		for i in range(self.selectedTexture - 5, self.selectedTexture + 5):
			
			# Draw the 5 previous textures and the 5 next.
			# The folowing condition are here to authorise a complete rotation of the 
			# texture asset, with no gap of any kind.
			if i >= len(self.textures.textures):
				# if index is to big, we fetch the textures from the begining (index 0)
				sprite = pyglet.sprite.Sprite(self.textures.get(i - len(self.textures.textures)))
			elif i < 0 :
				# if index is negative we fetch textures according to the end of the list
				sprite = pyglet.sprite.Sprite(self.textures.get(len(self.textures.textures) + i))
			else :
				sprite = pyglet.sprite.Sprite(self.textures.get(i))

			# Scale down the textures proportinaly to there distance to the selected one.
			sprite.scale =  1 - abs(self.selectedTexture - i) / 10.0
			# Set position
			sprite.x = self.offsetPos.x + 10
			sprite.y = y=self.offsetPos.y + W_HEIGHT / 2 - (self.selectedTexture - i) * (TILE_SIZE + 12) - TILE_SIZE/2 * sprite.scale

			# Draw
			sprite.draw()

		return self.returnState

	def on_mouse_motion(self, x, y, dx, dy):
		"""
		Get selected case when user moves the cursor
		"""
		self.cursorPos.set(x,y)

		selectedPos = Pos(self.offsetPos.x + x , self.offsetPos.y + y)
		selectedPos.x -= selectedPos.x%TILE_SIZE
		selectedPos.y -= selectedPos.y%TILE_SIZE

		# - compute the selected case in fonction of the selectedPos
		self.selectedCase.set(selectedPos.x / TILE_SIZE, selectedPos.y / TILE_SIZE)

	def on_mouse_press(self, x, y, button, modifiers):
		"""
		Add, remove or pick the texture of a tile depending
		on wich mouse button is pressed
		"""
		# -Add or remove a texture from the map -
		if button == pyglet.window.mouse.LEFT:

			if modifiers == 18: # MOD_CTRL doesn't work
				# if CTRl key is pressed, we delete the tile
				for tile in self.map:
					if tile.x == self.selectedCase.x * TILE_SIZE and tile.y == self.selectedCase.y * TILE_SIZE:
						self.map.remove(tile)

			else:
				# If the case as a texture we remove it, and then apply the new one.
				foundTextureID = None
				for tile in self.map:
					if tile.x == self.selectedCase.x * TILE_SIZE and tile.y == self.selectedCase.y * TILE_SIZE:
						if tile.texture != self.selectedTexture:
							self.map.remove(tile)
						else:
							foundTextureID = tile.texture
				
				if foundTextureID is not self.selectedTexture:
					# apply the texture only if case is empty or as not already the same one.
					self.map.append( Tile( self.selectedCase.x, self.selectedCase.y, False, self.selectedTexture, self.textures, self.batch ))
		
		# - Pick texture -
		if button == pyglet.window.mouse.RIGHT:
			for tile in self.map:
				if tile.x == self.selectedCase.x * TILE_SIZE and tile.y == self.selectedCase.y * TILE_SIZE:
					self.selectedTexture = tile.texture

	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		# Call on_mouse_motion when in dragin mod to
		# be able to "paint" the map
		if button == pyglet.window.mouse.LEFT:
			self.on_mouse_motion(x,y,dx,dy)
			self.on_mouse_press(x,y,button, modifiers)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		"""
		Change the selected texture. 
		"""
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
		"""
		Specific action triggered with the keybord.
		"""
		# - Export map -
		if symbol == key.E:
			exportMap(self.map)
			self.offsetPos = Pos(0, 0)
			self.returnState = "menu"

		# - Center position to map origin -
		if symbol == key.O:
			self.offsetPos.set(-W_WIDTH/2,-W_HEIGHT/2)

# ----------------------------------

class Camera:
	"""
	== Camera class ==
	Realise a transformation of the plan to emulate
	a change in the point of view of the map.
	"""
	def __init__(self):
		self.x = 0
		self.y = 0

	def setPos(self, x, y):
		self.x = x
		self.y = y
		pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
		pyglet.gl.glLoadIdentity()
		pyglet.gl.glOrtho(x - W_WIDTH/2, x + W_WIDTH/2, y - W_HEIGHT/2, y + W_HEIGHT/2, -1, 1)
		pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

# ----------------------------------

class Pos(object):
	"""
	== Pos ==
	A simple class for easy position managment.
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def set(self, x,y):
		self.x = x
		self.y = y

# ----------------------------------

class TextureList(object):
	"""
	== Texture List ==
	Load and give acces to all the 
	textures from a specified tile
	sheet.
	"""
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
	"""
	== Tile ==
	Class to handle the tile on the map array
	"""

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
	"""
	== Export Map ==
	Convert the map array into a xml
	file with coordinates in term
	of cases, collision and textures
	informations.
	"""
	# - Computing map size -
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

	# - Remove an eventual negatif offset -
	if minX < 0:
		for tile in map:
			tile.x = tile.x + abs(minX)
	if minY < 0:
		for tile in map:
			tile.y = tile.y + abs(minY)

	# - Export into xml file
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

# # ==================================

# if __name__ == "__main__":
# 	app = App()
# 	app.run()
