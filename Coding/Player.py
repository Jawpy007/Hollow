import pygame
from Settings import *
from Entity import *

"""
Une classe Player qui hérite de Entite, avec ses propres mouvements et sauts.
"""

class Player(Entite):
	def __init__(self, x, y,groups, eni_groups,obs_groups, width=50, height=50, color=(255, 255, 255)):
		super().__init__(x, y, width, height, groups, obs_groups,color)  # Appelle le constructeur de Entite
		self.speed = 5  # Vitesse de déplacement
		self.direction = pygame.math.Vector2()

		self.jump_count=MAXJUMP

		self.walljump=None
		self.walljump_time=pygame.time.get_ticks()

		self.lastwalljump=None

		self.in_jump=False
		self.in_jump_time =pygame.time.get_ticks()
		self.spacebar_block=False
		self.stats={"hp":{"value":10,"max_value":100}}

	def input(self):
		self.direction=pygame.math.Vector2()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_q] and not self.walljump:
			self.direction.x+=-1
		if keys[pygame.K_d] and not self.walljump:
			self.direction.x+=1
		if keys[pygame.K_SPACE] and self.jump_count>0 and not self.spacebar_block:  # Saut seulement si au sol
			self.walljump=None
			self.in_jump=True
			self.jump_count-=1
			self.in_jump_time =pygame.time.get_ticks()
			self.spacebar_block=True
		if not keys[pygame.K_SPACE]:
			self.spacebar_block=False
			


			
	
	def collision_event(self, CollisionType):
		if "gauche" in CollisionType and "bas" not in CollisionType and not self.walljump:
			self.walljump="gauche"
			self.walljump_time=pygame.time.get_ticks()
			self.jump_count=1

		if self.walljump and "gauche" not in CollisionType:
			self.walljump=None

		if  "bas" in CollisionType:
			self.jump_count=MAXJUMP


	def move(self):
		CollisionType=[]
		if not self.walljump and not self.in_jump:
			self.rect.x += self.direction.x * SPEED
			CollisionType+=[self.collision("x")]
			self.rect.y += self.direction.y * SPEED
			CollisionType+=[self.collision("y")]

		elif self.in_jump:

			self.rect.x += self.direction.x * SPEED
			CollisionType+=[self.collision("x")]
			for i in range(2):
				self.direction.y=-1
				self.rect.y += self.direction.y * SPEED
				CollisionType+=[self.collision("y")]
				
		if self.walljump:
			#declenchement intentionnel d'une colision pour verifier que le joueur est toujours accrocher a un mur
			if self.walljump=="gauche":
				self.direction.x=-1
			else:
				self.direction.x=1
			self.rect.x += self.direction.x
			CollisionType+=[self.collision("x")]

			self.direction.y=1
			self.rect.y += self.direction.y
			CollisionType+=[self.collision("y")]
		return CollisionType

	def apply_gravity(self):
		if not self.walljump and not self.walljump:
			self.direction.y += GRAVITY # Déplace l'entité en fonction de la gravité
		if self.walljump:
			pass


	def all_cooldown(self):
		self.current_time=pygame.time.get_ticks()
		if self.walljump and self.current_time -self.walljump_time > WALL_JUMP_COOLDOWN*10:
			self.walljump=None
		if self.in_jump and self.current_time - self.in_jump_time > JUMP_COOLDOWN:
			self.in_jump=False
				
	def stats_update(nom_stats,value_update,max_update=None):
		if max_update:
			self.stats[nom_stats]["max"]+=max_update
		if value_update:
			self.stats[nom_stats]["value"]+=max_update
		pass

	def update(self):
		"""Met à jour le joueur (mouvement + gravité)."""
		print(self.caca)
		self.input()
		self.apply_gravity()
		CollisionType=self.move()
		self.collision_event(CollisionType)
		self.all_cooldown()


		
