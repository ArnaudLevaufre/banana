# -*- encoding:utf-8 -*-

import os
import xml.dom.minidom as xmlParser
import entity
import cinematic
import map
import item
import IA


class Level(object):
    """
    Classe de gestion des niveaux
    """

    def __init__(self):
        """ Le constructeur initialise tout les éléments du jeu """

        self.player = None
        self.map = map.Map()
        self.cinematique = None
        self.enemies = []
        self.chests = []
        self.items = []
        self.entity = []
        self.nextLevel = ""

        self.campaign = True

    def load(self, fileName):
        """
        Charge le niveau depuis un fichier xml de nom fileName
        """

        # Selection des chemin de fichier celon si on est en mode campagne ou non
        if self.campaign:
            self.baseLvlPath = "data/lvl/campaign/"
            self.baseCinPath = "data/cin/campaign/"
            self.baseMapPath = "data/maps/campaign/"
        else:
            self.baseLvlPath = "data/lvl/"
            self.baseCinPath = "data/cin/"
            self.baseMapPath = "data/maps/"

        if os.path.isfile(self.baseLvlPath+fileName):
            xml = xmlParser.parse(self.baseLvlPath+fileName).documentElement
            # - Chargement des informations -
            xmlPlayerNode = xml.getElementsByTagName("player")[0]
            self.player = entity.Player(int(xmlPlayerNode.getAttribute("x")) * map.Tile.SIZE + 32, int(xmlPlayerNode.getAttribute("y")) * map.Tile.SIZE + 32)
            self.cinematique = cinematic.Cinematic(self.baseCinPath + xml.getElementsByTagName("cinematique")[0].getAttribute("file"))
            self.nextLevel = xml.getElementsByTagName("next")[0].getAttribute("level")
            self.map.load(self.baseMapPath + xml.getElementsByTagName("map")[0].getAttribute("name"))

            # GRIDMAP Pour l'IA
            self.gridMap = IA.GridMap(self.map.sizeX+1, self.map.sizeY+1)
            for b in self.map.collidable:
                self.gridMap.set_blocked(b)

            # calcul des successeurs
            self.suc = {}
            for i in xrange(self.map.sizeX+1):
                self.suc[i] = {}
                for j in xrange(self.map.sizeY+1):
                    self.suc[i][j] = self.gridMap.successors((i, j))

            # récupération des ennemies
            enemies = xml.getElementsByTagName("enemy")
            for e in enemies:
                self.enemies.append(entity.Enemy(int(e.getAttribute("x")) * map.Tile.SIZE + 32, int(e.getAttribute("y")) * map.Tile.SIZE + 32, e.getAttribute("type"), self.map, self.gridMap, self.suc))

            # récupération des coffres
            items = xml.getElementsByTagName("chest")
            for i in items:
                self.items.append(item.Item(int(i.getAttribute("x")) * map.Tile.SIZE + 32, int(i.getAttribute("y")) * map.Tile.SIZE + 32, "chest", 1))
