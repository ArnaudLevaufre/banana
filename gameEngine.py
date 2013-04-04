# coding=utf-8
import pyglet
import cinematic
class GameEngine(pyglet.window.Window):
    W_WIDTH = 640
    W_HEIGHT = 640
    def __init__(self):
        super(GameEngine, self).__init__(width=self.W_WIDTH, height=self.W_HEIGHT,resizable=False)
        
        self.set_vsync(False)
        self.set_caption("Banana")
        pyglet.clock.schedule_interval(lambda x:x, 1/1000000.0) # Debridage complet des FPS
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        self.state = "cin"

        # ===================================== #
        # =              VARIABLES            = #
        self.mainDrawingBatch = pyglet.graphics.Batch()
        self.fpsText = pyglet.text.Label("", x=4, y=self.height, anchor_y="top", batch=self.mainDrawingBatch, color=(0,0,0,255))
        self.background = pyglet.image.create(self.width, self.height, pyglet.image.SolidColorImagePattern((255,255,255,255))) # Background
        self.cin = cinematic.Cinematic()
    def on_draw(self):
        self.clear()
        self.background.blit(0,0)
        if(self.state == "cin"):
            self.cin.run()

        self.mainDrawingBatch.draw()
    
    def start(self):
        pyglet.app.run()
