import pygame  # Bibliothèque pygame pour gérer le jeu, et sys pour gérer la fermeture de la fenêtre
from Settings import *  # Importation des paramètres prédéfinis 
from Player import *
from Enemy import Monstre  # Importation de la classe Monstre
from Spectre import Spectre  # Import de classe Spectre



class CreateLevel():
    def __init__(self,LevelName,Screen):
        self.level_name=LevelName
        if self.level_name=="game_level":
            self.screen=Screen
            self.player = Player(100, HEIGHT - 100)  # Instance du joueur
            self.monstre = Monstre(500, HEIGHT - 100)  # Instance d'un monstre
            self.spectre = Spectre(400,500) #Instance d'un spectre

    def run(self, keys):
        self.player.update(keys, GRAVITY, HEIGHT)  # Mise à jour du joueur
        self.monstre.update(self.player, GRAVITY, HEIGHT)  # Mise à jour du monstre
        self.spectre.update(self.player, GRAVITY, HEIGHT) #Mise a jour du spectre
        
        self.player.draw(self.screen)  # Dessine le joueur
        self.monstre.draw(self.screen)  # Dessine le monstre
        self.spectre.draw(self.screen) # Dessine le spectre