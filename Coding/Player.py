import pygame
from Settings import *
from Entity import *

"""
Une classe Player qui hérite de Entite, avec ses propres mouvements et sauts.
"""

class Player(Entite):
	def __init__(self, x, y,groups, eni_groups,obs_groups, climp_zone, color=(255, 255, 255)):
		super().__init__(x, y, groups, obs_groups,color)  # Appelle le constructeur de Entite
		self.eni_groups=eni_groups

		self.direction = pygame.math.Vector2()

		self.jump_count=MAXJUMP

		self.climp_zone=climp_zone
		self.walljump=None
		self.walljump_time=pygame.time.get_ticks()

		self.lastwalljump=None
		self.lastwalljump_cooldown=pygame.time.get_ticks()

		self.wall_jump_jump_left=False
		self.wall_jump_jump_left_cooldown=pygame.time.get_ticks()

		self.wall_jump_jump_right=False
		self.wall_jump_jump_right_cooldown=pygame.time.get_ticks()
		
		self.in_jump=False
		self.in_jump_time =pygame.time.get_ticks()

		self.spacebar_block=False

		self.player_level=1
		self.d_block=False
		self.q_block=False

		self.stats["mana"]={"value":10,"max_value":100}
		self.stats["xp"]={"value":0,"max_value":100}

		self.dashing=False

		self.running=False

		self.player_xp_level=1

		self.dashing_last=[False, pygame.time.get_ticks()]

		self.K_d_doubletap=[pygame.time.get_ticks() ,pygame.time.get_ticks()]
		self.K_q_doubletap=[pygame.time.get_ticks() ,pygame.time.get_ticks()] #time de la derniere press et time du dernier lacher

		self.player_image_dash = pygame.image.load("Coding/graphics/player/dash.png")  
		self.player_image = pygame.Surface((TILE_SIZE,TILE_SIZE))

	def import_player_assets(self):
		pass

	def input(self):
		self.direction=pygame.math.Vector2()
		keys = pygame.key.get_pressed()

		if (keys[pygame.K_q] and not self.walljump) or self.wall_jump_jump_left:
			if 	self.current_time -self.K_q_doubletap[0]<200 and self.current_time -self.K_q_doubletap[1]<200 and not self.q_key_block and self.current_time -self.lastwalljump_cooldown>700 and not self.wall_jump_jump_left:
				self.dashing=True
			self.direction.x+=-1
			self.K_q_doubletap[0]=pygame.time.get_ticks() if not self.wall_jump_jump_left else self.K_q_doubletap[0]
			self.q_key_block=True if not self.wall_jump_jump_left else False

		if (keys[pygame.K_d] and not self.walljump) or self.wall_jump_jump_right:
			if 	self.current_time -self.K_d_doubletap[0]<200 and self.current_time -self.K_d_doubletap[1]<200 and not self.d_key_block and self.current_time -self.lastwalljump_cooldown>200 and not self.wall_jump_jump_right:
				self.dashing=True
			self.direction.x+=1
			self.K_d_doubletap[0]=pygame.time.get_ticks()  if not self.wall_jump_jump_right else self.K_d_doubletap[0]
			self.d_key_block=True if not self.wall_jump_jump_right else False

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

		if keys[pygame.K_LSHIFT]:
			self.K_d_doubletap=True

		if keys[pygame.K_e]:
			self.attack(self.eni_groups, self.rect.x+TILE_SIZE, self.rect.y, -10, (TILE_SIZE,TILE_SIZE))



		if not keys[pygame.K_d]:
			if self.current_time-self.K_d_doubletap[0]<200:
				self.K_d_doubletap[1]=pygame.time.get_ticks()
			self.d_key_block=False

		if not keys[pygame.K_q]:
			if self.current_time-self.K_q_doubletap[0]<200:
				self.K_q_doubletap[1]=pygame.time.get_ticks()
			self.q_key_block=False

		if not keys[pygame.K_LSHIFT]:
			self.running=False

		if not keys[pygame.K_SPACE]:
			self.spacebar_block=False

	def collision_event(self):
		keys = pygame.key.get_pressed() 
		if "climp_gauche" in self.CollisionType and not self.walljump and (keys[pygame.K_q] or self.wall_jump_jump_left) and self.lastwalljump!="gauche":
			self.walljump="gauche"
			self.walljump_time=pygame.time.get_ticks()
			self.lastwalljump_cooldown=pygame.time.get_ticks()
			self.jump_count=1
			self.lastwalljump="gauche"
			self.wall_jump_jump_right=False
			self.wall_jump_jump_left=False

			self.q_block=True

		
		elif "climp_droite" in self.CollisionType and not self.walljump and (keys[pygame.K_d] or self.wall_jump_jump_right) and self.lastwalljump!="droite":
			self.walljump="droite"
			self.walljump_time=pygame.time.get_ticks()
			self.lastwalljump_cooldown=pygame.time.get_ticks()
			self.jump_count=1
			self.lastwalljump="droite"
			self.wall_jump_jump_right=False
			self.wall_jump_jump_left=False

			self.d_block=True

		elif (self.walljump=="gauche" and "climp_gauche" not in self.CollisionType  )or (self.walljump=="droite"  and "climp_droite" not in self.CollisionType):
			self.walljump=None

		elif  "bas" in self.CollisionType:
			self.jump_count=MAXJUMP

	def move(self):
		self.CollisionType=[]
		self.collision("climp_zone")

		if self.dashing_last[0] and self.current_time-self.dashing_last[1]>100:
			x, y=self.rect.x, self.rect.y
			self.image = self.player_image  # Affectation de l'image au sprite
			self.rect = self.image.get_rect()  # Récupère le rectangle de l'image
			self.rect.topleft = (x, y)  # Position initiale du sprite
			self.image.fill("white")
			self.dashing_last[0]=False

		if self.walljump==None and not self.in_jump:
			if self.running:
				self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR/2
				self.collision("x")
				
			if self.dashing:
				self.dashing=False
				x, y=self.rect.x, self.rect.y
				self.image = self.player_image_dash  # Affectation de l'image au sprite
				self.rect = self.image.get_rect()  # Récupère le rectangle de l'image
				self.rect.topleft = (x, y)  # Position initiale du sprite
				for i in range(20):
					self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR
					self.collision("x")
				self.dashing_last[0]=True
				self.dashing_last[1]=pygame.time.get_ticks()


			self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR
			self.collision("x")
			self.rect.y += self.direction.y * PLAYER_SPEED_MULTIPLICATOR
			self.collision("y")

		elif self.in_jump and self.walljump==None:
			if self.wall_jump_jump_right or self.wall_jump_jump_left:
				self.direction.x =self.direction.x * WALL_JUMP_X_SPEED_MULTIPLICATOR
			else:
				if self.dashing:
					self.dashing=False
					x, y=self.rect.x, self.rect.y
					self.image = self.player_image_dash  # Affectation de l'image au sprite
					self.rect = self.image.get_rect()  # Récupère le rectangle de l'image
					self.rect.topleft = (x, y)  # Position initiale du sprite
					for i in range(20):
						self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR
						self.collision("x")
					self.dashing_last[0]=True
					self.dashing_last[1]=pygame.time.get_ticks()
			self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR
			self.collision("x")
			for i in range(2):
				self.direction.y=-1
				self.rect.y += self.direction.y * PLAYER_JUMP_MULTIPLICATOR
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
		if self.walljump and self.current_time -self.walljump_time > WALL_JUMP_COOLDOWN*10:
			self.walljump=None
		if self.in_jump and self.current_time - self.in_jump_time > JUMP_COOLDOWN:
			self.in_jump=False
		if self.lastwalljump and self.current_time-self.lastwalljump_cooldown> JUMP_COOLDOWN*10:
			self.lastwalljump=None
		if self.wall_jump_jump_left and self.current_time-self.wall_jump_jump_left_cooldown> JUMP_COOLDOWN*2:
			self.wall_jump_jump_left=False
		if self.wall_jump_jump_right and self.current_time-self.wall_jump_jump_right_cooldown> JUMP_COOLDOWN*2:
			self.wall_jump_jump_right=False


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

	def death(self):
		print("mort")

	def player_level_up(self, value=1):
		self.player_xp_level+=value

	def stats_update(self, nom_stats, value_update, max_value=None):
		if max_value is not None:
			self.stats[nom_stats]["max_value"] = max_value

		current_value = self.stats[nom_stats]["value"]
		max_value = self.stats[nom_stats]["max_value"]
	
		if value_update + current_value > max_value:
			if nom_stats == "hp":
				self.stats[nom_stats]["value"] = max_value
			elif nom_stats == "mana":
				self.stats[nom_stats]["value"] = max_value
			elif nom_stats == "xp":
				self.stats[nom_stats]["value"] = 0
				self.player_level_up()

		elif value_update + current_value <= 0:
			if nom_stats == "hp":
				self.stats[nom_stats]["value"] = 0
				self.death()
			elif nom_stats == "mana":
				return False
			elif nom_stats == "xp":
				reste = value_update + current_value
				self.stats[nom_stats]["value"] = max_value
				self.player_level_up(-1)
				self.stats_update("xp", reste)
		else:
			self.stats[nom_stats]["value"]+=value_update
		return True

	def update(self):
		"""Met à jour le joueur (mouvement + gravité)."""
		self.current_time=pygame.time.get_ticks()
		self.input()
		self.apply_gravity()
		self.move()
		self.collision_event()
		self.all_cooldown()


		
