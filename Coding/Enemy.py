import pygame
import math
from Entity import Entite
from Settings import *

class Monstre(Entite):
    def __init__(self, x, y, groups, player,obs_groups, color=(255, 0, 0), speed=2, detection_radius=((200))):
        super().__init__(x, y, groups,obs_groups,color=color)
        self.speed = speed  # Vitesse de déplacement de l'ennemi
        self.detection_radius = detection_radius  # Rayon de détection du joueur
        self.player=player
        self.direction = pygame.math.Vector2()


    def follow_player(self):
        """Fait suivre le joueur par le monstre s'il est à portée."""
        dx = self.player.rect.centerx - self.rect.centerx  # Distance horizontale
        dy = self.player.rect.centery - self.rect.centery  # Distance verticale
        distance = math.sqrt(dx**2 + dy**2)  # Calculer la distance

        if distance < self.detection_radius:  # Si le joueur est dans la zone de détection
            if distance > TILE_SIZE or distance <-TILE_SIZE:
                self.direction.x = dx / distance  # Normalisation du vecteur de direction
                self.direction.y = dy / distance  # Permet un suivi plus fluide du joueur
        else:
            self.direction = pygame.math.Vector2()  # Stopper le mouvement

        if TILE_SIZE>=dx>0:
            self.attack([self.player], self.rect.x+TILE_SIZE, self.rect.y, -5, (TILE_SIZE,TILE_SIZE))
        elif -TILE_SIZE<=dx<=0:
            self.attack([self.player], self.rect.x-TILE_SIZE, self.rect.y, -5, (TILE_SIZE,TILE_SIZE))




    def distance_player(self):
        """Retourne la distance du mob au joueur."""
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2) #Potit pythagore 
        return distance

    def update(self):
        """Met à jour le monstre (déplacement vers le joueur + gravité)."""
        self.direction=pygame.math.Vector2()
        self.follow_player()
        self.apply_gravity()
        self.move()