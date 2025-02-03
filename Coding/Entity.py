import pygame
from Settings import *

"""
Une classe Entite générique pour toutes les entités du jeu.
"""

class Entite:
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)  # Rectangle représentant l'entité
        self.color = color  # Couleur de l'entité
        self.velocity_y = 0  # Vitesse verticale (utilisée pour la gravité)
        self.on_ground = False  # Savoir si l'entité touche le sol

    def apply_gravity(self, gravity, ground_height):
        """Applique la gravité à l'entité."""
        self.velocity_y += gravity  # Augmente la vitesse vers le bas
        self.rect.y += self.velocity_y  # Déplace l'entité en fonction de la gravité

        # Empêcher de tomber en dehors du sol
        if self.rect.bottom >= ground_height:
            self.rect.bottom = ground_height
            self.velocity_y = 0
            self.on_ground = True

    def draw(self, screen):
        """Dessine l'entité sur l'écran."""
        pygame.draw.rect(screen, self.color, self.rect)
