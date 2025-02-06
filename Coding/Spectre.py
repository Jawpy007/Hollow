# Spectre.py
import pygame
import math
from Entity import Entite

"""
Post-it pour ameliorer le spectre :

calcule de la position de fin en fonction d'une symetrie axiale par rapport au jour , par exemple :   pos_fin = start_pos + 2 * ('distance entre start_pos et le joueur)




"""


class Spectre(Entite):
    def __init__(self, x, y, groups, player,obs_groups, width=50, height=50, color=(128, 0, 128), speed=2, detection_radius=528):
        super().__init__(x, y, width, height, groups,obs_groups,color)
        self.speed = speed  # Vitesse de déplacement en mode idle
        self.detection_radius = detection_radius  # Rayon de détection du joueur
        self.player=player
        self.direction = pygame.math.Vector2()

        # États possibles : "idle", "attack", "return", "waiting"
        self.state = "idle"
        
        self.attack_timer = 0  # Compteur pour l'attaque
        self.attack_duration = 60  # Durée de l'attaque en frames (1 sec à 60 FPS)
        self.wait_time = 10  # Temps d'attente avant une nouvelle attaque (10 ms)
        self.wait_timer = 0  # Timer pour le mode "waiting"

        self.start_pos = (x, y)  # Position de départ
        self.target_pos = None  # Position du joueur au début de l'attaque
        self.attack_amplitude = 100  # Amplitude du mouvement en courbe
        self.end_pos = (800,500) #Position de base

    def distance_player(self,player):
        """Retourne la distance du mob au joueur."""
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2) #Potit pythagore 
        return distance

    def detect_player(self, player):
        """Retourne True si le joueur est dans le rayon de détection."""
        distance = self.distance_player(player)
        return distance < self.detection_radius

    def start_attack(self, player):
        """Initialise l'attaque sur le joueur."""
        self.state = "attack"
        self.attack_timer = 0
        self.start_pos = (self.rect.x, self.    rect.y)
        self.target_pos = (player.rect.x, player.rect.y)

        if self.start_pos[0] < player.rect.centerx:
            self.end_pos = (self.start_pos[0] + self.distance_player(player) , self.start_pos[1])
            self.speed = -self.speed
        else:
            self.end_pos = (self.start_pos[0] - self.distance_player(player) , self.start_pos[1])
            

    def update_attack(self):
        """Met à jour la position du spectre selon une trajectoire courbée."""
        t = self.attack_timer / self.attack_duration  # t varie de 0 à 1
        if t > 1:
            # Fin de l'attaque, passage au retour
            self.state = "return"
            self.attack_timer = 0
            return

        x0, y0 = self.start_pos
        target_x, target_y = self.target_pos
        new_x = x0 + (target_x - x0) * t
        new_y = y0 + (target_y - y0) * t

        # Ajout d'une courbe avec un sinus
        curve_offset = self.attack_amplitude * math.sin(math.pi * t)
        new_y += curve_offset

        self.rect.x = new_x
        self.rect.y = new_y

        self.attack_timer += 1

    def update_return(self):
        """Fait revenir le spectre à sa position initiale."""
        t = self.attack_timer / self.attack_duration  # t varie de 0 à 1
        if t > 1:
            # Retour terminé, passage en attente
            self.state = "waiting"
            self.wait_timer = 0
            return

        target_x, target_y = self.end_pos
        start_x, start_y = self.rect.x, self.rect.y
        new_x = start_x + (target_x - start_x) * t
        new_y = start_y + (target_y - start_y) * t

        self.rect.x = new_x
        self.rect.y = new_y

        self.attack_timer += 1

    def idle_behavior(self):
        """Déplacement horizontal en mode idle."""
        self.rect.x += self.speed        
        if self.rect.right > 1920 or self.rect.left < 0: # A changer car si il depasse cette zone il bug un po
            self.speed = -self.speed

    def update(self):
        """Gère les mises à jour en fonction de l'état."""
        if self.state == "idle":
            if self.detect_player(self.player):
                self.start_attack(self.player)
            else:
                self.idle_behavior()

        elif self.state == "attack":
            self.update_attack()

        elif self.state == "return":
            self.update_return()

        elif self.state == "waiting":
            self.wait_timer += 1
            if self.wait_timer > self.wait_time:
                self.state = "idle"