import pygame
from Settings import *
from Entity import CreateHitbox
class weapons:
	def __init__(self, name, damage, cooldwon):

		#caractéristique de l'arme
		self.name=name
		self.damage=damage

		#gestion du temps
		self.cooldwon=cooldwon*3
	
		self.attack_time=pygame.time.get_ticks()
		self.current_time=pygame.time.get_ticks()


class ranged_weapons(weapons):
	def __init__(self, name, damage, cooldwon, range, fire_ready_cooldown, reload_time, visible_groups, magazine_size, player):
		super().__init__(name, damage, cooldwon)
		
		self.fire_ready_cooldown=fire_ready_cooldown
		self.last_shot_time=pygame.time.get_ticks()

		self.range=range
		self.reload_time=reload_time
		self.attacking=False
		self.current_projectille=[] # tout les projectille en cours d'utilisation
		self.projectille_cooldwon=[]
		self.visible_groups=visible_groups
		self.ammo=magazine_size
		self.player=player
		self.magazine_size=magazine_size
		self.starting_reloading_time=pygame.time.get_ticks()
		self.reloading=False
 

	def use_weapons(self, user):
		self.current_time = pygame.time.get_ticks()
		if self.current_time - self.last_shot_time > self.fire_ready_cooldown:
			if self.ammo > 0:
				mouse_cord = pygame.mouse.get_pos()

				print(((1+mouse_cord[1] / HEIGHT)) * 10)
				y_force = ((HEIGHT - mouse_cord[1]) / HEIGHT) * 10
				x_force = ((mouse_cord[0] / WIDTH) - 0.5) * 50

				# Détection du côté du tir grace a la position de la souris par rapport a celle du joueur
				mouse_cord = self.visible_groups.get_world_mouse_pos()
				if mouse_cord[0] < self.player.rect.x:
					x_force = -abs(x_force)  # Si à gauche du joueur, force négative (-valeur absolue)
				else:
					x_force = abs(x_force)   # Si à droite du joueur, force positive (valeur absolue)




				attack_time = self.current_time
				self.ammo -= 1
				self.attacking = True
				self.projectille_cooldwon.append(attack_time)
				self.current_projectille.append(
					projectille(-y_force, x_force, user.rect.x + TILE_SIZE / 2, user.rect.y - TILE_SIZE / 2, user, self.visible_groups, self.player, self.cooldwon)
				)
				self.last_shot_time = pygame.time.get_ticks()



	def reload (self):
		if not self.reloading:
			self.reloading=True
			self.starting_reloading_time=pygame.time.get_ticks()
			

	def projectile_pos_update(self):
		if len(self.current_projectille)<=0:
			self.attacking=False
		else:

			if self.current_time-self.projectille_cooldwon[-1]>self.cooldwon:
				self.current_projectille[-1].sprite.kill() #remove le projectile 
				self.current_projectille.pop(-1)
				self.projectille_cooldwon.pop(-1)

			for projectille in self.current_projectille:
				projectille.update()

	def update(self):
		self.current_time=pygame.time.get_ticks()
		if self.reloading:
			if self.current_time - self.starting_reloading_time>self.reload_time:
				self.ammo=self.magazine_size
				self.reloading=False
		if self.attacking:
			self.projectile_pos_update()


class projectille(pygame.sprite.Sprite):
	def __init__(self, y_velocity, x_velocity, start_pos_x, start_pos_y, user, visible_groups, player, cooldwon):
		self.cooldwon = cooldwon
		self.player = player
		self.x_velocity = x_velocity
		self.y_velocity = y_velocity  
		self.gravity = 0.2  # Ajout de gravité pour courber la trajectoire
		self.x = start_pos_x
		self.y = start_pos_y
		self.user = user
		self.visible_groups = visible_groups
		self.sprite = CreateHitbox(self.x, self.y, groups_hit=self.visible_groups)
		self.stop = False


	def projectille_collision(self, direction):

		if direction == "x":
			for sprite in self.player.obs_groups:
				if sprite.rect.colliderect(self.sprite.rect):
					if self.x_velocity > 0:
						self.sprite.rect.right = sprite.rect.left
					elif self.x_velocity < 0:
						self.sprite.rect.left = sprite.rect.right
					self.x_velocity = 0
					self.y_velocity = 0
					self.stop = True

		elif direction == 'y':
			for sprite in self.player.obs_groups:
				if sprite.rect.colliderect(self.sprite.rect):
					if self.y_velocity > 0:
						self.sprite.rect.bottom = sprite.rect.top
					elif self.y_velocity < 0:
						self.sprite.rect.top = sprite.rect.bottom
					self.x_velocity = 0
					self.y_velocity = 0
					self.stop = True

	def projectille_moving(self):
		if not self.stop:
			self.y_velocity += self.gravity  # Accélération progressive vers le bas
			self.sprite.rect.x += self.x_velocity
			self.projectille_collision("x")

			self.sprite.rect.y += self.y_velocity
			self.projectille_collision("y")

	def update(self):
		self.projectille_moving()


class melee_weapons(weapons):
	def __init__(self, name, damage, cooldwon, hitbox_x, hitbox_y):
		super().__init__(self, name, damage, cooldwon)
		self.name=name

	def use_weapons(self, target):
		self.attack(target, self.rect.x-TILE_SIZE, self.rect.y, -1, (TILE_SIZE,TILE_SIZE))