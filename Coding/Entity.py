import pygame
from Settings import *
from Player import *

# La classe Entite hérite de pygame.sprite.Sprite, ce qui signifie qu'elle peut être utilisée comme un sprite dans Pygame.
class Entite(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, obs_groups, surface=None, width=TILE_SIZE, height=TILE_SIZE, color=(255, 255, 255)):
        super().__init__(groups)  # Appel du constructeur de la classe parente pour initialiser le sprite
        self.image = pygame.Surface((width, height))  # Crée une surface (image) pour l'entité
        self.image.fill(color)  # Remplit la surface avec une couleur
        self.rect = self.image.get_rect(topleft=(x, y))  # Crée un rectangle représentant l'entité à la position (x, y)
        self.color = color  # Couleur de l'entité
        self.velocity_y = 0  # Vitesse verticale initiale
        self.on_ground = False  # Indique si l'entité est au sol
        self.obs_groups = obs_groups  # Groupes d'obstacles pour gérer les collisions
        self.direction = pygame.math.Vector2()  # Vecteur de direction pour les mouvements

        # Statistiques de l'entité, ici seulement les points de vie (hp)
        self.stats = {"hp": {"value": 100, "max_value": 100}}

        # Gestion des animations
        self.sprites = []  # Liste contenant toutes les images d'animation
        self.current_sprite = 0  # Indice de l'image actuellement utilisée

    def apply_gravity(self):
        # Applique la gravité à l'entité en modifiant sa vitesse verticale
        self.direction.y = GRAVITY * 4

    def move(self):
        # Déplace l'entité en fonction de sa direction et vérifie les collisions
        collision_type = []
        self.rect.x += self.direction.x * ENTITE_SPEED_MULTIPLICATOR  # Déplace horizontalement
        collision_type += [self.collision("x")]  # Vérifie les collisions horizontales
        self.rect.y += self.direction.y * ENTITE_SPEED_MULTIPLICATOR  # Déplace verticalement
        collision_type += [self.collision("y")]  # Vérifie les collisions verticales
        return collision_type

    def collision(self, direction):
        # Gère les collisions dans une direction donnée (x ou y)
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
        # Gère la mort de l'entité
        self.player.stats_update("xp", 10)  # Ajoute de l'expérience au joueur
        self.kill()  # Supprime l'entité

    def stats_update(self, nom_stats, value_update, max_value=None):
        print
        # Met à jour les statistiques de l'entité
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
        else:
            self.stats[nom_stats]["value"] += value_update

    def stats_set(self, nom_stats, value_update, max_update=None):
        # Définit les statistiques de l'entité à une valeur spécifique
        if max_update:
            self.stats[nom_stats]["max"] = max_update
        if value_update:
            self.stats[nom_stats]["value"] = value_update

    def attack(self, eni_groups, x, y, value, size=(TILE_SIZE, TILE_SIZE)):
        # Crée une hitbox pour l'attaque et vérifie les collisions avec les ennemis
        hitbox = CreateHitbox(x, y, size)
        for sprite in eni_groups:
            if hitbox.rect.colliderect(sprite):
                sprite.stats_update("hp", value)

class CreateHitbox(pygame.sprite.Sprite):
    def __init__(self, x, y, size=(TILE_SIZE, TILE_SIZE), groups_hit=None):
        if groups_hit is not None:
            super().__init__(groups_hit)  # Initialise la hitbox comme un sprite
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))  # Crée une surface pour la hitbox
        self.image.fill("blue")  # Remplit la surface avec une couleur bleue
        self.rect = self.image.get_rect(topleft=(x, y))  # Crée un rectangle pour la hitbox

"""
    def draw(self, screen):
        # Dessine l'entité sur l'écran (non utilisé ici)
        pygame.draw.rect(screen, self.color, self.rect)
"""
