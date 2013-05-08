#-*- encoding: utf-8 -*-

import gameEngine

"""
                        ====================
                        ==  Banana Quest  ==
                        ====================
PRINCIPE DU JEU:
    Le joueur incarne un Blarg, petit créature verte et gélatineuse qui
    devra parcourir différents mondes générés aléatoirements afin de battre
    des boss qui droperont les pièces d'un médaillon qu'il faut assembler
    pour terminer le jeu.

HISTOIRE:
    La princesse "x" possédée par le Démon se tranforme en immonde créature.
    Vous entendez parler d'un médaillon légendaire vous permettant de lui redonner
    forme blarg. Impavide vous vous élancez dans une longue quete permettant de
    réunir les pieces permettant d'assembler le médaillon.

                        ====================
"""


if __name__ == "__main__":
    game = gameEngine.GameEngine()
    game.start()
