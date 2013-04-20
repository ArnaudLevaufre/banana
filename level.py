import math, os
import xml.dom.minidom as xmlParser
import entity, cinematic, map

class Level(object):
    def __init__(self):
        self.player = None
        self.map = map.Map()
        self.cinematique = None
        self.enemies = []
        self.chests = []
        self.items = []
        self.entity = []
        self.nextLevel = ""
                
    def next(self):
        self.load(self.nextLevel)
        
    def load(self, fileName):
        if os.path.isfile("lvl/"+fileName):
            xml = xmlParser.parse("lvl/"+fileName).documentElement
            
            # - Chargement des parametres du niveau - 
            try:                
                # - Chargement des informations -
                xmlPlayerNode       = xml.getElementsByTagName("player")[0]
                self.player         = entity.Player( int(xmlPlayerNode.getAttribute("x")) * map.Tile.SIZE, int(xmlPlayerNode.getAttribute("y")) * map.Tile.SIZE)
                self.cinematique    = cinematic.Cinematic(xml.getElementsByTagName("cinematique")[0].getAttribute("file"))
                self.nextLevelName  = xml.getElementsByTagName("next")[0].getAttribute("level")
                self.map.load( xml.getElementsByTagName("map")[0].getAttribute("name") )
                
                enemies = xml.getElementsByTagName("enemy")
                for e in enemies:
                    self.enemies.append(entity.Enemy(int(e.getAttribute("x")) * map.Tile.SIZE, int(e.getAttribute("y")) * map.Tile.SIZE) )
                
                
            except:
                print "Congratulation! You fail your level editing.\nNow the rules has changed! You must find your mistake to win the game!"
