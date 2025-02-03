import pygame, sys  # Bibliothèque pygame pour gérer le jeu, et sys pour gérer la fermeture de la fenêtre
from Settings import *  # Importation des paramètres prédéfinis
from Level import *  # Importation du module Level, qui gère la carte et les entités
from Player import *

class CreateGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Simple Platformer')
        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 100)  # Instance du joueur

    def run(self):
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))  # Fond noir
            self.player.update(keys, GRAVITY, HEIGHT)  # Mise à jour du joueur
            self.player.draw(self.screen)  # Dessine le joueur
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = CreateGame()
    game.run()
