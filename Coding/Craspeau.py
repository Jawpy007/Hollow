# Spectre.py
import pygame
import math
from Entity import Entite

class Crapau(Entite):
	def __init__(self, x, y, groups, player,obs_groups, width=50, height=50, color=(128, 128, 128), speed=2, detection_radius=100):
		super().__init__(x, y, width, height, groups,obs_groups,color)
		self.speed = speed  # Vitesse de déplacement en mode idle
		self.detection_radius = detection_radius  # Rayon de détection du joueur
		self.player=player
		self.direction = pygame.math.Vector2()
		self.attack_range = 50
		# États possibles : "idle", "attack", "return", "waiting"
		self.state = "idle"
		
		self.attack_duration = 60  # Durée de l'attaque en frames (1 sec à 60 FPS)
		self.wait_time = 10  # Temps d'attente avant une nouvelle attaque (10 ms)
		self.wait_timer = 0  # Timer pour le mode "waiting"

		self.start_pos = (x, y)  # Position de départ
		self.end_pos = (x,y) #Position auquelle revenir a la fin du combat
		self.target_pos = None  # Position du joueur au début de l'attaque
		self.attack_amplitude = 100  # Amplitude du mouvement en courbe



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
		self.start_pos = (self.rect.x, self.rect.y)
		self.target_pos = (player.rect.x, player.rect.y)
			

	def update_attack(self):
		"""Met à jour la position du spectre selon une trajectoire courbée."""
		if self.attack_range < self.distance_player(self.player):
			# Fin de l'attaque, passage au retour
			self.state = "return"
			self.attack_timer = 0
			return

		x0, y0 = self.start_pos
		target_x, target_y = x0 , y0
	

	def update_return(self):
		"""Fait revenir le crapau à sa position initiale."""
		if  self.end_pos ==  (self.rect.centerx , self.rect.centery):
			# Retour terminé, passage en attente
			self.state = "waiting"
			self.wait_timer = 0
			return

		dx = self.rect.centerx - self.end_pos[0]  # Distance horizontale
		distance = abs(dx)  # Distance absolue
		if dx > 0:
			self.direction.x += 0.9  # Se déplace à droite
		elif dx < 0:
			self.direction.x -= 0.9  # Se déplace à gauche
		


	def idle_behavior(self):
		"""Déplacement horizontal en mode idle."""
		self.rect.x += self.speed     
		if self.rect.right > 1920 or self.rect.left < 0: # A changer car si il depasse cette zone il bug un po
			self.speed = -self.speed

	def update(self):
		"""Gère les mises à jour en fonction de l'état."""
		self.apply_gravity()
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