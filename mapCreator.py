#-*- encoding:utf-8 -*-

"""
        == DOCUMENTATION [FR] ==

Controles :
-----------

Z : Aller en haut
S : Aller en bas
Q : Aller vers la gauche
D : Aller vers la droite
SPACE : Doubler vitesse de déplacement
TAB : change between map editor and level editor
RETURN : Exporter map/level

CLIC GAUCHE : Poser texture selectionnée
CLIC DROITE : Selectionner texture depuis celles déja posés
MOLETTE HAUT: Parcourir texture
MOLETTE BAS : Parcourir texture
"""


import os
import xml.dom.minidom as xmlParser
import pyglet
import pyglet.window.key as key
import gameEngine


# ============================================= #
# =                  SETTINGS                 = #

MAP_NAME = "EXPORT"

TILE_SIZE = 64
TILEMAP_IMAGE_PATH = "data/sprites/tile-map.jpg"
MAP_DIR_PATH = "data/maps/"
ENNEMIES_DIR_PATH = "data/ennemies/"
W_WIDTH = 1024
W_HEIGHT = 640


COLLISIONABLE = [
"False", "True" , "True" , "False", "True" , "True" , "False", "True",
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
        width, height = gameEngine.getDinamicWindowSize()
        
        self.offsetPos = Pos(-width/2,-height/2)
        self.camera = Camera()
        self.cursorPos = Pos(0,0)
        self.selectedCase = Pos(0,0)
        self.map = []
        self.batch = pyglet.graphics.Batch()
        self.levelBatch = pyglet.graphics.Batch()
        self.returnState = "creator"
        self.focus = None
        self.selectedEditor = "map"
        self.levelItemList = []
        
        # Export Boxes
        self.exportMapBox = ExportBox("map")
        self.exportLevelBox = ExportBox("level")
        
        # Selector
        self.selector = Selector()
        self.selector.selected = 10


    def refresh(self, dt, keysHandler):
        """
        Check if the user is pressing movement keys. If he does
        then we update the gloval offsetPos and the camera position
        """
        width, height = gameEngine.getDinamicWindowSize()

        # - block the update of the offset exporting -
        if not self.exportLevelBox.show and not self.exportMapBox.show:
            
            # - Acceleration with spacebar -
            if keysHandler[key.SPACE]:
                speed = int(1500 * dt)
            else: speed = int(1000 * dt)
    
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
            self.camera.setPos(self.offsetPos.x + width/2, self.offsetPos.y + height/2)

    def render(self):
        """
        Update screen.
        Daw map, grid, interface, texture selector.
        """
        width, height = gameEngine.getDinamicWindowSize()

        self.batch.draw()
        self.levelBatch.draw()

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

        for i in xrange(self.offsetPos.x, self.offsetPos.x + width):
            # we draw all vertical lines with a gap of TILE_SIZE between them
            # according to the offsetPos

            if i % TILE_SIZE == 0:
                # Draw red line on the x=0 pos
                if i == 0:
                    pyglet.gl.glColor4f(1, 0, 0, 1)
                else:
                    pyglet.gl.glColor4f(0, 0, 0, 1)

                pyglet.gl.glVertex2i(i, self.offsetPos.y)
                pyglet.gl.glVertex2i(i, self.offsetPos.y + height)

        for i in xrange(self.offsetPos.y, self.offsetPos.y + height):
            # Same as previous for loop, but for horizontal lines
            if i % TILE_SIZE == 0:
                # draw a red line on y=0 pos
                if i == 0:
                    pyglet.gl.glColor4f(1, 0, 0, 1)
                else:
                    pyglet.gl.glColor4f(0, 0, 0, 1)

                pyglet.gl.glVertex2i(self.offsetPos.x, i)
                pyglet.gl.glVertex2i(self.offsetPos.x + width, i)

        pyglet.gl.glEnd()

        # - Draw the selector -
        self.selector.render(self.offsetPos, self.selectedEditor)
        
        # - Draw the export boxes -
        self.exportLevelBox.render(self.offsetPos.x, self.offsetPos.y)
        self.exportMapBox.render(self.offsetPos.x, self.offsetPos.y)

        return self.returnState
    
    
    def set_focus(self, focus):
        """
        Reset the current focused widget by setting is visibility
        to False and unfocus him by reseting his mark and 
        position (cursor).
        
        set current focused, and the proper pyglet specifications
        to make a widget has the real focus.
        """
        
        # - hide current focused caret -
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0
        
        # - set new caret focused -
        self.focus = focus
        
        # - change it state to visible -
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)


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
        # - Focusing the inputs -
        if self.exportLevelBox.show or self.exportMapBox.show:
            widgets = self.exportLevelBox.widgets if self.exportLevelBox.show else self.exportMapBox.widgets
            
            for widget in widgets:
                if widget.hit_test(x,y, self.offsetPos):
                    self.set_focus(widget)

        # - Mouse event on the map editor -
        elif self.selectedEditor == "map":
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
                            if tile.texture != self.selector.selected:
                                self.map.remove(tile)
                            else:
                                foundTextureID = tile.texture

                    if foundTextureID is not self.selector.selected:
                        # apply the texture only if case is empty or as not already the same one.
                        self.map.append(Tile(self.selectedCase.x, self.selectedCase.y, False, self.selector.selected, self.selector.items["map"], self.batch))

            # - Pick texture -
            if button == pyglet.window.mouse.RIGHT:
                for tile in self.map:
                    if tile.x == self.selectedCase.x * TILE_SIZE and tile.y == self.selectedCase.y * TILE_SIZE:
                        self.selector.selected = tile.texture

        # - Mouse event on the level editor -
        elif self.selectedEditor == "level":
            if button == pyglet.window.mouse.LEFT:
                # - Check if there is already an enemy on that tile, delete it if found one -
                for item in self.levelItemList:
                    if item.x == self.selectedCase.x * TILE_SIZE and item.y == self.selectedCase.y * TILE_SIZE:
                        self.levelItemList.remove(item)

                # get the current selected enemy
                sss = self.selector.selected % len(self.selector.items["level"])
                # shorten the call of getCustom
                c = self.selector.items["level"][sss].getCustom
                # Add an enemy on the level
                self.levelItemList.append( levelEntity(self.selectedCase.x * TILE_SIZE, self.selectedCase.y * TILE_SIZE, c(0), c(1), self.selector.items["level"][sss].id , self.selector.items["level"][sss].image, self.levelBatch ) )


    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.selectedEditor == "map":
            # Call on_mouse_motion when in dragin mod to
            # be able to "paint" the map
            if button == pyglet.window.mouse.LEFT:
                self.on_mouse_motion(x, y, dx, dy)
                self.on_mouse_press(x, y, button, modifiers)


    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # - Change selected item in the selector -
        if scroll_y > 0:
            if self.selector.selected + 1 < len(self.selector.items[self.selectedEditor]):
                self.selector.selected += 1
            else:
                self.selector.selected = 0
        else:
            if self.selector.selected > 0:
                self.selector.selected -= 1
            else:
                self.selector.selected = len(self.selector.items[self.selectedEditor]) - 1


    def on_key_press(self, symbol, modifiers):
        # - Key interaction on the inputs -
        if self.exportMapBox.show:
            if symbol == key.RETURN:
                # close the export menu, then export the map
                self.exportMapBox.toggle()
                self.set_focus(None)
                
                if self.exportMapBox.widgets[0].document.text != "":
                    fixOffset(self.map, self.levelItemList)
                    exportMap(self.map, self.exportMapBox.widgets[0].document.text)
                else:
                    self.exportMapBox.widgets[0].rectangle.vertex_list.colors[:16] = [255, 0, 0, 255] * 4

        # - Change from map editor to level editor -
        elif symbol == key.TAB:
            if self.selectedEditor == "map":
                self.selectedEditor = "level"
            else:
                self.selectedEditor = "map"

        # - Specific action for map editor -
        elif self.selectedEditor == "map":
            # - Export map -
            if symbol == key.ENTER:
                width, height = gameEngine.getDinamicWindowSize()
                
                # - Toggle the state of the exportbox
                self.exportMapBox.toggle() 
            

            # - Center position to map origin -
            if symbol == key.O:
                width, height = gameEngine.getDinamicWindowSize()
                self.offsetPos.set(-width/2, -height/2)



    # - input event listenner on writting - 
    def on_text(self, text):
        if self.focus and self.selectedEditor == "map":
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)
    

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

        width, height = gameEngine.getDinamicWindowSize()
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslated(width/2 - x, height/2 - y, 0)


