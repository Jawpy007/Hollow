import pygame, sys 
from Settings import *

class UI:
	def __init__(self,level_type,game):

		#general
		self.game=game
		self.level_type=level_type
		self.display_surface = pygame.display.get_surface()
		self.font =pygame.font.Font(UI_FONT,UI_FONT_SIZE)

		if self.level_type=="game_level":
			#bar setup
			self.dico_bar={} #contient : [self.XXX_bar_rect, [Nom, posx, posy, taille x, taille y], color]
				#health
			self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,HEALTH_BAR_HEIGHT)
			self.dico_bar["hp"]=[self.health_bar_rect, ["hp",10,10,HEALTH_BAR_WIDTH,HEALTH_BAR_HEIGHT], GREEN]
				#mana
			self.energy_bar_rect = pygame.Rect(10,10+HEALTH_BAR_HEIGHT,ENERGY_BAR_WIDTH,ENERGY_BAR_HEIGHT)
			self.dico_bar["mana"]=[self.energy_bar_rect, ["mana",10,10+HEALTH_BAR_HEIGHT,ENERGY_BAR_WIDTH,ENERGY_BAR_HEIGHT], YELLOW]
				#xp
			self.xp_bar_rect = pygame.Rect(10,10+HEALTH_BAR_HEIGHT*2,XP_BAR_WIDTH,XP_BAR_HEIGHT)
			self.dico_bar["xp"]=[self.xp_bar_rect, ["xp",10,10+HEALTH_BAR_HEIGHT*2,XP_BAR_WIDTH,XP_BAR_HEIGHT], BLUEXP]

		if self.level_type=="main_menu":
			decalage = PLAY_BUT_SIZE["y"]
			self.play_but = pygame.Rect(WIDTH//2-PLAY_BUT_SIZE["x"]//2,HEIGTH//2-PLAY_BUT_SIZE["y"]//2 + decalage*0 ,PLAY_BUT_SIZE["x"],PLAY_BUT_SIZE["y"])
			self.options_but = pygame.Rect(WIDTH//2-PLAY_BUT_SIZE["x"]//2,HEIGTH//2-PLAY_BUT_SIZE["y"]//2 + decalage*1 +  PLAY_BUT_SIZE["y"],PLAY_BUT_SIZE["x"],PLAY_BUT_SIZE["y"])
			self.charger_but = pygame.Rect(WIDTH//2-PLAY_BUT_SIZE["x"]//2,HEIGTH//2-PLAY_BUT_SIZE["y"]//2 + decalage*3 +  PLAY_BUT_SIZE["y"],PLAY_BUT_SIZE["x"],PLAY_BUT_SIZE["y"])
			self.quit_but = pygame.Rect(WIDTH//2-PLAY_BUT_SIZE["x"]//2,HEIGTH//2-PLAY_BUT_SIZE["y"]//2 + decalage*5 +  PLAY_BUT_SIZE["y"],PLAY_BUT_SIZE["x"],PLAY_BUT_SIZE["y"])

			self.dico_buts = {
			"Play": [self.play_but, "Commencer Le Jeu"],
			"Options": [self.options_but, "Options"],
			"Charger": [self.charger_but, "Charger"],
			"Quitter": [self.quit_but, "Quitter Le Jeu"]
			}



	def draw_bar(self,elem_de_bar):

		stats=self.player.stats[elem_de_bar[1][0]]
		max_stats=stats["max_value"]
		min_stats=stats["value"]

		bar_len_x=(min_stats*100)/max_stats

		bar_len_x=bar_len_x*(elem_de_bar[1][3]-4)/100

		inside_bar=pygame.Rect(elem_de_bar[1][1]+2,elem_de_bar[1][2]+2,bar_len_x,elem_de_bar[1][4]-4)

		bar_color=elem_de_bar[-1] #prend la couleur de la bar
		bar=elem_de_bar[0]
		pygame.draw.rect(self.display_surface,bar_color,bar)
		pygame.draw.rect(self.display_surface,(101,100,222),inside_bar)

	def input(self):
		mouse=pygame.mouse.get_pressed()
		keys=pygame.key.get_pressed()
		cliquedroit=mouse[0]

		if self.level_type=="main_menu":
			if cliquedroit:
				mouse_cord=pygame.mouse.get_pos()
				
				if self.play_but.collidepoint(mouse_cord):
					self.game.change_level("game_level")
				if self.quit_but.collidepoint(mouse_cord):
					pygame.quit()  # Quitte pygame
					sys.exit()  # Ferme proprement le programme
		if self.level_type=="game_level":
			if keys[pygame.K_ESCAPE]:
				self.game.change_level("main_menu")


	def display(self,player=None):

		if self.level_type=="game_level":
			self.player=player


			for elem_de_bar in self.dico_bar.keys():
				self.draw_bar(self.dico_bar[elem_de_bar])
			self.input()
		elif self.level_type=="main_menu":

			for but in self.dico_buts.values():
				#pygame.draw.rect(self.display_surface, (0, 0, 255), but[0]) #debug
				play_text = self.font.render(but[1], True, "white")  # True pour activer l'antialiasing
				text_rect = play_text.get_rect(center=but[0].center)  # Centrer le texte sur le bouton
				self.display_surface.blit(play_text, text_rect)
				self.input()