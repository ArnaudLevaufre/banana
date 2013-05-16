import os
import xml.dom.minidom as xmlParser
import entity
import cinematic
import map
import item
import IA


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

            # - Chargement des informations -
            xmlPlayerNode = xml.getElementsByTagName("player")[0]
            self.player = entity.Player(int(xmlPlayerNode.getAttribute("x")) * map.Tile.SIZE + 32, int(xmlPlayerNode.getAttribute("y")) * map.Tile.SIZE + 32)
            self.cinematique = cinematic.Cinematic(xml.getElementsByTagName("cinematique")[0].getAttribute("file"))
            self.nextLevelName = xml.getElementsByTagName("next")[0].getAttribute("level")
            self.map.load(xml.getElementsByTagName("map")[0].getAttribute("name"))
            # GRIDMAP Pour l'IA
            self.gridMap = IA.GridMap(self.map.sizeX+1, self.map.sizeY+1)

            for b in self.map.collidable:
                self.gridMap.set_blocked(b)

            self.suc = {}
            for i in xrange(self.map.sizeX+1):
                self.suc[i] = {}
                for j in xrange(self.map.sizeY+1):
                    self.suc[i][j] = self.gridMap.successors((i, j))

            enemies = xml.getElementsByTagName("enemy")
            for e in enemies:
                self.enemies.append(entity.Enemy(int(e.getAttribute("x")) * map.Tile.SIZE + 32, int(e.getAttribute("y")) * map.Tile.SIZE + 32, e.getAttribute("type"), self.map, self.gridMap, self.suc))

            items = xml.getElementsByTagName("chest")
            for i in items:
                self.items.append(item.Item(int(i.getAttribute("x")) * map.Tile.SIZE + 32, int(i.getAttribute("y")) * map.Tile.SIZE + 32, "chest", 1))
