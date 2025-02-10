import pygame
from Entity import Entite
from Settings import *
import math

class Belier(Entite):
	def __init__(self, x, y, groups, obs_groups, player, detection_range=10, attack_range=20):
		super().__init__(x, y, groups, obs_groups, color=(0, 255, 0))  # Couleur verte pour le crapaud
		self.player = player
		self.detection_range = detection_range
		self.attack_range = attack_range
		self.is_attacking = False
		self.direction = pygame.math.Vector2()

	def update(self):
		distance_to_player = self.distance_player()

		if distance_to_player <= self.attack_range:
			self.attack_player()
		elif distance_to_player <= self.detection_range:
			self.rush_towards_player()
		else:
			self.is_attacking = False

		self.apply_gravity()
		self.move()

	def distance_player(self):
		"""Retourne la distance du mob au joueur."""
		dx = self.player.rect.centerx - self.rect.centerx
		dy = self.player.rect.centery - self.rect.centery
		distance = math.sqrt(dx**2 + dy**2)  # Pythagore

		if distance > 0.1:
			self.direction.x = dx / distance  # Normalisation du vecteur de direction
			self.direction.y = dy / distance  # Permet un suivi plus fluide du joueur
		return distance

	def rush_towards_player(self):
		(end_x,end_y) = (self.player.rect.centerx,self.player.rect.centery)


	def attack_player(self):
		if not self.is_attacking:
			self.is_attacking = True
			self.attack([self.player], self.rect.centerx, self.rect.centery, -5)  # -5 dégâts


