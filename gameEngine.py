# coding=utf-8
import pyglet, game

class GameEngine(pyglet.window.Window):
    W_WIDTH = 1024
    W_HEIGHT = 640
    def __init__(self):
        super(GameEngine, self).__init__(width=self.W_WIDTH, height=self.W_HEIGHT,resizable=False)
        
        self.set_vsync(False)
        self.set_caption("Banana")
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.clock.schedule_interval(lambda x:x, 1/1000000.0) # Debridage complet des FPS
        pyglet.clock.schedule_interval(self.physicEngine, 1/100.0)

        # Input handler        
        self.keysHandler = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keysHandler)
        
        # ===================================== #
        # =              VARIABLES            = #

        self.mainDrawingBatch = pyglet.graphics.Batch()
        self.fpsText = pyglet.text.Label("", x=4, y=self.height, anchor_y="top", batch=self.mainDrawingBatch)
        self.state = "playing"
        self.game = game.Game()
        
    def physicEngine(self, dt):
        if self.state == "playing" and self.game:
            self.game.simulate(dt, self.keysHandler)
        
    
    def on_draw(self):
        self.clear()
        self.fpsText.text = str( round(pyglet.clock.get_fps(), 2) )
        
        if self.state == "playing" and self.game:
            self.game.render()
        
        self.mainDrawingBatch.draw()
    
    def start(self):
        pyglet.app.run()
