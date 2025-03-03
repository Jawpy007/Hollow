import pygame, sys
from Settings import *
from Cursor import *
from Dialogues import *
from pygame.math import Vector2

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

			#element du menu pause
			self.menu_rect = pygame.Rect(WIDTH//2-IG_MENU_SIZE[0]//2, HEIGHT//2-IG_MENU_SIZE[1]//2, IG_MENU_SIZE[0], IG_MENU_SIZE[1])
			decalage = 50  # Décalage vertical entre les boutons
			bord_x=(IG_MENU_SIZE[0]-BUT_SIZE["x"])//2 #decalage par rapport au bord x
			bord_y=30 #decalage par rapport au bord y
			print(bord_y, bord_x)
			
			# Bouton "Play"
			self.ig_menu_play_but = pygame.Rect(WIDTH//2-IG_MENU_SIZE[0]//2+bord_x, HEIGHT//2-IG_MENU_SIZE[1]//2+decalage*0+bord_y, BUT_SIZE["x"], BUT_SIZE["y"])

			# Bouton "Options"
			self.ig_menu_options_but = pygame.Rect(WIDTH//2-IG_MENU_SIZE[0]//2+bord_x, HEIGHT//2-IG_MENU_SIZE[1]//2+decalage*1+bord_y, BUT_SIZE["x"], BUT_SIZE["y"])

			# Bouton "Charger"
			#self.ig_menu_charger_but = pygame.Rect(WIDTH//2-IG_MENU_SIZE[0]//2+bord_x, HEIGHT//2-IG_MENU_SIZE[1]//2+decalage*2+bord_y, BUT_SIZE["x"], BUT_SIZE["y"])

			# Bouton "Quitter"
			self.ig_menu_quit_but = pygame.Rect(WIDTH//2-IG_MENU_SIZE[0]//2+bord_x, HEIGHT//2-IG_MENU_SIZE[1]//2+decalage*3+bord_y, BUT_SIZE["x"], BUT_SIZE["y"])

			self.ig_menu_dico_buts = {
				"Play": [self.ig_menu_play_but, "Continuer"],
			#	"Options": [self.ig_menu_options_but, "Options"],
			#	"Charger": [self.ig_menu_charger_but, "Charger"],
				"Quitter": [self.ig_menu_quit_but, "Quitter Le Jeu"]
			}

		# Configuration des boutons du menu principal
		elif self.level_type == "main_menu":
			decalage = BUT_SIZE["y"]  # Décalage vertical entre les boutons

			# Bouton "Play"  
			self.play_but = pygame.Rect(WIDTH // 2 - BUT_SIZE["x"] // 2, HEIGHT // 2 - BUT_SIZE["y"] // 2 + decalage * 0, BUT_SIZE["x"], BUT_SIZE["y"])

			# Bouton "Options"
			self.options_but = pygame.Rect(WIDTH // 2 - BUT_SIZE["x"] // 2, HEIGHT // 2 - BUT_SIZE["y"] // 2 + decalage * 1 + BUT_SIZE["y"], BUT_SIZE["x"], BUT_SIZE["y"])

			# Bouton "Charger"
			self.charger_but = pygame.Rect(WIDTH // 2 - BUT_SIZE["x"] // 2, HEIGHT // 2 - BUT_SIZE["y"] // 2 + decalage * 3 + BUT_SIZE["y"], BUT_SIZE["x"], BUT_SIZE["y"])

			# Bouton "Quitter"
			self.quit_but = pygame.Rect(WIDTH // 2 - BUT_SIZE["x"] // 2, HEIGHT // 2 - BUT_SIZE["y"] // 2 + decalage * 5 + BUT_SIZE["y"], BUT_SIZE["x"], BUT_SIZE["y"])

			# Dictionnaire pour stocker les boutons et leurs textes
			self.dico_buts = {
				"Play": [self.play_but, "Commencer Le Jeu"],
				"Options": [self.options_but, "Options"],
				"Charger": [self.charger_but, "Charger"],
				"Quitter": [self.quit_but, "Quitter Le Jeu"]
			}

	def affiche_menu(self):
		pass
		

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

			if keys[pygame.K_ESCAPE] and not self.K_ESCAPE_block:
				self.level.pause=not self.level.pause
				self.K_ESCAPE_block=True #attendre que la touche soit relacher avant de a novueau prendre cettetouiche en compte
			if not keys[pygame.K_ESCAPE]:
				self.K_ESCAPE_block=False

			# Gestion des dialogues
			if cliquedroit:
				if self.in_dialogue and not self.level.pause:
					self.current_time = pygame.time.get_ticks()
					if self.current_time - self.last_dialogue_skip_time > 200:
						self.next_dialogue()
						self.last_dialogue_skip_time = pygame.time.get_ticks()

				elif self.level.pause:
					mouse_cord = pygame.mouse.get_pos()
					if self.ig_menu_play_but.collidepoint(mouse_cord):
						self.level.pause=False
					elif self.ig_menu_quit_but.collidepoint(mouse_cord):
						pygame.quit()
						sys.exit()		

	def dialogue_start(self, dial_name, dial_states, sprite):
		# Démarrer un dialogue 
		self.in_dialogue = [dial_name, dial_states, 0, sprite]
		self.last_dialogue_skip_time = pygame.time.get_ticks()

	def next_dialogue(self):
		# Passer au dialogue suivant
		print(self.in_dialogue[3])
		if self.in_dialogue:
			self.in_dialogue[2] += 1
			
			if self.in_dialogue[2] >= len(dialogues_dic[self.in_dialogue[0]][self.in_dialogue[1]]): #si on atteint la fin
				if self.in_dialogue[3].dialogue_states+1 >= self.in_dialogue[3].generic_dialogue_index:
					self.in_dialogue[3].dialogue_states=self.in_dialogue[3].generic_dialogue_index # si ont a depasser le nombre de dialogue disponnible alors ont met le meme dialogue en boucle
					self.in_dialogue = False  # Arrêter le dialogue
				else:
					self.in_dialogue[3].dialogue_states+=1 # sinon ont passe a suivant
					self.in_dialogue = False  # Arrêter le dialogue


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
		pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
		if self.in_dialogue==False:
			mouse_cord = self.level.visible_sprites.get_world_mouse_pos()
			if not self.level.pause:
				for sprite in self.level.clickable_items:
					if sprite.rect.collidepoint(mouse_cord):
						if sprite.name == "Chest":
							cursor = pygame.cursors.compile(dialogue_strings)
							pygame.mouse.set_cursor((24, 24), (0, 0), *cursor)
							mouse = pygame.mouse.get_pressed()
							cliquedroit = mouse[0]
							if cliquedroit:
								# Calcul de la distance entre le joueur et le coffre
								player_pos = Vector2(self.level.player.rect.center)
								chest_pos = Vector2(sprite.rect.center)
								distance = player_pos.distance_to(chest_pos)

								# Si la distance est supérieure à 20, on ne fait rien
								if not distance > 60:
									sprite.give_items() # focntion de CreateChest (une class de du fichier Tile) qui donne l'item qui est dans le coffre si le coffre n'est pas deja ouvert
									dial_state=sprite.dialogue_states
									dial_name=sprite.item_name
									self.dialogue_start(dial_name,dial_state, sprite)
						if sprite.name in ["John"] :
							cursor = pygame.cursors.compile(dialogue_strings)
							pygame.mouse.set_cursor((24, 24), (0, 0), *cursor)
							mouse = pygame.mouse.get_pressed()
							cliquedroit = mouse[0]
							if cliquedroit:
								dial_state=sprite.dialogue_states
								dial_name=sprite.name
								self.dialogue_start(dial_name,dial_state,sprite)

	def display(self, player=None):
		# Affichage de l'UI en fonction du type de niveau
		if self.level_type == "game_level":
			self.player = player
			for elem_de_bar in self.dico_bar.keys():
				self.draw_bar(self.dico_bar[elem_de_bar])
			self.input()
			self.cursor_gestion()
			self.dialogue_draw()
			if self.level.pause:
				pygame.draw.rect(self.display_surface, "black", self.menu_rect)
				for but in self.ig_menu_dico_buts.values():
					play_text = self.font.render(but[1], True, "white")
					text_rect = play_text.get_rect(center=but[0].center)
					self.display_surface.blit(play_text, text_rect)
					self.input()


		elif self.level_type == "main_menu":
			for but in self.dico_buts.values():
				play_text = self.font.render(but[1], True, "white")
				text_rect = play_text.get_rect(center=but[0].center)
				self.display_surface.blit(play_text, text_rect)
				self.input()

