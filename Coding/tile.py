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
    