import pygame  # Bibliothèque pygame pour gérer le jeu, et sys pour gérer la fermeture de la fenêtre
from Settings import *  # Importation des paramètres prédéfinis 
from Player import *
from Enemy import Monstre  # Importation de la classe Monstre
from Spectre import Spectre  # Import de classe Spectre
from tile import *
from Craspeau import *
from Ui import UI
from pnj import pnj

class CreateLevel():
	def __init__(self,LevelName,Screen, game):
		self.level_name=LevelName
		if self.level_name=="game_level":

				
			self.visible_sprites = YSortCameraGroup() #Sprite Visible par le joueur exemple texture
			self.obstacles_sprites = pygame.sprite.Group() #Sprite non Visible par le joueur exemple Hit-Box
			self.enemy_sprites = pygame.sprite.Group() #Sprite non Visible par le joueur exemple Hit-Box
			self.items_sprites= pygame.sprite.Group()
			self.climp_zone=pygame.sprite.Group()
			self.clickable_items=pygame.sprite.Group()

			self.ui=UI("game_level", game, self)
			self.screen=Screen
			self.create_map(WORLD_MAP)
	
	def create_map(self,Map):
		img= pygame.image.load('Coding/graphics/tilemap/ground/stone.png').convert()
		img_climp= pygame.image.load('Coding/graphics/tilemap/ground/climbable wall.png').convert()
		self.tiles_liste=[]
		self.player = Player(0, 0, self.visible_sprites, self.enemy_sprites, self.obstacles_sprites, self.climp_zone, self.visible_sprites)  # Instance du joueur
		for LigneIndex, Ligne in enumerate(Map):
			for ColIndex, Col in enumerate(Ligne):
				if Col!=VOID_CHR:
					x = ColIndex * TILE_SIZE
					y = LigneIndex * TILE_SIZE
					if Col=="p":
						self.player.rect.x=x
						self.player.rect.y=y
					elif Col=="m":
						Monstre(x, y, [self.visible_sprites,self.enemy_sprites], self.player, self.obstacles_sprites)  # Instance d'un monstre
					elif Col=="s":
						Spectre(x, y, [self.visible_sprites,self.enemy_sprites], self.player, self.obstacles_sprites) #Instance d'un spectre
					elif Col=="x":
						CreateTiles(x, y, [self.visible_sprites,self.obstacles_sprites], img)
					elif Col=="climp_wall_r":
						CreateTiles(x, y, [self.visible_sprites,self.obstacles_sprites,self.climp_zone], img_climp, Col)
					elif Col=="climp_wall_g":
						CreateTiles(x, y, [self.visible_sprites,self.obstacles_sprites,self.climp_zone], img_climp, Col)
					elif Col=="n":
						pnj(x, y, [self.visible_sprites,self.obstacles_sprites, self.clickable_items],self.obstacles_sprites)

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		self.ui.display(self.player)
		

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		
		#setup general
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_widht = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()
   
		#création le sol
		self.floor_surf = pygame.image.load('Coding/graphics/tilemap/ground/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
		  
	def custom_draw(self,player):

		#obtenir le joueur quand il part
		self.offset.x = player.rect.centerx - self.half_widht
		self.offset.y = player.rect.centery - self.half_height

		#dessiner le sol
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf, floor_offset_pos)
		for sprite in self.sprites():
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
			
	def get_world_mouse_pos(self):
		mouse_x, mouse_y = pygame.mouse.get_pos()
		return pygame.math.Vector2(mouse_x + self.offset.x, mouse_y + self.offset.y)
