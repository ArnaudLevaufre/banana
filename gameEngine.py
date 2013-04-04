# coding=utf-8
import pyglet


class GameEngine(pyglet.window.Window):
    W_WIDTH = 640
    W_HEIGHT = 640
    def __init__(self):
        super(GameEngine, self).__init__(width=self.W_WIDTH, height=self.W_HEIGHT,resizable=False)
        
        self.set_vsync(False)
        self.set_caption("Banana")
        pyglet.clock.schedule_interval(lambda x:x, 1/1000000.0) # Debridage complet des FPS
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        self.serverStarted = False

        # ===================================== #
        # =              VARIABLES            = #
        self.mainDrawingBatch = pyglet.graphics.Batch()
        self.fpsText = pyglet.text.Label("", x=4, y=self.height, anchor_y="top", batch=self.mainDrawingBatch)
    
    def on_draw(self):
        self.clear()
        self.fpsText.text = str( round(pyglet.clock.get_fps(), 2) )
        self.mainDrawingBatch.draw()
    
    def start(self):
        pyglet.app.run()
