
from Settings import *  # Importation des paramètres du jeu
from Entity import *  # Importation de la classe de base des entités
from Weapons import *  # Importation des armes
from Inventory import *  # Importation de l'inventaire
from Graphics import import_folder  # Importation de la fonction pour charger les dossiers graphiques

"""
Une classe Player qui hérite de Entite, avec ses propres mouvements et sauts.
"""

class Player(Entite):
	def __init__(self, x, y, groups, eni_groups, obs_groups, climp_zone, visible_groups, color=(255, 255, 255)):
		"""Initialisation du joueur avec ses attributs et ses groupes de sprites"""
		super().__init__(x, y, groups, obs_groups, color)  # Initialisation de la classe parente Entite

		# Variables graphiques de base du joueur
		self.player_image = pygame.Surface((TILE_SIZE, TILE_SIZE))  # Création de la surface du joueur
		self.player_layer = 1  # Couche du joueur
		self.effect = None  # Effet graphique
		self.frame_index = 0  # Index de l'animation
		self.animation_speed = 0.5  # Vitesse de l'animation

		# Variables de statut du joueur
		self.status = "right"  # Statut initial du joueur
		self.attacking = False  # Le joueur attaque-t-il ?
		self.bowing = False  # Le joueur utilise-t-il un arc ?
		self.attack_time = pygame.time.get_ticks()  # Temps de l'attaque
		self.attack_side = ""  # Côté de l'attaque

		# Groupes de sprites des ennemis du joueur
		self.eni_groups = eni_groups  # Groupes des ennemis

		# Variables de statistiques
		self.inventory = inventory()  # Inventaire du joueur
		self.player_xp_level = 1  # Niveau d'expérience du joueur
		self.stats = {"mana": {"value": 10, "max_value": 100}, "xp": {"value": 0, "max_value": 100}, "hp": {"value": 100, "max_value": 100}}  # Statistiques du joueur

		# Variables de mouvement
		self.direction = pygame.math.Vector2()  # Direction du joueur

		# Mouvement horizontal
		self.dashing_last = [False, pygame.time.get_ticks()]  # Dernier dash
		self.dashing = False  # Le joueur dash-t-il ?
		self.running = False  # Le joueur court-il ?

		# Mouvement vertical
		self.jump_count = MAXJUMP  # Nombre de sauts restants
		self.in_jump = False  # Le joueur est-il en train de sauter ?
		self.in_jump_time = pygame.time.get_ticks()  # Temps du saut

		# Variables pour le wall jump
		self.climp_zone = climp_zone  # Zone d'escalade
		self.walljump = None  # Le joueur est-il en train de faire un wall jump ?
		self.walljump_time = pygame.time.get_ticks()  # Temps du wall jump
		self.lastwalljump = None  # Dernier wall jump
		self.lastwalljump_cooldown = pygame.time.get_ticks()  # Temps de recharge du wall jump
		self.wall_jump_jump_left = False  # Le joueur fait-il un wall jump à gauche ?
		self.wall_jump_jump_left_cooldown = pygame.time.get_ticks()  # Temps de recharge du wall jump à gauche
		self.wall_jump_jump_right = False  # Le joueur fait-il un wall jump à droite ?
		self.wall_jump_jump_right_cooldown = pygame.time.get_ticks()  # Temps de recharge du wall jump à droite

		# Variables de détection de touches
		self.spacebar_key_block = False  # Blocage de la touche espace
		self.r_key_block = False  # Blocage de la touche R
		self.K_d_doubletap = [pygame.time.get_ticks(), pygame.time.get_ticks()]  # Double tap sur la touche D
		self.K_q_doubletap = [pygame.time.get_ticks(), pygame.time.get_ticks()]  # Double tap sur la touche Q

		self.import_player_assets()  # Chargement des assets graphiques du joueur

	def death(self):
		"""Gère la mort du joueur"""
		self.rect.x = 50  # Réinitialisation de la position x du joueur
		self.rect.y = 50  # Réinitialisation de la position y du joueur
		self.stats_update("hp", 100)  # Réinitialisation des points de vie du joueur

	def import_player_assets(self):
		"""Importe les assets graphiques du joueur"""
		chr_path = "Coding/graphics/player/"  # Chemin des assets graphiques du joueur
		self.animations = {
			'left': [], 'right': [], 'right_idle': [], 'left_idle': [],
			'right_attack': [], 'left_attack': [], 'right_bow': [], 'left_bow': [],
			'right_dash': [], 'left_dash': []
		}  # Dictionnaire des animations du joueur
		for animation in self.animations.keys():
			full_path = chr_path + animation  # Chemin complet de l'animation
			self.animations[animation] = import_folder(full_path)  # Importation des images d'animation

	def get_status(self):
		"""Met à jour le statut du joueur en fonction de ses actions"""
		if self.direction.x == 0:
			if not "idle" in self.status and not "attack" in self.status and not "bow" in self.status:
				self.status = self.status + "_idle"  # Le joueur est à l'arrêt

		if self.attacking and not self.dashing:
			if not self.bowing:
				if not "attack" in self.status:
					if "idle" in self.status:
						self.status = self.status.replace("_idle", "_attack")  # Le joueur attaque
					else:
						self.status = self.status + "_attack"  # Le joueur attaque
					if "_bow" in self.status:
						self.status = self.status.replace("_bow", "")  # Le joueur n'utilise pas l'arc
			else:
				if not "_bow" in self.status:
					self.status = self.attack_side + "_bow"  # Le joueur utilise l'arc
					if "attack" in self.status:
						self.status = self.status.replace("_attack", "")  # Le joueur n'attaque pas
		else:
			if "attack" in self.status:
				self.status = self.status.replace("_attack", "")  # Le joueur n'attaque pas
			if "_bow" in self.status:
				self.status = self.status.replace("_bow", "")  # Le joueur n'utilise pas l'arc

		if self.dashing:
			if not "dash" in self.status:
				if "idle" in self.status:
					self.status = self.status.replace("_idle", "_dash")  # Le joueur dash
				else:
					self.status = self.status + "_dash"  # Le joueur dash
		else:
			if "_dash" in self.status:
				self.status = self.status.replace("_dash", "")  # Le joueur ne dash pas

	def input(self):
		"""Gère les entrées clavier et souris pour contrôler le joueur"""
		self.direction = pygame.math.Vector2()  # Réinitialisation de la direction du joueur
		keys = pygame.key.get_pressed()  # Récupération des touches pressées
		mouse = pygame.mouse.get_pressed()  # Récupération des boutons de la souris pressés
		cliquedroit = mouse[0]  # Bouton gauche de la souris

		if (keys[pygame.K_q] and not self.walljump) or self.wall_jump_jump_left:
			self.status = "left"  # Le joueur va à gauche
			if self.current_time - self.K_q_doubletap[0] < 200 and self.current_time - self.K_q_doubletap[1] < 200 and not self.q_key_block and self.current_time - self.lastwalljump_cooldown > 700 and not self.wall_jump_jump_left:
				self.dashing = True  # Le joueur dash
			self.direction.x += -1  # Direction vers la gauche
			self.K_q_doubletap[0] = pygame.time.get_ticks() if not self.wall_jump_jump_left else self.K_q_doubletap[0]  # Mise à jour du double tap
			self.q_key_block = True if not self.wall_jump_jump_left else False  # Blocage de la touche Q

		if (keys[pygame.K_d] and not self.walljump) or self.wall_jump_jump_right:
			self.status = "right"  # Le joueur va à droite
			if self.current_time - self.K_d_doubletap[0] < 200 and self.current_time - self.K_d_doubletap[1] < 200 and not self.d_key_block and self.current_time - self.lastwalljump_cooldown > 200 and not self.wall_jump_jump_right:
				self.dashing = True  # Le joueur dash
			self.direction.x += 1  # Direction vers la droite
			self.K_d_doubletap[0] = pygame.time.get_ticks() if not self.wall_jump_jump_right else self.K_d_doubletap[0]  # Mise à jour du double tap
			self.d_key_block = True if not self.wall_jump_jump_right else False  # Blocage de la touche D

		if keys[pygame.K_SPACE] and self.jump_count > 0 and not self.spacebar_key_block:
			if self.walljump == "droite":
				self.wall_jump_jump_left = True  # Le joueur fait un wall jump à gauche
				self.wall_jump_jump_left_cooldown = pygame.time.get_ticks()  # Temps de recharge du wall jump à gauche
			elif self.walljump == "gauche":
				self.wall_jump_jump_right = True  # Le joueur fait un wall jump à droite
				self.wall_jump_jump_right_cooldown = pygame.time.get_ticks()  # Temps de recharge du wall jump à droite
			self.in_jump = True  # Le joueur saute
			self.jump_count -= 1  # Décrémentation du nombre de sauts restants
			self.in_jump_time = pygame.time.get_ticks()  # Temps du saut
			self.spacebar_key_block = True  # Blocage de la touche espace
			self.walljump = None  # Réinitialisation du wall jump

		if keys[pygame.K_LSHIFT]:
			self.running = True  # Le joueur court

		if keys[pygame.K_e]:
			if not self.attacking:
				if "sword" in self.inventory.items_dict.keys():
					if "left" in self.status:
						self.attack(self.eni_groups, self.rect.x - TILE_SIZE + 10, self.rect.y, -50, (TILE_SIZE + 10, TILE_SIZE))  # Attaque à gauche
						self.attacking = True  # Le joueur attaque
						self.attack_time = pygame.time.get_ticks()  # Temps de l'attaque
					elif "right" in self.status:
						self.attack(self.eni_groups, self.rect.x + TILE_SIZE - 10, self.rect.y, -50, (TILE_SIZE + 10, TILE_SIZE))  # Attaque à droite
						self.attacking = True  # Le joueur attaque
						self.attack_time = pygame.time.get_ticks()  # Temps de l'attaque

		if keys[pygame.K_r]:
			if len(self.inventory.items_dict) > 0 and not self.r_key_block:
				self.inventory.items_dict["bow"].reload()  # Recharge de l'arc
				self.r_key_block = True  # Blocage de la touche R

		if cliquedroit:
			if not self.attacking:
				if "bow" in self.inventory.items_dict.keys():
					self.bowing = True  # Le joueur utilise l'arc
					self.attacking = True  # Le joueur attaque
					self.attack_time = pygame.time.get_ticks()  # Temps de l'attaque
					self.attack_side = self.inventory.items_dict["bow"].use_weapons(self)  # Utilisation de l'arc
					if self.attack_side < 0:
						self.attack_side = "left"  # Attaque à gauche
					else:
						self.attack_side = "right"  # Attaque à droite

		if not keys[pygame.K_d]:
			if self.current_time - self.K_d_doubletap[0] < 200:
				self.K_d_doubletap[1] = pygame.time.get_ticks()  # Mise à jour du double tap
			self.d_key_block = False  # Déblocage de la touche D

		if not keys[pygame.K_q]:
			if self.current_time - self.K_q_doubletap[0] < 200:
				self.K_q_doubletap[1] = pygame.time.get_ticks()  # Mise à jour du double tap
			self.q_key_block = False  # Déblocage de la touche Q

		if not keys[pygame.K_r]:
			self.r_key_block = False  # Déblocage de la touche R

		if not keys[pygame.K_LSHIFT]:
			self.running = False  # Le joueur ne court plus

		if not keys[pygame.K_SPACE]:
			self.spacebar_key_block = False  # Déblocage de la touche espace

	def animate(self):
		"""Anime le joueur en fonction de son statut"""
		animation = self.animations[self.status]  # Récupération de l'animation correspondant au statut du joueur
		self.frame_index += self.animation_speed  # Incrémentation de l'index de l'animation
		if self.frame_index >= len(animation):
			self.frame_index = 0  # Réinitialisation de l'index de l'animation
		x, y = self.rect.x, self.rect.y  # Sauvegarde de la position du joueur
		self.image = animation[int(self.frame_index)]  # Mise à jour de l'image du joueur
		self.rect = self.image.get_rect()  # Mise à jour du rectangle de collision du joueur
		self.rect.topleft = (x, y)  # Restauration de la position du joueur

	def collision_event(self):
		"""Gère les événements de collision avec l'environnement"""
		keys = pygame.key.get_pressed()  # Récupération des touches pressées
		if "climp_gauche" in self.CollisionType and not self.walljump and (keys[pygame.K_q] or self.wall_jump_jump_left) and self.lastwalljump != "gauche":
			self.walljump = "gauche"  # Le joueur fait un wall jump à gauche
			self.walljump_time = pygame.time.get_ticks()  # Temps du wall jump
			self.lastwalljump_cooldown = pygame.time.get_ticks()  # Temps de recharge du wall jump
			self.jump_count = 1  # Réinitialisation du nombre de sauts restants
			self.lastwalljump = "gauche"  # Dernier wall jump à gauche
			self.wall_jump_jump_right = False  # Le joueur ne fait pas de wall jump à droite
			self.wall_jump_jump_left = False  # Le joueur ne fait pas de wall jump à gauche

		elif "climp_droite" in self.CollisionType and not self.walljump and (keys[pygame.K_d] or self.wall_jump_jump_right) and self.lastwalljump != "droite":
			self.walljump = "droite"  # Le joueur fait un wall jump à droite
			self.walljump_time = pygame.time.get_ticks()  # Temps du wall jump
			self.lastwalljump_cooldown = pygame.time.get_ticks()  # Temps de recharge du wall jump
			self.jump_count = 1  # Réinitialisation du nombre de sauts restants
			self.lastwalljump = "droite"  # Dernier wall jump à droite
			self.wall_jump_jump_right = False  # Le joueur ne fait pas de wall jump à droite
			self.wall_jump_jump_left = False  # Le joueur ne fait pas de wall jump à gauche

		elif (self.walljump == "gauche" and "climp_gauche" not in self.CollisionType) or (self.walljump == "droite" and "climp_droite" not in self.CollisionType):
			self.walljump = None  # Réinitialisation du wall jump

		elif "bas" in self.CollisionType:
			self.jump_count = MAXJUMP  # Réinitialisation du nombre de sauts restants

	def move(self):
		"""Gère les déplacements du joueur"""
		self.CollisionType = []  # Réinitialisation des types de collision
		self.collision("climp_zone")  # Vérification des collisions dans la zone d'escalade

		if self.dashing_last[0] and self.current_time - self.dashing_last[1] > 100:
			self.dashing_last[0] = False  # Réinitialisation du dash si le temps est écoulé

		if self.walljump is None and not self.in_jump:
			if self.running:
				self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR / 2  # Déplacement horizontal en courant
				self.collision("x")  # Vérification des collisions horizontales

			if self.dashing:
				self.dashing = False  # Fin du dash
				x, y = self.rect.x, self.rect.y  # Sauvegarde de la position actuelle
				self.rect.topleft = (x, y)  # Mise à jour de la position
				for i in range(20):
					self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR  # Déplacement horizontal en dash
					self.collision("x")  # Vérification des collisions horizontales
				self.dashing_last[0] = True  # Indication que le joueur a dashé
				self.dashing_last[1] = pygame.time.get_ticks()  # Mise à jour du temps du dernier dash

			self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR  # Déplacement horizontal
			self.collision("x")  # Vérification des collisions horizontales
			self.rect.y += self.direction.y * PLAYER_SPEED_MULTIPLICATOR  # Déplacement vertical
			self.collision("y")  # Vérification des collisions verticales

		elif self.in_jump and self.walljump is None:
			if self.wall_jump_jump_right or self.wall_jump_jump_left:
				self.direction.x = self.direction.x * WALL_JUMP_X_SPEED_MULTIPLICATOR  # Ajustement de la direction pour le wall jump
			else:
				if self.dashing:
					self.dashing = False  # Fin du dash
					x, y = self.rect.x, self.rect.y  # Sauvegarde de la position actuelle
					self.rect.topleft = (x, y)  # Mise à jour de la position
					for i in range(20):
						self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR  # Déplacement horizontal en dash
						self.collision("x")  # Vérification des collisions horizontales
					self.dashing_last[0] = True  # Indication que le joueur a dashé
					self.dashing_last[1] = pygame.time.get_ticks()  # Mise à jour du temps du dernier dash
			self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR  # Déplacement horizontal
			self.collision("x")  # Vérification des collisions horizontales
			for i in range(2):
				self.direction.y = -1  # Direction vers le haut
				self.rect.y += self.direction.y * PLAYER_JUMP_MULTIPLICATOR  # Déplacement vertical en saut
				self.collision("y")  # Vérification des collisions verticales

		elif self.walljump is not None:
			if self.walljump == "gauche":
				self.direction.x = -1  # Direction vers la gauche
			else:
				self.direction.x = 1  # Direction vers la droite
			self.rect.x += self.direction.x  # Déplacement horizontal
			self.collision("x")  # Vérification des collisions horizontales
			self.direction.y = 1  # Direction vers le bas
			self.rect.y += self.direction.y  # Déplacement vertical
			self.collision("y")  # Vérification des collisions verticales

	def apply_gravity(self):
		"""Applique la gravité au mouvement vertical du joueur"""
		if self.walljump is None:
			self.direction.y += GRAVITY  # Ajout de la gravité à la direction verticale

	def all_cooldown(self):
		"""Gère les temps de recharge pour diverses actions"""
		if self.walljump and self.current_time - self.walljump_time > WALL_JUMP_COOLDOWN * 10:
			self.walljump = None  # Réinitialisation du wall jump après le cooldown
		if self.in_jump and self.current_time - self.in_jump_time > JUMP_COOLDOWN:
			self.in_jump = False  # Fin du saut après le cooldown
		if self.lastwalljump and self.current_time - self.lastwalljump_cooldown > JUMP_COOLDOWN * 10:
			self.lastwalljump = None  # Réinitialisation du dernier wall jump après le cooldown
		if self.wall_jump_jump_left and self.current_time - self.wall_jump_jump_left_cooldown > JUMP_COOLDOWN * 2:
			self.wall_jump_jump_left = False  # Fin du wall jump à gauche après le cooldown
		if self.wall_jump_jump_right and self.current_time - self.wall_jump_jump_right_cooldown > JUMP_COOLDOWN * 2:
			self.wall_jump_jump_right = False  # Fin du wall jump à droite après le cooldown
		if self.attacking and self.current_time - self.attack_time > JUMP_COOLDOWN:
			self.attacking = False  # Fin de l'attaque après le cooldown
			self.bowing = False  # Fin de l'utilisation de l'arc après le cooldown
			self.attack_side = ""  # Réinitialisation du côté d'attaque

	def collision(self, Direction):
		"""Détecte et réagit aux collisions avec les obstacles"""
		if Direction == "x":
			for sprite in self.obs_groups:
				if sprite.rect.colliderect(self.rect):  # Vérification de la collision horizontale
					if sprite.name == "climp_wall_g":
						if sprite.rect.centerx < self.rect.centerx:
							self.rect.left = sprite.rect.right  # Ajustement de la position en cas de collision à gauche
							self.CollisionType += ["climp_gauche", "gauche"]
						else:
							self.rect.right = sprite.rect.left  # Ajustement de la position en cas de collision à droite
							self.CollisionType += ["droite"]
					elif sprite.name == "climp_wall_r":
						if sprite.rect.centerx > self.rect.centerx:
							self.rect.right = sprite.rect.left  # Ajustement de la position en cas de collision à droite
							self.CollisionType += ["climp_droite", "droite"]
						else:
							self.rect.left = sprite.rect.right  # Ajustement de la position en cas de collision à gauche
							self.CollisionType += ["gauche"]
					elif self.direction.x > 0:
						self.rect.right = sprite.rect.left  # Ajustement de la position en cas de collision à droite
						self.CollisionType += ["droite"]
					elif self.direction.x < 0:
						self.rect.left = sprite.rect.right  # Ajustement de la position en cas de collision à gauche
						self.CollisionType += ["gauche"]
		elif Direction == 'y':
			for sprite in self.obs_groups:
				if sprite.rect.colliderect(self.rect):  # Vérification de la collision verticale
					if self.direction.y > 0:
						self.rect.bottom = sprite.rect.top  # Ajustement de la position en cas de collision en bas
						self.CollisionType += ["bas"]
					elif self.direction.y < 0:
						self.rect.top = sprite.rect.bottom  # Ajustement de la position en cas de collision en haut
						self.CollisionType += ["haut"]

	def player_level_up(self, value=1):
		"""Gère la montée en niveau du joueur"""
		self.player_xp_level += value  # Incrémentation du niveau d'expérience du joueur

	def stats_update(self, nom_stats, value_update, max_value=None):
		"""Met à jour les statistiques du joueur"""
		if max_value is not None:
			self.stats[nom_stats]["max_value"] = max_value  # Mise à jour de la valeur maximale de la statistique

		current_value = self.stats[nom_stats]["value"]  # Récupération de la valeur actuelle de la statistique
		max_value = self.stats[nom_stats]["max_value"]  # Récupération de la valeur maximale de la statistique

		if value_update + current_value > max_value:
			if nom_stats == "hp":
				self.stats[nom_stats]["value"] = max_value  # Limitation de la valeur de la statistique à la valeur maximale
			elif nom_stats == "mana":
				self.stats[nom_stats]["value"] = max_value  # Limitation de la valeur de la statistique à la valeur maximale
			elif nom_stats == "xp":
				self.stats[nom_stats]["value"] = 0  # Réinitialisation de la valeur de l'expérience
				self.player_level_up()  # Montée en niveau du joueur

		elif value_update + current_value <= 0:
			if nom_stats == "hp":
				self.stats[nom_stats]["value"] = 0  # Réinitialisation de la valeur de la statistique
				self.death()  # Gestion de la mort du joueur
			elif nom_stats == "mana":
				return False  # Retourne False si la valeur de mana est insuffisante
			elif nom_stats == "xp":
				reste = value_update + current_value  # Calcul du reste de l'expérience
				self.stats[nom_stats]["value"] = max_value  # Limitation de la valeur de l'expérience à la valeur maximale
				self.player_level_up(-1)  # Décrémentation du niveau d'expérience du joueur
				self.stats_update("xp", reste)  # Mise à jour de l'expérience avec le reste
		else:
			self.stats[nom_stats]["value"] += value_update  # Mise à jour de la valeur de la statistique
		return True  # Retourne True si la mise à jour est réussie

	def update(self):
		"""Boucle principale du joueur"""
		self.current_time = pygame.time.get_ticks()  # Récupération du temps actuel
		self.input()  # Gestion des entrées clavier et souris
		self.apply_gravity()  # Application de la gravité
		self.get_status()  # Mise à jour du statut du joueur
		self.animate()  # Animation du joueur
		self.move()  # Déplacement du joueur
		self.collision_event()  # Gestion des événements de collision
		self.all_cooldown()  # Gestion des temps de recharge
		self.inventory.update()  # Mise à jour de l'inventaire