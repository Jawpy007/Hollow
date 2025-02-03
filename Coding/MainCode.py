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
        pygame.display.set_caption('Simple Platformer')
        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 100)  # Instance du joueur
        self.monstre = Monstre(500, HEIGHT - 100)  # Instance d'un monstre
        self.spectre = Spectre(400,500) #Instance d'un spectre
        

    def run(self):
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))  # Fond noir
            self.player.update(keys, GRAVITY, HEIGHT)  # Mise à jour du joueur
            self.monstre.update(self.player, GRAVITY, HEIGHT)  # Mise à jour du monstre
            self.spectre.update(self.player, GRAVITY, HEIGHT) #Mise a jour du spectre
            
            self.player.draw(self.screen)  # Dessine le joueur
            self.monstre.draw(self.screen)  # Dessine le monstre
            self.spectre.draw(self.screen) # Dessine le spectre

            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = CreateGame()
    game.run()
