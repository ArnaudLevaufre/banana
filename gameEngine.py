# coding=utf-8
import pyglet
import cinematic 
import game
import menu
class GameEngine(pyglet.window.Window):
    W_WIDTH = 1024
    W_HEIGHT = 640
    def __init__(self):
        super(GameEngine, self).__init__(width=self.W_WIDTH, height=self.W_HEIGHT,resizable=False)
        
        self.set_vsync(False)
        self.set_caption("Banana")
        pyglet.clock.schedule_interval(lambda x:x, 1/1000000.0) # Debridage complet des FPS
        pyglet.clock.schedule_interval(self.physicEngine, 1/100.0)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        

        # Input handler        
        self.keysHandler = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keysHandler)
        
        # ===================================== #
        # =              VARIABLES            = #

        self.mainDrawingBatch = pyglet.graphics.Batch()
        self.state = "askForMenu"
        self.lvl = 1
        
        self.game = game.Game()
        self.cin = cinematic.Cinematic()
        self.fpsText = pyglet.text.Label("", x=4, y=self.height, anchor_y="top", batch=self.mainDrawingBatch, color=(0,0,0,255))
        image = pyglet.image.load('sprites/vis.png')    
        self.cursor = pyglet.window.ImageMouseCursor(image, 8, 8)
        self.set_mouse_cursor(self.cursor)
        
    def physicEngine(self, dt):
        if self.state == "playing" and self.game:
            self.game.simulate(dt, self.keysHandler)
         
    
    def on_draw(self):
        self.clear()
        pyglet.gl.glClearColor(0.5,0.75,1,1)
        self.fpsText.text = str( round(pyglet.clock.get_fps(), 2) )
        
        if self.state == "askForCin":
            self.cin = cinematic.Cinematic()
            self.state = "cin"
        elif self.state == "cin":
            if self.cin.run() == False:
                self.state = "askForMap"
                self.state = "playing"
        elif self.state == "askForMenu":
            self.menu = menu.MainMenu()
            self.state = "menu"
        elif self.state == "menu":
            self.state = self.menu.render()
        elif self.state == "quit":
            self.close()
            
        if self.state == "playing" and self.game:
            self.game.render()
        
        self.fps =  round(pyglet.clock.get_fps(), 2) +0.1
        self.mainDrawingBatch.draw()
        
    def on_mouse_press(self,x, y, button, modifiers):
        if self.state == "playing":
            self.game.on_mouse_press(x,y,button,modifiers)
        elif self.state == "menu":
            self.menu.on_mouse_press(x,y,button,modifiers)
            
    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        if self.state == "playing":
            self.game.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
            
    def on_mouse_motion(self,x, y, dx, dy):
        if self.state == "menu":
            self.menu.on_mouse_motion(x, y, dx, dy)
        
    def start(self):
        pyglet.app.run()
