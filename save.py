#-*- encoding:utf-8 -*-

import os
import xml.etree.ElementTree as xml


class Save(object):
    def __init__(self):
        # - Default -
        self.lvl = 1
        self.maxHp = 100.0
        self.hp = 100.0
        self.speed = 30.0
        self.shieldCapacity = 50.0
        self.shield = 50.0
        self.fireRate = 10.0
        self.resistance = 100
        self.attack = 10
        self.isMoving = False
        self.mucus = 100
        self.mucusMax = 100
        self.regenMucus = 0.01

        # - Parametres -
        self.fileName = "data/save/save.data"

    def load(self):
        """
        Charge les caractéristiques du joueur ainsi que des infos 
        sur le niveau ou il était rendus. 
        """
        if os.path.isfile(self.fileName):
            self.xml = xml.parse(self.fileName)
            root = self.xml.getroot()
            for child in root:
                if child.tag == "lvl":
                    self.lvl = child.text
                if child.tag == "maxHp":
                    self.maxHp = float(child.text)
                if child.tag == "hp":
                    self.hp = float(child.text)
                if child.tag == "speed":
                    self.speed = float(child.text)
                if child.tag == "shieldCapacity":
                    self.shieldCapacity = float(child.text)
                if child.tag == "shield":
                    self.shield = float(child.text)
                if child.tag == "fireRate":
                    self.fireRate = float(child.text)
                if child.tag == "resistance":
                    self.resistance = float(child.text)
                if child.tag == "attack":
                    self.attack = float(child.text)
                if child.tag == "mucus":
                    self.mucus = float(child.text)
                if child.tag == "mucusMax":
                    self.mucusMax = float(child.text)
                if child.tag == "regenMucus":
                    self.regenMucus = float(child.text)

    def save(self):
        """
        Enregistre les informations du joueur et le niveau auquel il
        est rendus dans un fichier xml.
        """
        
        file = open(self.fileName, "w")
        saveFile = "<?xml version=\"1.0\" ?>\n\
<save>\n\t\
<lvl>" + str(self.lvl) + "</lvl>\n\t\
<maxHp>" + str(self.maxHp) + "</maxHp>\n\t\
<hp>" + str(self.hp) + "</hp>\n\t\
<speed>" + str(self.speed) + "</speed>\n\t\
<shieldCapacity>" + str(self.shieldCapacity) + "</shieldCapacity>\n\t\
<shield>" + str(self.shield) + "</shield>\n\t\
<fireRate>" + str(self.fireRate) + "</fireRate>\n\t\
<resistance>" + str(self.resistance) + "</resistance>\n\t\
<attack>" + str(self.attack) + "</attack>\n\t\
<mucus>" + str(self.mucus) + "</mucus>\n\t\
<mucusMax>" + str(self.mucusMax) + "</mucusMax>\n\t\
<regenMucus>" + str(self.regenMucus) + "</regenMucus>\n\
</save>"

        file.write(saveFile)
