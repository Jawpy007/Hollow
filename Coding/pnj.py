import pygame
import math
from Entity import Entite
from Settings import *

class pnj(Entite):
    def __init__(self, x, y, groups,obs_groups, color=(25, 45, 2), speed=2, detection_radius=((200))):
        super().__init__(x, y, groups,obs_groups,color=color)
        self.speed = speed  # Vitesse de déplacement de l'ennemi
        self.detection_radius = detection_radius  # Rayon de détection du joueur
        self.direction = pygame.math.Vector2()
        self.name="john"
        self.dialogue_states=0
        self.generic_dialogue_index=1

    def update(self):


        self.move()
