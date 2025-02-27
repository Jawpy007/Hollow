import pygame
from Settings import *
from Entity import CreateHitbox
import math

class weapons:
	def __init__(self, name, damage, cooldown):
		self.name = name
		self.damage = damage
		self.cooldown = cooldown * 3
		self.attack_time = pygame.time.get_ticks()
		self.current_time = pygame.time.get_ticks()

class melee_weapons(weapons):
	def __init__(self, name, damage, cooldown):
		super().__init__(name, damage, cooldown)

	def update(self):
		pass

class ranged_weapons(weapons):
	def __init__(self, name, damage, cooldown, range, fire_ready_cooldown, reload_time, visible_groups, magazine_size, player, eni_group):
		super().__init__(name, damage, cooldown)
		
		self.fire_ready_cooldown = fire_ready_cooldown
		self.last_shot_time = pygame.time.get_ticks()
		self.eni_group = eni_group
		self.range = range
		self.reload_time = reload_time
		self.attacking = False
		self.current_projectile = []
		self.projectile_cooldown = []
		self.visible_groups = visible_groups
		self.ammo = magazine_size
		self.player = player
		self.magazine_size = magazine_size
		self.starting_reloading_time = pygame.time.get_ticks()
		self.reloading = False
		self.damage = damage

	def use_weapons(self, user):
		mouse_pos = self.visible_groups.get_world_mouse_pos()
		player_pos = user.rect.center

		angle = math.atan2(mouse_pos[1] - player_pos[1], mouse_pos[0] - player_pos[0])
		speed = 10  # Vitesse du projectile
		x_force = math.cos(angle) * speed
		y_force = math.sin(angle) * speed
		
		attack_time = pygame.time.get_ticks()
		self.ammo -= 1
		self.attacking = True
		self.projectile_cooldown.append(attack_time)
		self.current_projectile.append(
			projectille(y_force, x_force, user.rect.centerx, user.rect.centery-16, user, self.visible_groups, self.player, self.cooldown, self.eni_group, self.damage)
		)
		self.last_shot_time = pygame.time.get_ticks()
		return x_force

	def reload(self):
		if not self.reloading:
			self.reloading = True
			self.starting_reloading_time = pygame.time.get_ticks()
	
	def projectile_pos_update(self):
		if not self.current_projectile:
			self.attacking = False
		else:
			if self.current_time - self.projectile_cooldown[0] > self.cooldown:
				self.current_projectile[0].sprite.kill()
				self.current_projectile.pop(0)
				self.projectile_cooldown.pop(0)
			
			for projectile in self.current_projectile:
				projectile.update()
	
	def update(self):
		self.current_time = pygame.time.get_ticks()
		if self.reloading and self.current_time - self.starting_reloading_time > self.reload_time:
			self.ammo = self.magazine_size
			self.reloading = False
		if self.attacking:
			self.projectile_pos_update()

class projectille(pygame.sprite.Sprite):
	def __init__(self, y_velocity, x_velocity, start_pos_x, start_pos_y, user, visible_groups, player, cooldown, eni_groups, damage):

		self.cooldown = cooldown
		self.player = player
		self.x_velocity = x_velocity
		self.y_velocity = y_velocity  
		self.x = start_pos_x
		self.y = start_pos_y
		self.user = user
		self.visible_groups = visible_groups
		self.sprite = CreateHitbox(self.x, self.y, groups_hit=self.visible_groups)
		self.stop = False
		self.eni_groups = eni_groups
		self.damage = damage
		self.timeur=0

	def projectille_collision(self):
		for sprite in self.player.obs_groups:
			if sprite.rect.colliderect(self.sprite.rect):
				self.stop = True

		for sprite in self.eni_groups:
			if self.sprite.rect.colliderect(sprite.rect):
				sprite.stats_update("hp", self.damage)
				self.stop = True

	def update(self):
		if not self.stop:
			self.sprite.rect.x += self.x_velocity
			self.sprite.rect.y += self.y_velocity
			self.projectille_collision()
		if self.stop and self.timeur >50:
			self.sprite.kill()
		else:
			self.timeur+=1

