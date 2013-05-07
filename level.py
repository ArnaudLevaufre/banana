import os
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
        if os.path.isfile("data/lvl/"+fileName):
            xml = xmlParser.parse("data/lvl/"+fileName).documentElement
            
            # - Chargement des parametres du niveau -              
            # - Chargement des informations -
            xmlPlayerNode       = xml.getElementsByTagName("player")[0]
            self.player         = entity.Player( int(xmlPlayerNode.getAttribute("x")) * map.Tile.SIZE +32, int(xmlPlayerNode.getAttribute("y")) * map.Tile.SIZE +32)
            self.cinematique    = cinematic.Cinematic(xml.getElementsByTagName("cinematique")[0].getAttribute("file"))
            self.nextLevelName  = xml.getElementsByTagName("next")[0].getAttribute("level")
            self.map.load( xml.getElementsByTagName("map")[0].getAttribute("name") )
            
            enemies = xml.getElementsByTagName("enemy")
            for e in enemies:
                self.enemies.append(entity.Enemy(int(e.getAttribute("x")) * map.Tile.SIZE +32, int(e.getAttribute("y")) * map.Tile.SIZE +32, self.map ) )