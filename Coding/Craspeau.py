import pygame
from Entity import Entite
from Settings import *
import math

class Wolf(Entite):
	def __init__(self, x, y, groups, obs_groups, player, detection_range=100, attack_range=20):
		super().__init__(x, y, groups, obs_groups, color=(0, 255, 0))  # Couleur verte pour le crapaud
		self.player = player
		self.detection_range = detection_range
		self.attack_range = attack_range
		self.is_attacking = False
		self.direction = pygame.math.Vector2()
		self.stop = False
		self.timer_attack = 0
		
		self.state = "idle"
		self.stun_timer = 0
		self.return_timer = 0
		self.direction.x = 0.5
		self.direction.y = 0

		self.sprites.append(pygame.image.load("Coding\graphics\Monster\Wolf\Idle\Frame1.png"))
		self.sprites.append(pygame.image.load("Coding\graphics\Monster\Wolf\Attack\Frame1.png"))
		self.sprites.append(pygame.image.load("Coding\graphics\Monster\Wolf\Attack\Frame1.png"))
		self.sprites.append(pygame.image.load("Coding\graphics\Monster\Wolf\Attack\Frame3.png"))
		self.sprites.append(pygame.image.load("Coding\graphics\Monster\Wolf\Attack\Frame4.png"))
		

		self.sprites_death = []
		self.count_sprite_death = 0
		self.sprites_death.append(pygame.image.load("Coding\graphics\Monster\Wolf\Death\Frame1.png"))
		self.sprites_death.append(pygame.image.load("Coding\graphics\Monster\Wolf\Death\Frame2.png"))
		self.sprites_death.append(pygame.image.load("Coding\graphics\Monster\Wolf\Death\Frame3.png"))
		self.sprites_death.append(pygame.image.load("Coding\graphics\Monster\Wolf\Death\Frame4.png"))
		self.sprites_death.append(pygame.image.load("Coding\graphics\Monster\Wolf\Death\Frame5.png"))
		self.sprites_death.append(pygame.image.load("Coding\graphics\Monster\Wolf\Death\Frame6.png"))
		self.sprites_death.append(pygame.image.load("Coding\graphics\Monster\Wolf\Death\Frame7.png"))

		self.sprites_stun = []
		self.count_sprite_stun = 0
		self.sprites_stun.append(pygame.image.load("Coding\graphics\Monster\Wolf\Stun\Frame1.png"))
		self.sprites_stun.append(pygame.image.load("Coding\graphics\Monster\Wolf\Stun\Frame2.png"))
		self.sprites_stun.append(pygame.image.load("Coding\graphics\Monster\Wolf\Stun\Frame3.png"))
		self.sprites_stun.append(pygame.image.load("Coding\graphics\Monster\Wolf\Stun\Frame4.png"))

		self.image = self.sprites[self.current_sprite]

	def distance_player(self, player):
		"""Calcule la distance entre le spectre et le joueur."""
		# Calcule la différence de position en x entre le belier et le joueur.
		dx = player.rect.centerx - self.rect.centerx
		return dx

	def detect_player(self, player):
		"""Vérifie si le joueur est dans le rayon de détection du spectre."""
		# Calcule la distance entre le spectre et le joueur.
		distance = self.distance_player(player)
		y = self.rect.centery
		#debug print : print("la valeur de y est",y)
		self.range = [z for z in range(y-10,y+10)]
		# Retourne True si le joueur est à portée de détection, sinon False.
		return distance < self.detection_range and player.rect.centery in self.range

	def update_attack(self):
		print('gauche' in self.move() or 'droite' in self.move())
		if 'gauche' in self.move() or 'droite' in self.move() or self.attack_timer >= 40:
			self.state = "stun"
		self.rect.x += self.direction.x

		# Met à jour l'animation toutes les 10 frames.
		if self.attack_timer % 10 == 0:
			if self.current_sprite >= 4:
				self.current_sprite = 0
			else:

				if self.direction.x < 0:
					self.current_sprite += 1
					self.image = self.sprites[self.current_sprite]
				else:
					self.image = pygame.transform.flip(self.sprites[self.current_sprite], True, False)

		self.attack_timer += 1

	def update_stun(self):
		if self.stun_timer >= 30:
			self.state = "return"
			self.direction = pygame.math.Vector2()
		if self.stun_timer % 10 == 0:
			self.image = self.sprites_stun[self.count_sprite_stun]
			self.count_sprite_stun += 1

		self.stun_timer += 1
		


	def update_return(self):
		self.current_sprite = 0
		self.count_sprite_stun = 0
		self.image = self.sprites[self.current_sprite]
		self.direction.x = -self.direction.x

		if self.return_timer >= 5:
			self.state = "idle"
		self.return_timer += 1




	def start_attack(self, player):
		"""Initialise l'attaque sur le joueur."""
		# Passe l'état du belier à "attack".
		self.state = "attack"

		# Réinitialise le compteur d'attaque.
		self.attack_timer = 0

		# Stocke la position actuelle du spectre comme position de départ.
		self.start_pos = (self.rect.x, self.rect.y)

		# Stocke la position actuelle du joueur comme cible de l'attaque.
		self.target_pos = (player.rect.x, player.rect.y)

		print("position =",self.start_pos[0] - self.target_pos[0])
		if self.start_pos[0] - self.target_pos[0] > 0:
			self.direction.x = -self.direction.x

	def update(self):
		"""Met à jour le comportement du spectre en fonction de son état actuel."""
		if self.state == "idle":
			#print("Idle")
			# Si le spectre est inactif, vérifie s'il détecte le joueur.
			if self.detect_player(self.player):
				print("Attack started")
				self.start_attack(self.player)
			else:
				pass
				"self.idle_behavior()"

		elif self.state == "attack":
			#print("Attack")
			# Met à jour l'attaque du spectre.
			self.update_attack()

		elif self.state == "stun":
			#print("stun")
			self.update_stun()

		elif self.state == "return":
			# Fait revenir le spectre à sa position initiale.
			print("return")
			self.update_return()
		
		elif self.state == "dead":
			print("Dead")
			self.count_death += 0.125
			self.death()

		self.apply_gravity()
		self.move()

