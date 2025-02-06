import pygame
from Settings import *

"""
Une classe Entite générique pour toutes les entités du jeu.
"""

class Entite(pygame.sprite.Sprite):
	def __init__(self, x, y, groups,obs_groups, surface=None, width=TILE_SIZE, height=TILE_SIZE, color=(255, 255, 255)):
		print(groups)
		super().__init__(groups) #Initialisation de la classe parent
		self.image = pygame.Surface((width, height))
		self.image.fill(color)
		self.rect = self.image.get_rect(topleft=(x, y))  # Rectangle représentant l'entité
		self.color = color  # Couleur de l'entité
		self.velocity_y = 0  # Vitesse verticale (utilisée pour la gravité)
		self.on_ground = False  # Savoir si l'entité touche le sol
		self.obs_groups=obs_groups

		self.stats={"hp":{"value":10,"max_value":100}}

	def apply_gravity(self):
		self.direction.y += GRAVITY*4  # Déplace l'entité en fonction de la gravité
	
	def move(self):
		CollisionType=[]
		self.rect.x += self.direction.x * ENTITE_SPEED_MULTIPLICATOR
		CollisionType+=[self.collision("x")]
		self.rect.y += self.direction.y * ENTITE_SPEED_MULTIPLICATOR
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
	
	def stats_update(self,nom_stats,value_update,max_update=None):
		if max_update:
			self.stats[nom_stats]["max"]+=max_update
		if value_update:
			self.stats[nom_stats]["value"]+=value_update
			print(self,self.stats[nom_stats]["value"])

	def stats_set(self,nom_stats,value_update,max_update=None):
		if max_update:
			self.stats[nom_stats]["max"]=max_update
		if value_update:
			self.stats[nom_stats]["value"]=value_update
			print(self,self.stats[nom_stats]["value"])

	def attack(self, eni_groups,x,y,value,size=(TILE_SIZE,TILE_SIZE)):
		hitbox=CreateHitbox(x,y,size)
		for sprite in eni_groups:
			if hitbox.rect.colliderect(sprite):
				sprite.stats_update("hp", value)
	
class CreateHitbox(pygame.sprite.Sprite):
	def __init__(self,x, y, size=(TILE_SIZE,TILE_SIZE)):

		self.image=pygame.Surface(size)
		#self.image.set_alpha(0)
		self.image.fill("blue")
		self.rect = self.image.get_rect(topleft = (x,y))
	

"""    def draw(self, screen):

		pygame.draw.rect(screen, self.color, self.rect) #A remplacer plus tard avec des import de texture personnalisé
"""