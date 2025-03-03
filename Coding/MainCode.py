import pygame, sys  # Importation des bibliothèques nécessaires
from Settings import *  # Importation des paramètres prédéfinis
from Level import *  # Importation du module Level, qui gère la carte et les entités
from Player import *  # Importation du module Player
from Enemy import Monstre  # Importation de la classe Monstre
from Spectre import Spectre  # Importation de la classe Spectre

"""
CreateGame est la classe principale qui permet de lancer le jeu.
Elle gère l'initialisation de la fenêtre, le chargement des niveaux et la boucle principale du jeu.
"""

class CreateGame:
    def __init__(self):
        pygame.init()  # Initialisation de tous les modules Pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Création de la fenêtre de jeu avec une taille définie
        pygame.display.set_caption('Hollow')  # Définition du titre de la fenêtre
        self.clock = pygame.time.Clock()  # Création d'un objet horloge pour gérer la vitesse du jeu

        # Chargement des niveaux du jeu
        self.game_level = CreateLevel("game_level", self.screen, self)
        self.main_menu_level = CreateLevel("main_menu", self.screen, self)
        self.selected_level = "main_menu"  # Niveau actuellement sélectionné

        # Chargement de l'image de fond pour le menu principal
        self.main_menu_background = pygame.image.load("Coding/graphics/background/main_menu_background.png")

    def run(self):
        while True:  # Boucle principale du jeu
            keys = pygame.key.get_pressed()  # Récupération des touches pressées
            for event in pygame.event.get():  # Parcours des événements Pygame
                if event.type == pygame.QUIT:  # Si l'événement est de type QUIT
                    pygame.quit()  # Quitter Pygame
                    sys.exit()  # Fermer la fenêtre

            self.screen.fill((0, 0, 0))  # Remplissage de l'écran avec une couleur noire

            # Affichage du niveau sélectionné
            if self.selected_level == "main_menu":
                self.screen.blit(self.main_menu_background, (0, 0))  # Affichage de l'image de fond du menu principal
                self.main_menu_level.run()  # Exécution du niveau du menu principal
            else:
                self.game_level.run()  # Exécution du niveau de jeu

            pygame.display.update()  # Mise à jour de l'affichage
            self.clock.tick(FPS)  # Contrôle de la vitesse du jeu

    def change_level(self, level_name):
        self.selected_level = level_name  # Changement du niveau actuellement sélectionné

if __name__ == '__main__':
    game = CreateGame()  # Création d'une instance de CreateGame
    game.run()  # Lancement du jeu
