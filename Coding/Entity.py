import pygame
from Settings import *

class Entite(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, obs_groups, surface=None, width=TILE_SIZE, height=TILE_SIZE, color=(255, 255, 255)):
        super().__init__(groups)  # Initialisation de la classe parent
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))  # Rectangle représentant l'entité
        self.color = color  # Couleur de l'entité
        self.velocity_y = 0  # Vitesse verticale (utilisée pour la gravité)
        self.on_ground = False  # Savoir si l'entité touche le sol
        self.obs_groups = obs_groups
        self.direction = pygame.math.Vector2()  # Initialisation de l'attribut direction

        self.stats = {"hp": {"value": 10, "max_value": 100}}

    def apply_gravity(self):
        self.direction.y = GRAVITY * 4  # Déplace l'entité en fonction de la gravité

    def move(self):
        collision_type = []
        self.rect.x += self.direction.x * ENTITE_SPEED_MULTIPLICATOR
        collision_type += [self.collision("x")]
        self.rect.y += self.direction.y * ENTITE_SPEED_MULTIPLICATOR
        collision_type += [self.collision("y")]
        return collision_type

    def collision(self, direction):
        collision_type = None
        if direction == "x":
            for sprite in self.obs_groups:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                        collision_type = "droite"
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                        collision_type = "gauche"

        elif direction == 'y':
            for sprite in self.obs_groups:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                        collision_type = "bas"
                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                        collision_type = "haut"
        return collision_type

    def death(self):
        print("eni mort")

    def stats_update(self, nom_stats, value_update, max_value=None):
        if max_value is not None:
            self.stats[nom_stats]["max_value"] = max_value

        current_value = self.stats[nom_stats]["value"]
        max_value = self.stats[nom_stats]["max_value"]

        if value_update + current_value > max_value:
            if nom_stats == "hp":
                self.stats[nom_stats]["value"] = max_value

        elif value_update + current_value <= 0:
            if nom_stats == "hp":
                self.stats[nom_stats]["value"] = 0
                self.death()

            self.stats[nom_stats]["value"] += value_update
        return True

    def stats_set(self, nom_stats, value_update, max_update=None):
        if max_update:
            self.stats[nom_stats]["max"] = max_update
        if value_update:
            self.stats[nom_stats]["value"] = value_update
            print(self, self.stats[nom_stats]["value"])

    def attack(self, eni_groups, x, y, value, size=(TILE_SIZE, TILE_SIZE)):
        hitbox = CreateHitbox(x, y, size)
        for sprite in eni_groups:
            if hitbox.rect.colliderect(sprite):
                sprite.stats_update("hp", value)

class CreateHitbox(pygame.sprite.Sprite):
    def __init__(self, x, y, size=(TILE_SIZE, TILE_SIZE)):
        self.image = pygame.Surface(size)
        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft=(x, y))
