import pygame
from Settings import *
from Entity import *

"""
Une classe Player qui hérite de Entite, avec ses propres mouvements et sauts.
"""

class Player(Entite):
    def __init__(self, x, y, width=50, height=50, color=(255, 255, 255)):
        super().__init__(x, y, width, height, color)  # Appelle le constructeur de Entite
        self.speed = 5  # Vitesse de déplacement
        self.jump_strength = -10  # Force du saut

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += SPEED
        if keys[pygame.K_SPACE] and self.on_ground:  # Saut seulement si au sol
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

    def update(self, keys, gravity, ground_height):
        """Met à jour le joueur (mouvement + gravité)."""
        self.move(keys)
        self.apply_gravity(gravity, ground_height)
