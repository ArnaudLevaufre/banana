import os
import xml.etree.ElementTree as xml


class Save(object):
    def __init__(self):
        self.lvl = 1

    def load(self):
        self.fileName = "data/save/save.data"
        if os.path.isfile(self.fileName):
            self.xml = xml.parse(self.fileName)
            root = self.xml.getroot()
            for child in root:
                if child.tag == "lvl":
                    self.lvl = child.text
