#-*- encoding: utf-8 -*-

import gameEngine

"""
                        ====================
                        ==  Banana Quest  ==
                        ====================
PRINCIPE DU JEU:
    Le joueur incarne un Blarg, petit créature verte et gélativeuse qui
    devra parcourir différent mondes générés aléatoirements afin de battre
    des boss qui droperons les pieces d'un médaillon qu'il faut assembler
    pour terminer le jeux.

HISTOIRE:
    La princesse "x" posséder par le Démon se tranforme en immonde créature.
    Vous entendez parler d'un médaillon légendaire vous permettant de lui redonner
    forme blarg. Impavide vous vous élancez dans une longue quette permettant de
    réunir les pieces permetant d'assembler le médaillon. 

                        ====================
"""


if __name__ == "__main__":
    game = gameEngine.GameEngine()
    game.start()
    