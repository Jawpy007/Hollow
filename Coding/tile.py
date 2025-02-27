import pygame
from Settings import *
from Level import *


class CreateTiles(pygame.sprite.Sprite):
    def __init__(self,x, y,groups, img, name=None):
        super().__init__(groups) #Initialisation de la classe parent
        if img==None:
            self.image=pygame.Surface((TILE_SIZE,TILE_SIZE))
            self.image.set_alpha(0)
        else:
            self.image = img
            if name=="climp_wall_r":
                self.image=pygame.transform.rotate(self.image, 180)

        self.name=name
        #self.image.fill("blue")
        self.rect = self.image.get_rect(topleft = (x,y))
    
class CreateChest(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, player,visible_groups, item, item_name):
        super().__init__(groups)  # Initialisation de la classe parent
        # Charger l'image depuis le fichier
        self.item=item
        self.item_name=item_name
        self.image = pygame.image.load("Coding/graphics/tilemap/ground/chest.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))  # Redimensionner
        self.name="Chest"
        self.rect = self.image.get_rect(topleft=(x, y))
        self.player=player
        self.oppened=False
        self.visible_groups=visible_groups

        # gestrion de la boite de dialogue qui s'affiche quand ont recupere l'objet
        self.dialogue_states=0 #index du dialogue qui annonce la recuperation de l'objet
        self.generic_dialogue_index=1 


    def give_items(self):
        if not self.oppened:
            self.image = pygame.image.load("Coding/graphics/tilemap/ground/chest_open.png")
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))  # Redimensionner
            self.name="Chest"
            self.player.inventory.add_items(self.item, self.item_name)
            self.oppened=True