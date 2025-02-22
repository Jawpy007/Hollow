import pygame, sys  # Bibliothèque pygame pour gérer le jeu, et sys pour gérer la fermeture de la fenêtre
from Settings import *  # Importation des paramètres prédéfinis
from Level import *  # Importation du module Level, qui gère la carte et les entités
from Player import *
from Enemy import Monstre  # Importation de la classe Monstre
from Spectre import Spectre  # Import de classe Spectre


"""
CreateGame permet de lancer le jeu , il est la base centrale

"""


class CreateGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Hollow')
        self.clock = pygame.time.Clock()
        self.game_level= CreateLevel("game_level", self.screen, self)
        self.main_menu_level=CreateLevel("main_menu", self.screen, self)
        self.selected_level="main_menu"
        # Charger l'image
        self.main_menu_background = pygame.image.load("Coding/graphics/background/main_menu_background.png")
    def run(self):
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((0, 0, 0))  # Fond noir
            if self.selected_level=="main_menu":
                self.screen.blit(self.main_menu_background, (0, 0))
                self.main_menu_level.run()
            else:
                self.game_level.run()
            pygame.display.update()
            self.clock.tick(FPS)
    def change_level(self,level_name):
        self.selected_level=level_name
if __name__ == '__main__':
    game = CreateGame()
    game.run()