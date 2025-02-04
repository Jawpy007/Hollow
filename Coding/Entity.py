import pygame
from Settings import *

"""
Une classe Entite générique pour toutes les entités du jeu.
"""

class Entite(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, groups,obs_groups, color=(255, 255, 255),  surface=None):
		super().__init__(groups) #Initialisation de la classe parent
		self.image = pygame.Surface((width, height))
		self.image.fill(color)
		self.rect = self.image.get_rect(topleft=(x, y))  # Rectangle représentant l'entité
		self.color = color  # Couleur de l'entité
		self.velocity_y = 0  # Vitesse verticale (utilisée pour la gravité)
		self.on_ground = False  # Savoir si l'entité touche le sol
		self.obs_groups=obs_groups

	def apply_gravity(self):
		self.direction.y += GRAVITY*4  # Déplace l'entité en fonction de la gravité
	
	def move(self):
		CollisionType=[]
		self.rect.x += self.direction.x * SPEED
		CollisionType+=[self.collision("x")]
		self.rect.y += self.direction.y * SPEED
		CollisionType+=[self.collision("y")]
		return CollisionType

		# Empêcher de tomber en dehors du sol
	def collision(self,Direction):
		CollisionType=None
		if Direction == "x":
			for sprite in self.obs_groups: # on parcour tout les sprite qui ont une hitbox
				if sprite.rect.colliderect(self.rect):
					if self.direction.x > 0: 
						self.rect.right = sprite.rect.left #on va a gauche du sprite avec le quel on est entrée en collision 
						CollisionType="droite" 
					elif self.direction.x < 0: 
						self.rect.left = sprite.rect.right #on va a droite du sprite avec le quel on est entrée en collision 
						CollisionType="gauche" 
						
		elif Direction == 'y': 
			for sprite in self.obs_groups: # on parcour tout les sprite qui ont une hitbox
				if sprite.rect.colliderect(self.rect):
					if self.direction.y > 0: 
						self.rect.bottom = sprite.rect.top #on va au dessus du sprite avec le quel on est entrée en collision 
						CollisionType="bas" 
					elif self.direction.y < 0:
						self.rect.top = sprite.rect.bottom #on va en bas du sprite avec le quel on est entrée en collision 
						CollisionType="haut" 
		return CollisionType
		
 
"""    def draw(self, screen):

		pygame.draw.rect(screen, self.color, self.rect) #A remplacer plus tard avec des import de texture personnalisé
"""