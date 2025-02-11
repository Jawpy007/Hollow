import pygame, sys
from Settings import *
from Cursor import *
from Dialogues import *

class UI:
	def __init__(self, level_type, game, level):
		# Initialisation des attributs généraux
		self.game = game  # Référence au jeu principal
		self.level_type = level_type  # Type de niveau (game_level ou main_menu)
		self.level = level  # Référence au niveau actuel
		self.display_surface = pygame.display.get_surface()  # Surface d'affichage de Pygame
		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)  # Police de caractères utilisée pour le texte

		self.in_dialogue = False  # Indique si un dialogue est en cours
		self.last_dialogue_skip_time = pygame.time.get_ticks()  # Temps du dernier clic pour passer un dialogue

		# Configuration des barres de statut pour les niveaux de jeu
		if self.level_type == "game_level":
			self.dico_bar = {}  # Dictionnaire pour stocker les barres de statut

			# Barre de santé
			self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
			self.dico_bar["hp"] = [self.health_bar_rect, ["hp", 10, 10, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT], GREEN]

			# Barre de mana
			self.energy_bar_rect = pygame.Rect(10, 10 + HEALTH_BAR_HEIGHT, ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT)
			self.dico_bar["mana"] = [self.energy_bar_rect, ["mana", 10, 10 + HEALTH_BAR_HEIGHT, ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT], YELLOW]

			# Barre d'expérience
			self.xp_bar_rect = pygame.Rect(10, 10 + HEALTH_BAR_HEIGHT * 2, XP_BAR_WIDTH, XP_BAR_HEIGHT)
			self.dico_bar["xp"] = [self.xp_bar_rect, ["xp", 10, 10 + HEALTH_BAR_HEIGHT * 2, XP_BAR_WIDTH, XP_BAR_HEIGHT], BLUEXP]

			# Rectangles pour afficher les dialogues
			self.dialogue_screen = pygame.Rect(0, HEIGHT - 200, WIDTH, 200)
			self.dialogue_pnj_name = pygame.Rect(0, HEIGHT - 200 - 50, 200, 50)

		# Configuration des boutons du menu principal
		elif self.level_type == "main_menu":
			decalage = PLAY_BUT_SIZE["y"]  # Décalage vertical entre les boutons

			# Bouton "Play"
			self.play_but = pygame.Rect(WIDTH // 2 - PLAY_BUT_SIZE["x"] // 2, HEIGHT // 2 - PLAY_BUT_SIZE["y"] // 2 + decalage * 0, PLAY_BUT_SIZE["x"], PLAY_BUT_SIZE["y"])

			# Bouton "Options"
			self.options_but = pygame.Rect(WIDTH // 2 - PLAY_BUT_SIZE["x"] // 2, HEIGHT // 2 - PLAY_BUT_SIZE["y"] // 2 + decalage * 1 + PLAY_BUT_SIZE["y"], PLAY_BUT_SIZE["x"], PLAY_BUT_SIZE["y"])

			# Bouton "Charger"
			self.charger_but = pygame.Rect(WIDTH // 2 - PLAY_BUT_SIZE["x"] // 2, HEIGHT // 2 - PLAY_BUT_SIZE["y"] // 2 + decalage * 3 + PLAY_BUT_SIZE["y"], PLAY_BUT_SIZE["x"], PLAY_BUT_SIZE["y"])

			# Bouton "Quitter"
			self.quit_but = pygame.Rect(WIDTH // 2 - PLAY_BUT_SIZE["x"] // 2, HEIGHT // 2 - PLAY_BUT_SIZE["y"] // 2 + decalage * 5 + PLAY_BUT_SIZE["y"], PLAY_BUT_SIZE["x"], PLAY_BUT_SIZE["y"])

			# Dictionnaire pour stocker les boutons et leurs textes
			self.dico_buts = {
				"Play": [self.play_but, "Commencer Le Jeu"],
				"Options": [self.options_but, "Options"],
				"Charger": [self.charger_but, "Charger"],
				"Quitter": [self.quit_but, "Quitter Le Jeu"]
			}

	def draw_bar(self, elem_de_bar):
		# Récupérer les statistiques du joueur
		stats = self.player.stats[elem_de_bar[1][0]]
		max_stats = stats["max_value"]
		min_stats = stats["value"]

		# Calculer la longueur de la barre en fonction des statistiques
		bar_len_x = (min_stats * 100) / max_stats
		bar_len_x = bar_len_x * (elem_de_bar[1][3] - 4) / 100

		# Dessiner la barre de statut
		inside_bar = pygame.Rect(elem_de_bar[1][1] + 2, elem_de_bar[1][2] + 2, bar_len_x, elem_de_bar[1][4] - 4)
		bar_color = elem_de_bar[-1]
		bar = elem_de_bar[0]
		pygame.draw.rect(self.display_surface, bar_color, bar)
		pygame.draw.rect(self.display_surface, (101, 100, 222), inside_bar)

	def input(self):
		# Gestion des entrées de la souris et du clavier
		mouse = pygame.mouse.get_pressed()
		keys = pygame.key.get_pressed()
		cliquedroit = mouse[0]

		# Gestion des interactions dans le menu principal
		if self.level_type == "main_menu":
			if cliquedroit:
				mouse_cord = pygame.mouse.get_pos()
				if self.play_but.collidepoint(mouse_cord):
					self.game.change_level("game_level")
				elif self.quit_but.collidepoint(mouse_cord):
					pygame.quit()
					sys.exit()

		# Gestion des interactions dans les niveaux de jeu
		elif self.level_type == "game_level":
			if keys[pygame.K_ESCAPE]:
				self.game.change_level("main_menu")

		# Gestion des dialogues
		if cliquedroit:
			if self.in_dialogue:
				self.current_time = pygame.time.get_ticks()
				if self.current_time - self.last_dialogue_skip_time > 200:
					self.next_dialogue()
					self.last_dialogue_skip_time = pygame.time.get_ticks()

	def dialogue_start(self, pnj):
		# Démarrer un dialogue avec un PNJ
		if len(dialogues_dic[pnj.name][pnj.dialogue_states]) > 0:
			self.in_dialogue = [pnj.name, pnj.dialogue_states, 0, pnj]
			self.last_dialogue_skip_time = pygame.time.get_ticks()
		else:
			# Si le PNJ n'a pas de nouveau dialogue, afficher un dialogue générique
			self.in_dialogue = [pnj.name, pnj.generic_dialogue_index, 0, pnj]
			self.last_dialogue_skip_time = pygame.time.get_ticks()
			print("kkl")

	def next_dialogue(self):
		# Passer au dialogue suivant
		self.in_dialogue[2] += 1
		if self.in_dialogue[2] > len(dialogues_dic[self.in_dialogue[0]][self.in_dialogue[1]]) - 1:
			self.in_dialogue = False
		else:
			self.in_dialogue[3].dialogue_states += 1

	def dialogue_draw(self):
		# Dessiner le dialogue à l'écran
		if self.in_dialogue:
			pygame.draw.rect(self.display_surface, "white", self.dialogue_screen)
			texte = dialogues_dic[self.in_dialogue[0]][self.in_dialogue[1]][self.in_dialogue[2]]
			dialogue_text = self.font.render(texte, True, "black")
			dialogue_rect = dialogue_text.get_rect(center=self.dialogue_screen.center)
			self.display_surface.blit(dialogue_text, dialogue_rect)

			pygame.draw.rect(self.display_surface, "white", self.dialogue_pnj_name)
			pnj_name = self.in_dialogue[0]
			pnj_name_texte = self.font.render(pnj_name, True, "black")
			pnj_name__rect = pnj_name_texte.get_rect(center=self.dialogue_pnj_name.center)
			self.display_surface.blit(pnj_name_texte, pnj_name__rect)

	def cursor_gestion(self):
		# Gestion du curseur de la souris

		if self.in_dialogue==False:
			mouse_cord = self.level.visible_sprites.get_world_mouse_pos()
			for sprite in self.level.clickable_items:
				if sprite.rect.collidepoint(mouse_cord):
					if sprite.name == "Chest":
						cursor = pygame.cursors.compile(dialogue_strings)
						pygame.mouse.set_cursor((24, 24), (0, 0), *cursor)
						mouse = pygame.mouse.get_pressed()
						cliquedroit = mouse[0]
						if cliquedroit:
							sprite.give_items()
					else:
						cursor = pygame.cursors.compile(dialogue_strings)
						pygame.mouse.set_cursor((24, 24), (0, 0), *cursor)
						mouse = pygame.mouse.get_pressed()
						cliquedroit = mouse[0]
						if cliquedroit:
							self.dialogue_start(sprite)

	def display(self, player=None):
		# Affichage de l'UI en fonction du type de niveau
		if self.level_type == "game_level":
			self.player = player
			for elem_de_bar in self.dico_bar.keys():
				self.draw_bar(self.dico_bar[elem_de_bar])
			self.input()
			self.cursor_gestion()
			self.dialogue_draw()
		elif self.level_type == "main_menu":
			for but in self.dico_buts.values():
				play_text = self.font.render(but[1], True, "white")
				text_rect = play_text.get_rect(center=but[0].center)
				self.display_surface.blit(play_text, text_rect)
				self.input()