# ----------------------------------


class Pos(object):
    """
    == Pos ==
    A simple class for easy position managment.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y


# ----------------------------------


class Selector(object):
    def __init__(self):
        self.items = {}
        self.selected = 0
        self.load()
        
    def render(self, offsetPos, state):
        width, height = gameEngine.getDinamicWindowSize()
        
        # - Background Selector -
        pyglet.gl.glBegin(pyglet.gl.GL_POLYGON)
        pyglet.gl.glColor4f(0, 0, 0, 0.75)
        pyglet.gl.glVertex2i(offsetPos.x, offsetPos.y)
        pyglet.gl.glVertex2i(offsetPos.x + TILE_SIZE/2 + 30, offsetPos.y)
        pyglet.gl.glVertex2i(offsetPos.x + TILE_SIZE + 15, offsetPos.y + height/2 - TILE_SIZE/2 - 10)
        pyglet.gl.glVertex2i(offsetPos.x + TILE_SIZE + 15, offsetPos.y + height/2 + TILE_SIZE/2 + 10)
        pyglet.gl.glVertex2i(offsetPos.x + TILE_SIZE/2 + 30, offsetPos.y + height)
        pyglet.gl.glVertex2i(offsetPos.x, offsetPos.y + height)
        pyglet.gl.glEnd()

        # - selected item background -
        pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
        pyglet.gl.glColor4f(0, 0, 0, 1)
        pyglet.gl.glVertex2i(offsetPos.x, offsetPos.y + height/2 - (10 + TILE_SIZE / 2) )
        pyglet.gl.glVertex2i(offsetPos.x + TILE_SIZE + 25, offsetPos.y + height/2 - (10 + TILE_SIZE / 2) )
        pyglet.gl.glVertex2i(offsetPos.x + TILE_SIZE + 25, offsetPos.y + height/2 + (10 + TILE_SIZE / 2))
        pyglet.gl.glVertex2i(offsetPos.x, offsetPos.y + height/2 + (10 + TILE_SIZE / 2))
        pyglet.gl.glColor4f(1, 1, 1, 1)
        pyglet.gl.glEnd()

        # - selected item white lines -
        pyglet.gl.glBegin(pyglet.gl.GL_LINE_STRIP)
        pyglet.gl.glColor4f(1, 1, 1, 1)
        pyglet.gl.glVertex2i(offsetPos.x, offsetPos.y + height/2 - (10 + TILE_SIZE / 2) )
        pyglet.gl.glVertex2i(offsetPos.x + TILE_SIZE + 25, offsetPos.y + height/2 - (10 + TILE_SIZE / 2) )
        pyglet.gl.glVertex2i(offsetPos.x + TILE_SIZE + 25, offsetPos.y + height/2 + (10 + TILE_SIZE / 2))
        pyglet.gl.glVertex2i(offsetPos.x, offsetPos.y + height/2 + (10 + TILE_SIZE / 2))
        pyglet.gl.glColor4f(1, 1, 1, 1)
        pyglet.gl.glEnd()
        
        
        # on récupere les items du selector qui correspondent 
        # a l'éditeur actuel.
        try:
            itemList = self.items[state]
        except:
            return -1
        
        
        # - Draw the textures in the selection panel -
        for i in range(self.selected - 5, self.selected + 6):

            sprite = pyglet.sprite.Sprite( itemList[i % len(itemList)].image )

            # the textures proportinaly to there distance to the selected one.
            sprite.scale =  1 - abs(self.selected - i) / 10.0
            
            # Set position
            sprite.x = offsetPos.x + 10
            sprite.y = offsetPos.y + height / 2 - (self.selected - i) * (TILE_SIZE + 12) - TILE_SIZE/2 * sprite.scale
 
            # Draw
            sprite.draw()


    def load(self):
        # - Chargement des tiles de la map -
        
        tileSheet = pyglet.image.load(TILEMAP_IMAGE_PATH)
        imageGrid = pyglet.image.ImageGrid(tileSheet, tileSheet.width/TILE_SIZE, tileSheet.height / TILE_SIZE)
        array = []
        
        # on réordonne les tiles de maniere plus propre
        # c'est a dire du haut à gauche jusqu'en bas à droite
        for y in range(tileSheet.height/TILE_SIZE - 1, 1, -1):
            for x in range(tileSheet.width/TILE_SIZE):
                array.append( SelectorItem( y*(tileSheet.height/TILE_SIZE) + x, imageGrid[y*(tileSheet.height/TILE_SIZE) + x], "map"))
        
        self.items["map"] = array

        # - Chargement des Types d'enemies -
        
        array = []
        listDir = os.listdir(ENNEMIES_DIR_PATH)
        
        for file in listDir:
            if os.path.isfile( os.path.join( ENNEMIES_DIR_PATH, file)):
                xml    = xmlParser.parse( os.path.join( ENNEMIES_DIR_PATH, file) ).documentElement 
                width  = int( xml.getElementsByTagName("width")[0].firstChild.data )
                height = int( xml.getElementsByTagName("height")[0].firstChild.data )
                
                # - Image Model -
                tileSheet = pyglet.image.load(xml.getElementsByTagName("sprite")[0].firstChild.data)
                images = pyglet.image.ImageGrid(tileSheet, tileSheet.height/height, tileSheet.width / width)
                image = images[len(images) - 1]
                
                array.append( SelectorItem( os.path.basename(file).split(".")[0] , image, "level", width, height) ) # Width and Height are stored in the "customs"
                
        self.items["level"] = array


class SelectorItem(object):
    def __init__(self, id , image, editor, *args):
        self.id= id
        self.image = image
        self.editor = editor
        self.customs = []
        
        for arg in args:
            self.customs.append(arg)        
    
    def getCustom(self, nbr):
        # - return the custom variable nbr if it exists -
        if len(self.customs) > nbr:
            return self.customs[nbr]
        else :
            return None


# ----------------------------------


class levelEntity(object):
    def __init__(self, x, y, width, height, descriptionFile, image , batch):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = descriptionFile
        self.sprite = pyglet.sprite.Sprite(image, batch=batch, x=x, y=y)


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
        self.sprite = pyglet.sprite.Sprite( textures[type].image , batch=batch, x=self.x, y=self.y)

        if collision == "True":
            self.collision = True
        else:
            self.collision = False


# ----------------------------------


class ExportBox(object):
    def __init__(self, type):

        self.batch = pyglet.graphics.Batch()
        self.title = pyglet.text.Label("", batch=self.batch)
        self.fieldsTitle = []
        self.widgets = []
        self.show = False
        
        if type == "map":
            self.title.text = "Export map"
            self.width = 450
            self.height = 100
            self.fieldsTitle.append( pyglet.text.Label("Map name:", batch=self.batch) )
            
            self.widgets = [
                TextWidget('', 0, 0, self.width - 20,self.batch)
                ]
    
    def render(self, editorOffsetX, editorOffsetY):
        
        if self.show:
            width, height = gameEngine.getDinamicWindowSize()
            
            # calculate tu position of the bottom left corner of the box
            boxPos = Pos( editorOffsetX + width/2 - self.width/2, editorOffsetY + height/2 - self.height/2 )
            
            # - update label and sprite pos -
            self.title.x, self.title.y = boxPos.x + 10, boxPos.y + self.height - 25
            for i in xrange(len(self.fieldsTitle) ):
                self.fieldsTitle[i].x = boxPos.x + 10
                self.fieldsTitle[i].y = boxPos.y + self.height - i * 50 - 50
            
            for i in xrange(len(self.widgets)):
                self.widgets[i].updatePos(boxPos.x + 10, boxPos.y + self.height - i * 50 - 75)
                
            # - Draw the background box -
            pyglet.gl.glColor4f(0,0,0,0.5)
            pyglet.gl.glBegin(pyglet.gl.GL_QUADS)
            pyglet.gl.glVertex2i(boxPos.x, boxPos.y)
            pyglet.gl.glVertex2i(boxPos.x + self.width, boxPos.y)
            pyglet.gl.glVertex2i(boxPos.x + self.width, boxPos.y + self.height)
            pyglet.gl.glVertex2i(boxPos.x, boxPos.y + self.height)
            pyglet.gl.glEnd()
            
            self.batch.draw()
        
    def toggle(self):
        self.show = not self.show


# ----------------------------------


def exportLvl(name, nextName=None, cinName=None):
    """ 
    === Export Lvl ===
    Exporte le niveau associé à la map
    """
    file = open("data/lvl/" + name, "w+")
    file.write("<?xml version=\"1.0\" ?>\n")
    file.write("<init>\n")
    if cinName is not None:
        file.write("\t<cinematique file=\"data/cin/"+cinName+".xml\" />\n")
    if nextName is not None:
        file.write("\t<next level=\""+nextName+"\" />\n")
    file.write("\t<player skin=\"blarg.png\" x=\"3\" y=\"3\" <idth=\"48\" height=\"48\" />\n")
    file.write("\t<map name=\""+name+"\" />\n")
    file.write("</init>\n")


def fixOffset(map, items):
    """
    === Fix offset ==
    Must be called before exporting map (maybe level)
    """
    # - Computing map size -
    minX = 0
    minY = 0

    for tile in map:
        if tile.x < minX:
            minX = tile.x
        if tile.y < minY:
            minY = tile.y

    if minX != 0:
        for tile in map:
            tile.x -= minX
            tile.sprite.x -= minX
        for item in items:
            item.x -= minX
            item.sprite.x -= minX
              
    if minY != 0:
        for tile in map:
            tile.y -= minY
            tile.sprite.y -= minY
        for item in items:
            item.y -= minX
            item.sprite.y -= minY


# ----------------------------------


def exportMap(map, mapName=MAP_NAME):
    """
    == Export Map ==
    Convert the map array into a xml
    file with coordinates in term
    of cases, collision and textures
    informations.
    """
    # - Calculate the width of the map -
    width = 0
    height = 0
    for tile in map:
        if tile.x > width:
            width = tile.x
        if tile.y > height:
            height = tile.y
    
    # - Export into xml file
    try:
        file = open("data/maps/" + mapName, "w+")
        file.write("<?xml version=\"1.0\" ?>\n")
        file.write("<map sizeX=\"%i\" sizeY=\"%i\">\n" % (width/TILE_SIZE, height/TILE_SIZE))

        for tile in map:
            file.write("\t<tile x=\"%i\" y=\"%i\" collision=\"%s\" type=\"%i\" />\n" % (tile.x / TILE_SIZE, tile.y / TILE_SIZE, COLLISIONABLE[tile.texture], tile.texture))

        file.write("</map>\n")
        print "Map succesfully exported as " + mapName

    except:
        print "Error while exporting map."


# ----------------------------------


class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )
    
    def updatePos(self, x,y, width, height):
        self.vertex_list.vertices = [x, y, x + width, y, x + width, y + height, x, y + height]


# ----------------------------------


class TextWidget(object):
    """
    Class to handle text input.
    Almost copy/paste from the documentation
    """
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text), dict(color=(0, 0, 0, 255)) )
        font = self.document.get_font()
        
        self.width = width
        self.height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, self.width, self.height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad, x + width + pad, y + self.height + pad, batch)

    def hit_test(self, x, y, offset):
        width, height = gameEngine.getDinamicWindowSize()
        sl = self.layout
        ox = offset.x
        oy = offset.y
        return (sl.x - ox < x < sl.x - ox + sl.width and sl.y - oy < y < sl.y - oy + sl.height)
        
    def updatePos(self, x,y):
        self.layout.x = x
        self.layout.y = y
        
        self.caret.x = x
        self.caret.y = y
        
        self.rectangle.updatePos(x,y, self.width, self.height)
