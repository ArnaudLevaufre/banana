# coding=utf-8
import pyglet
import cinematic
import game
import menu

class GameEngine(pyglet.window.Window):
    # Constantes de la fenetre
    W_WIDTH = 1024
    W_HEIGHT = 640
    
    def __init__(self):
        
        super(GameEngine, self).__init__(width=self.W_WIDTH, height=self.W_HEIGHT,resizable=False)
        
        self.set_vsync(False)
        self.set_caption("Blarg")
        pyglet.clock.schedule_interval(lambda x:x, 1/100000000.0) # Debridage complet des FPS
        pyglet.clock.schedule_interval(self.physicEngine, 1/100.0)
        
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glClearColor(0.5,0.75,1,1)
        

        # Input handler        
        self.keysHandler = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keysHandler)
        
        # ===================================== #
        # =              VARIABLES            = #

        self.mainDrawingBatch = pyglet.graphics.Batch()
        self._state = "playing"
        self._lvl = 1
        self._menu = menu.MainMenu()
        self._game = game.Game()
        self._cin = cinematic.Cinematic()
        self.fpsText = pyglet.text.Label("", x=4, y=self.height, anchor_y="top", batch=self.mainDrawingBatch, color=(0,0,0,255))
        self.set_mouse_cursor(pyglet.window.ImageMouseCursor(pyglet.image.load('sprites/vis.png'), 8, 8))
        
    def physicEngine(self, dt):
        if self._state == "playing" and self._game:
            self._game.simulate(dt, self.keysHandler)
    
    def on_draw(self):
        self.clear()
        self.fpsText.text = str( round(pyglet.clock.get_fps(), 2) )
        
        if self._state == "askForCin":
            self._cin = cinematic.Cinematic()
            self._state = "cin"
        elif self._state == "cin":
            if self._cin.run() == False:
                self._state = "askForMap"
                self._state = "playing"
        elif self._state == "askForMenu":
            self._menu = menu.MainMenu()
            self._state = "menu"
        elif self._state == "menu":
            self._state = self._menu.render()
        elif self._state == "quit":
            self.close()
            
        if self._state == "playing" and self._game:
            self._game.render()
        
        self.fps =  round(pyglet.clock.get_fps(), 2) +0.1
        self.mainDrawingBatch.draw()
        
    def on_mouse_press(self,x, y, button, modifiers):
        if self._state == "playing":
            self._game.on_mouse_press(x,y,button,modifiers)
        elif self._state == "menu":
            self._menu.on_mouse_press(x,y,button,modifiers)


    def on_mouse_release(self,x, y, button, modifiers):
        if self._state == "playing":
            self._game.on_mouse_release(x, y, button, modifiers)
        
        
    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        if self._state == "playing":
            self._game.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
            
    def on_mouse_motion(self,x, y, dx, dy):
        if self._state == "menu":
            self._menu.on_mouse_motion(x, y, dx, dy)
        
    def start(self):
        pyglet.app.run()
