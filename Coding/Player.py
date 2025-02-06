import pygame
from Settings import *
from Entity import *

"""
Une classe Player qui hérite de Entite, avec ses propres mouvements et sauts.
"""

class Player(Entite):
	def __init__(self, x, y,groups, eni_groups,obs_groups, climp_zone, width=50, height=50, color=(255, 255, 255)):
		super().__init__(x, y, width, height, groups, obs_groups,color)  # Appelle le constructeur de Entite
		self.speed = 5  # Vitesse de déplacement
		self.direction = pygame.math.Vector2()
		self.climp_zone=climp_zone
		self.jump_count=MAXJUMP

		self.walljump=None
		self.walljump_time=pygame.time.get_ticks()
		self.walljump_side_cooldown=pygame.time.get_ticks()
		self.lastwalljump=None

		self.wall_jump_jump_left=False
		self.wall_jump_jump_left_cooldown=pygame.time.get_ticks()
		self.wall_jump_jump_right=False
		self.wall_jump_jump_right_cooldown=pygame.time.get_ticks()
		
		self.in_jump=False
		self.in_jump_time =pygame.time.get_ticks()
		self.spacebar_block=False
		self.stats={"hp":{"value":10,"max_value":100}}
		self.i=0


	def input(self):
		self.direction=pygame.math.Vector2()
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_q] and not self.walljump) or self.wall_jump_jump_left:
			self.direction.x+=-1
		if (keys[pygame.K_d] and not self.walljump) or self.wall_jump_jump_right:
			self.direction.x+=1
		if keys[pygame.K_SPACE] and self.jump_count>0 and not self.spacebar_block:  # Saut seulement si au sol
			if self.walljump=="droite":
				self.wall_jump_jump_left=True
				self.wall_jump_jump_left_cooldown=pygame.time.get_ticks()
			elif self.walljump=="gauche":
				self.wall_jump_jump_right=True
				self.wall_jump_jump_right_cooldown=pygame.time.get_ticks()
			self.in_jump=True
			self.jump_count-=1
			self.in_jump_time =pygame.time.get_ticks()
			self.spacebar_block=True
			self.walljump=None

		if not keys[pygame.K_SPACE]:
			self.spacebar_block=False
	
	def collision_event(self):
		keys = pygame.key.get_pressed() 
		if "climp_gauche" in self.CollisionType and not self.walljump and (keys[pygame.K_q] or self.wall_jump_jump_left) and self.lastwalljump!="gauche":
			self.walljump="gauche"
			self.walljump_time=pygame.time.get_ticks()
			self.walljump_side_cooldown=pygame.time.get_ticks()
			self.jump_count=1
			self.lastwalljump="gauche"
			self.wall_jump_jump_right=False
			self.wall_jump_jump_left=False

		
		elif "climp_droite" in self.CollisionType and not self.walljump and (keys[pygame.K_d] or self.wall_jump_jump_right) and self.lastwalljump!="droite":
			self.walljump="droite"
			self.walljump_time=pygame.time.get_ticks()
			self.walljump_side_cooldown=pygame.time.get_ticks()
			self.jump_count=1
			self.lastwalljump="droite"
			self.wall_jump_jump_right=False
			self.wall_jump_jump_left=False

		elif (self.walljump=="gauche" and "climp_gauche" not in self.CollisionType  )or (self.walljump=="droite"  and "climp_droite" not in self.CollisionType):
			self.walljump=None

		elif  "bas" in self.CollisionType:
			self.jump_count=MAXJUMP



	def move(self):
		self.CollisionType=[]
		self.collision("climp_zone")
		if self.walljump==None and not self.in_jump:
			self.rect.x += self.direction.x * SPEED
			self.collision("x")
			self.rect.y += self.direction.y * SPEED
			self.collision("y")

		elif self.in_jump and self.walljump==None:
			if self.wall_jump_jump_right or self.wall_jump_jump_left:
				self.direction.x =self.direction.x *2
			self.rect.x += self.direction.x * SPEED
			self.collision("x")
			for i in range(2):
				self.direction.y=-1
				self.rect.y += self.direction.y * SPEED
				self.collision("y")
				
		elif self.walljump!=None:
			#declenchement intentionnel d'une colision pour verifier que le joueur est toujours accrocher a un mur
			if self.walljump=="gauche":
				self.direction.x = -1
			else:
				self.direction.x = 1
			self.rect.x += self.direction.x
			self.collision("x")
			self.direction.y=1
			self.rect.y += self.direction.y
			self.collision("y")


	def apply_gravity(self):
		if self.walljump==None:
			self.direction.y += GRAVITY
 # Déplace l'entité en fonction de la gravité
		if self.walljump:
			pass


	def all_cooldown(self):
		self.current_time=pygame.time.get_ticks()
		if self.walljump and self.current_time -self.walljump_time > WALL_JUMP_COOLDOWN*10:
			self.walljump=None
		if self.in_jump and self.current_time - self.in_jump_time > JUMP_COOLDOWN:
			self.in_jump=False
		if self.lastwalljump and self.current_time-self.walljump_side_cooldown> JUMP_COOLDOWN*10:
			self.lastwalljump=None
		if self.wall_jump_jump_left and self.current_time-self.wall_jump_jump_left_cooldown> JUMP_COOLDOWN*2:
			self.wall_jump_jump_left=False
		if self.wall_jump_jump_right and self.current_time-self.wall_jump_jump_right_cooldown> JUMP_COOLDOWN*2:
			self.wall_jump_jump_right=False
						
	def stats_update(self,nom_stats,value_update,max_update=None):
		if max_update:
			self.stats[nom_stats]["max"]+=max_update
		if value_update:
			self.stats[nom_stats]["value"]+=value_update
		pass

	def collision(self,Direction):

		if Direction == "x":
			for sprite in self.obs_groups: # on parcour tout les sprite qui ont une hitbox
				if sprite.rect.colliderect(self.rect):
					if sprite.name=="climp_wall_g":
						if sprite.rect.centerx<self.rect.centerx:
							self.rect.left = sprite.rect.right
							self.CollisionType+= ["climp_gauche", "gauche"]
						else:
							self.rect.right = sprite.rect.left #on va a gauche du sprite avec le quel on est entrée en collision 
							self.CollisionType+=["droite"]

					elif sprite.name=="climp_wall_r":
						if sprite.rect.centerx>self.rect.centerx:
							self.rect.right = sprite.rect.left
							self.CollisionType+= ["climp_droite", "droite"]
						else:
							self.rect.left = sprite.rect.right #on va a droite du sprite avec le quel on est entrée en collision 
							self.CollisionType+=["gauche"]

					elif self.direction.x > 0: 
						self.rect.right = sprite.rect.left #on va a gauche du sprite avec le quel on est entrée en collision 
						self.CollisionType+=["droite"]
					elif self.direction.x < 0: 
						self.rect.left = sprite.rect.right #on va a droite du sprite avec le quel on est entrée en collision 
						self.CollisionType+=["gauche"]
		elif Direction == 'y': 
			for sprite in self.obs_groups: # on parcour tout les sprite qui ont une hitbox
				if sprite.rect.colliderect(self.rect):
					if self.direction.y > 0: 
						self.rect.bottom = sprite.rect.top #on va au dessus du sprite avec le quel on est entrée en collision 
						self.CollisionType+=["bas"]
					elif self.direction.y < 0:
						self.rect.top = sprite.rect.bottom #on va en bas du sprite avec le quel on est entrée en collision 
						self.CollisionType+=["haut]"]



	def update(self):
		"""Met à jour le joueur (mouvement + gravité)."""
		self.input()
		self.apply_gravity()
		self.move()
		self.collision_event()
		self.all_cooldown()


		
