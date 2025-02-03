import pygame
from Entity import Entite

class Monstre(Entite):
    def __init__(self, x, y, width=50, height=50, color=(255, 0, 0), speed=2, detection_radius=200):
        super().__init__(x, y, width, height, color)
        self.speed = speed  # Vitesse de déplacement de l'ennemi
        self.detection_radius = detection_radius  # Rayon de détection du joueur

    def follow_player(self, player):
        """Fait suivre le joueur par le monstre s'il est à portée."""
        dx = player.rect.centerx - self.rect.centerx  # Distance horizontale
        distance = abs(dx)  # Distance absolue

        if distance < self.detection_radius:  # Si le joueur est dans la zone de détection
            if dx > 0:
                self.rect.x += self.speed  # Se déplace à droite
            elif dx < 0:
                self.rect.x -= self.speed  # Se déplace à gauche

    def update(self, player, gravity, ground_height):
        """Met à jour le monstre (déplacement vers le joueur + gravité)."""
        self.follow_player(player)
        self.apply_gravity(gravity, ground_height)
