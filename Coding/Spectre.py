# Importe les modules nécessaires.
import pygame
import math
from Entity import Entite
from time import * 

# La classe Spectre hérite de la classe Entite, ce qui signifie qu'elle possède toutes les propriétés et méthodes de Entite.
class Spectre(Entite):
	def __init__(self, x, y, groups, player, obs_groups, color=(128, 0, 128), speed=2, detection_radius=300):
		# Appelle le constructeur de la classe parente Entite pour initialiser les attributs communs.
		# Cela inclut la position initiale, les groupes, les obstacles, et la couleur.
		super().__init__(x, y, groups, obs_groups, color=color)

		# Vitesse de déplacement du spectre lorsqu'il est en mode inactif.
		self.speed = speed

		# Rayon de détection : distance à laquelle le spectre peut détecter le joueur.
		self.detection_radius = detection_radius

		# Rayon d'attaque : distance à laquelle le spectre peut attaquer le joueur.
		self.attack_radius = 50

		# Indique si le joueur a été touché par une attaque.
		self.hit = False

		# Référence au joueur, nécessaire pour calculer la distance et détecter le joueur.
		self.player = player

		# Direction de déplacement du spectre, initialisée à un vecteur vide.
		self.direction = pygame.math.Vector2()

		# État actuel du spectre. Peut être "idle", "attack", "return", ou "waiting".
		self.state = "idle"

		# Compteur pour l'attaque, mesuré en frames.
		self.attack_timer = 0

		# Durée totale de l'attaque en frames (par exemple, 60 frames = 1 seconde à 60 FPS).
		self.attack_duration = 60

		# Temps d'attente avant de pouvoir attaquer à nouveau, en frames.
		self.wait_time = 10

		# Timer pour le mode "waiting".
		self.wait_timer = 0.0

		# Position de départ du spectre, utilisée pour revenir après une attaque.
		self.start_pos = (x, y)

		# Position du joueur au début de l'attaque, utilisée pour calculer la trajectoire.
		self.target_pos = None

		# Amplitude du mouvement en courbe lors de l'attaque.
		self.attack_amplitude = 100

		# Position de base où le spectre retourne après une attaque.
		self.end_pos = (800, 500)

		# Iterateur pour les sprites de morts
		self.count_death = 0

		#moove()
		self.direction.x = 0.2

		# Sprite de mort
		self.sprites_death = []
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame1.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame2.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame3.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame4.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame5.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame6.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame7.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame8.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame9.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame10.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame11.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame12.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame13.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame14.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame15.png'))
		self.sprites_death.append(pygame.image.load('Coding/graphics/Specter_Animation/Death/Frame16.png'))

		# Chargement des images d'animation pour l'attaque.
		# Chaque image représente une frame de l'animation.
		self.sprites.append(pygame.image.load('Coding/graphics/Specter_Animation/Attack/Frame1.png'))
		self.sprites.append(pygame.image.load('Coding/graphics/Specter_Animation/Attack/Frame2.png'))
		self.sprites.append(pygame.image.load('Coding/graphics/Specter_Animation/Attack/Frame3.png'))
		self.sprites.append(pygame.image.load('Coding/graphics/Specter_Animation/Attack/Frame4.png'))
		self.sprites.append(pygame.image.load('Coding/graphics/Specter_Animation/Attack/Frame5.png'))
		self.sprites.append(pygame.image.load('Coding/graphics/Specter_Animation/Attack/Frame6.png'))

		# Initialisation de l'image actuelle à la première frame de l'animation.
		self.image = self.sprites[self.current_sprite]

		# Crée un rectangle représentant la zone occupée par l'image sur l'écran.
		self.rect = self.image.get_rect()

		# Positionne le rectangle à la position initiale du spectre.
		self.rect.topleft = [x, y]

	def distance_player(self, player):
		"""Calcule la distance entre le spectre et le joueur."""
		# Calcule la différence de position en x et en y entre le spectre et le joueur.
		dx = player.rect.centerx - self.rect.centerx
		dy = player.rect.centery - self.rect.centery

		# Utilise le théorème de Pythagore pour calculer la distance euclidienne.
		distance = math.sqrt(dx**2 + dy**2)
		return distance

	def detect_player(self, player):
		"""Vérifie si le joueur est dans le rayon de détection du spectre."""
		# Calcule la distance entre le spectre et le joueur.
		distance = self.distance_player(player)

		# Retourne True si le joueur est à portée de détection, sinon False.
		return distance < self.detection_radius

	def start_attack(self, player):
		"""Initialise l'attaque sur le joueur."""
		# Passe l'état du spectre à "attack".
		self.state = "attack"

		# Réinitialise le compteur d'attaque.
		self.attack_timer = 0

		# Stocke la position actuelle du spectre comme position de départ.
		self.start_pos = (self.rect.x, self.rect.y)

		# Stocke la position actuelle du joueur comme cible de l'attaque.
		self.target_pos = (player.rect.x, player.rect.y)

		# Calcule la position de fin de l'attaque en fonction de la symétrie axiale.
		if self.start_pos[0] < player.rect.centerx:
			self.end_pos = (self.start_pos[0] + self.distance_player(player), self.start_pos[1])
			self.speed = -self.speed
		else:
			self.end_pos = (self.start_pos[0] - self.distance_player(player), self.start_pos[1])

	def update_attack(self):
		"""Met à jour la position du spectre pendant l'attaque, suivant une trajectoire courbée."""
		# Calcule la progression de l'attaque (t varie de 0 à 1).
		t = self.attack_timer / self.attack_duration

		# Si l'attaque est terminée, passe à l'état "return".
		if t > 1:
			self.state = "return"
			self.attack_timer = 0
			return

		# Vérifie si le joueur est à portée d'attaque et n'a pas encore été touché.
		if self.distance_player(self.player) < self.attack_radius and not self.hit:
			print("Tapé")
			# Attaque le joueur en réduisant ses points de vie.
			self.attack([self.player], self.rect.x, self.rect.y, 5)
			self.hit = True

		# Met à jour l'animation toutes les 10 frames.
		if self.attack_timer % 10 == 0:
			if self.current_sprite >= 5:
				self.current_sprite = 0
			else:

				if self.speed < 0:
					self.current_sprite += 1
					self.image = self.sprites[self.current_sprite]
				else:
					self.image = pygame.transform.flip(self.sprites[self.current_sprite], True, False)

		# Calcule la nouvelle position du spectre en fonction de la progression de l'attaque.
		x0, y0 = self.start_pos
		target_x, target_y = self.target_pos
		new_x = x0 + (target_x - x0) * t
		new_y = y0 + (target_y - y0) * t

		# Ajoute une courbe à la trajectoire en utilisant une fonction sinus.
		curve_offset = self.attack_amplitude * math.sin(math.pi * t)
		new_y += curve_offset

		# Met à jour la position du spectre.
		self.rect.x = new_x
		self.rect.y = new_y

		# Incrémente le compteur d'attaque.
		self.attack_timer += 1

	def update_return(self):
		"""Fait revenir le spectre à sa position initiale après une attaque."""
		# Calcule la progression du retour (t varie de 0 à 1).
		t = self.attack_timer / self.attack_duration

		# Si le retour est terminé, passe à l'état "waiting".
		if t > 1:
			self.state = "waiting"
			self.wait_timer = 0
			self.current_sprite = 0
			if self.speed < 0:
				self.image = self.sprites[self.current_sprite]
			else:
				self.image = pygame.transform.flip(self.sprites[self.current_sprite], True, False)
			self.hit = False
			return

		# Calcule la nouvelle position du spectre en fonction de la progression du retour.
		target_x, target_y = self.end_pos
		start_x, start_y = self.rect.x, self.rect.y
		new_x = start_x + (target_x - start_x) * t
		new_y = start_y + (target_y - start_y) * t

		# Met à jour la position du spectre.
		self.rect.x = new_x
		self.rect.y = new_y

		# Incrémente le compteur d'attaque.
		self.attack_timer += 1

	def idle_behavior(self):
		"""Gère le comportement du spectre en mode inactif, en le faisant se déplacer horizontalement."""
		# Déplace le spectre horizontalement à la vitesse définie.
		collision = self.move()
		zone = (self.rect.centerx-100,self.rect.centerx+100)
		# Si le spectre sort de l'écran, inverse sa direction.
		#print(zone, self.rect.right,self.rect.left)
		#print(collision)
		if self.rect.right > zone[1] or self.rect.left < zone[0] or "droite" in collision or "gauche" in collision:
			self.direction.x = -self.direction.x
			self.image = pygame.transform.flip(self.sprites[self.current_sprite], True, False)
			
			
	def death(self):
		self.count_death += 0.125
		if int(self.count_death) == len(self.sprites_death)-1:
			self.player.stats_update("xp", 10)
			self.kill()

		self.state = "dead"
		self.image = self.sprites_death[int(self.count_death)]

	def update(self):
		"""Met à jour le comportement du spectre en fonction de son état actuel."""
		if self.state == "idle":
			# Si le spectre est inactif, vérifie s'il détecte le joueur.
			if self.detect_player(self.player):
				self.start_attack(self.player)
			else:
				self.idle_behavior()

		elif self.state == "attack":
			# Met à jour l'attaque du spectre.
			self.update_attack()

		elif self.state == "return":
			# Fait revenir le spectre à sa position initiale.
			self.update_return()

		elif self.state == "waiting":
			# Incrémente le timer d'attente.
			self.wait_timer += 1
			# Si le temps d'attente est écoulé, repasse en mode inactif.
			if self.wait_timer > self.wait_time:
				self.state = "idle"
		
		elif self.state == "dead":
			self.death()
