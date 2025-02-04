import pygame
from Settings import *
from Level import *


class CreateTiles(pygame.sprite.Sprite):
    def __init__(self,x, y,groups, img):
        super().__init__(groups) #Initialisation de la classe parent
        #self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.image = img
        #self.image.fill("blue")
        self.rect = self.image.get_rect(topleft = (x,y))
    