import pygame
from Settings import *
from Entity import *
from Weapons import *
from Inventory import *
from Graphics import import_folder

"""
Une classe Player qui hérite de Entite, avec ses propres mouvements et sauts.
"""

class Player(Entite):
    def __init__(self, x, y, groups, eni_groups, obs_groups, climp_zone, visible_groups, color=(255, 255, 255)):
        super().__init__(x, y, groups, obs_groups, color)  # Initialisation de la classe parente Entite

        # Variables graphiques de base du joueur
        self.player_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.player_layer = 1
        self.effect = None
        self.frame_index = 0
        self.animation_speed = 0.5

        # Variables de statut du joueur
        self.status = "right"
        self.attacking = False
        self.bowing = False
        self.attack_time = pygame.time.get_ticks()
        self.attack_side = ""

        # Groupes de sprites des ennemis du joueur
        self.eni_groups = eni_groups

        # Variables de statistiques
        self.inventory = inventory()
        self.player_xp_level = 1
        self.stats = {"mana": {"value": 10, "max_value": 100}, "xp": {"value": 0, "max_value": 100}, "hp": {"value": 100, "max_value": 100}}

        # Variables de mouvement
        self.direction = pygame.math.Vector2()

        # Mouvement horizontal
        self.dashing_last = [False, pygame.time.get_ticks()]
        self.dashing = False
        self.running = False

        # Mouvement vertical
        self.jump_count = MAXJUMP
        self.in_jump = False
        self.in_jump_time = pygame.time.get_ticks()

        # Variables pour le wall jump
        self.climp_zone = climp_zone
        self.walljump = None
        self.walljump_time = pygame.time.get_ticks()
        self.lastwalljump = None
        self.lastwalljump_cooldown = pygame.time.get_ticks()
        self.wall_jump_jump_left = False
        self.wall_jump_jump_left_cooldown = pygame.time.get_ticks()
        self.wall_jump_jump_right = False
        self.wall_jump_jump_right_cooldown = pygame.time.get_ticks()

        # Variables de détection de touches
        self.spacebar_key_block = False
        self.r_key_block = False
        self.K_d_doubletap = [pygame.time.get_ticks(), pygame.time.get_ticks()]
        self.K_q_doubletap = [pygame.time.get_ticks(), pygame.time.get_ticks()]

        self.import_player_assets()  # Chargement des assets graphiques du joueur

    def import_player_assets(self):
        chr_path = "Coding/graphics/player/"
        self.animations = {
            'left': [], 'right': [],
            'right_idle': [], 'left_idle': [],
            'right_attack': [], 'left_attack': [],
            'right_bow': [], 'left_bow': [],
            'right_dash': [], 'left_dash': []
        }
        for animation in self.animations.keys():
            full_path = chr_path + animation
            self.animations[animation] = import_folder(full_path)  # Importation des images d'animation

    def get_status(self):
        # Met à jour le statut du joueur en fonction de ses actions
        if self.direction.x == 0:
            if not "idle" in self.status and not "attack" in self.status and not "bow" in self.status:
                self.status = self.status + "_idle"

        if self.attacking and not self.dashing:
            if not self.bowing:
                if not "attack" in self.status:
                    if "idle" in self.status:
                        self.status = self.status.replace("_idle", "_attack")
                    else:
                        self.status = self.status + "_attack"
                    if "_bow" in self.status:
                        self.status = self.status.replace("_bow", "")
            else:
                if not "_bow" in self.status:
                    self.status = self.attack_side + "_bow"
                    if "attack" in self.status:
                        self.status = self.status.replace("_attack", "")
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")
            if "_bow" in self.status:
                self.status = self.status.replace("_bow", "")

        if self.dashing:
            if not "dash" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_dash")
                else:
                    self.status = self.status + "_dash"
        else:
            if "_dash" in self.status:
                self.status = self.status.replace("_dash", "")

    def input(self):
        # Gère les entrées clavier et souris pour contrôler le joueur
        self.direction = pygame.math.Vector2()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        cliquedroit = mouse[0]

        if (keys[pygame.K_q] and not self.walljump) or self.wall_jump_jump_left:
            self.status = "left"
            if self.current_time - self.K_q_doubletap[0] < 200 and self.current_time - self.K_q_doubletap[1] < 200 and not self.q_key_block and self.current_time - self.lastwalljump_cooldown > 700 and not self.wall_jump_jump_left:
                self.dashing = True
            self.direction.x += -1
            self.K_q_doubletap[0] = pygame.time.get_ticks() if not self.wall_jump_jump_left else self.K_q_doubletap[0]
            self.q_key_block = True if not self.wall_jump_jump_left else False

        if (keys[pygame.K_d] and not self.walljump) or self.wall_jump_jump_right:
            self.status = "right"
            if self.current_time - self.K_d_doubletap[0] < 200 and self.current_time - self.K_d_doubletap[1] < 200 and not self.d_key_block and self.current_time - self.lastwalljump_cooldown > 200 and not self.wall_jump_jump_right:
                self.dashing = True
            self.direction.x += 1
            self.K_d_doubletap[0] = pygame.time.get_ticks() if not self.wall_jump_jump_right else self.K_d_doubletap[0]
            self.d_key_block = True if not self.wall_jump_jump_right else False

        if keys[pygame.K_SPACE] and self.jump_count > 0 and not self.spacebar_key_block:
            if self.walljump == "droite":
                self.wall_jump_jump_left = True
                self.wall_jump_jump_left_cooldown = pygame.time.get_ticks()
            elif self.walljump == "gauche":
                self.wall_jump_jump_right = True
                self.wall_jump_jump_right_cooldown = pygame.time.get_ticks()
            self.in_jump = True
            self.jump_count -= 1
            self.in_jump_time = pygame.time.get_ticks()
            self.spacebar_key_block = True
            self.walljump = None

        if keys[pygame.K_LSHIFT]:
            self.running = True

        if keys[pygame.K_e]:
            if not self.attacking:
                if "sword" in self.inventory.items_dict.keys():
                    if "left" in self.status:
                        self.attack(self.eni_groups, self.rect.x - TILE_SIZE + 10, self.rect.y, -50, (TILE_SIZE + 10, TILE_SIZE))
                        self.attacking = True
                        self.attack_time = pygame.time.get_ticks()
                    elif "right" in self.status:
                        self.attack(self.eni_groups, self.rect.x + TILE_SIZE - 10, self.rect.y, -50, (TILE_SIZE + 10, TILE_SIZE))
                        self.attacking = True
                        self.attack_time = pygame.time.get_ticks()

        if keys[pygame.K_r]:
            if len(self.inventory.items_dict) > 0 and not self.r_key_block:
                self.inventory.items_dict["bow"].reload()
                self.r_key_block = True

        if cliquedroit:
            if not self.attacking:
                if "bow" in self.inventory.items_dict.keys():
                    self.bowing = True
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    self.attack_side = self.inventory.items_dict["bow"].use_weapons(self)
                    if self.attack_side < 0:
                        self.attack_side = "left"
                    else:
                        self.attack_side = "right"

        if not keys[pygame.K_d]:
            if self.current_time - self.K_d_doubletap[0] < 200:
                self.K_d_doubletap[1] = pygame.time.get_ticks()
            self.d_key_block = False

        if not keys[pygame.K_q]:
            if self.current_time - self.K_q_doubletap[0] < 200:
                self.K_q_doubletap[1] = pygame.time.get_ticks()
            self.q_key_block = False

        if not keys[pygame.K_r]:
            self.r_key_block = False

        if not keys[pygame.K_LSHIFT]:
            self.running = False

        if not keys[pygame.K_SPACE]:
            self.spacebar_key_block = False

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        x, y = self.rect.x, self.rect.y
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def collision_event(self):
        # Gère les événements de collision avec l'environnement
        keys = pygame.key.get_pressed()
        if "climp_gauche" in self.CollisionType and not self.walljump and (keys[pygame.K_q] or self.wall_jump_jump_left) and self.lastwalljump != "gauche":
            self.walljump = "gauche"
            self.walljump_time = pygame.time.get_ticks()
            self.lastwalljump_cooldown = pygame.time.get_ticks()
            self.jump_count = 1
            self.lastwalljump = "gauche"
            self.wall_jump_jump_right = False
            self.wall_jump_jump_left = False

        elif "climp_droite" in self.CollisionType and not self.walljump and (keys[pygame.K_d] or self.wall_jump_jump_right) and self.lastwalljump != "droite":
            self.walljump = "droite"
            self.walljump_time = pygame.time.get_ticks()
            self.lastwalljump_cooldown = pygame.time.get_ticks()
            self.jump_count = 1
            self.lastwalljump = "droite"
            self.wall_jump_jump_right = False
            self.wall_jump_jump_left = False

        elif (self.walljump == "gauche" and "climp_gauche" not in self.CollisionType) or (self.walljump == "droite" and "climp_droite" not in self.CollisionType):
            self.walljump = None

        elif "bas" in self.CollisionType:
            self.jump_count = MAXJUMP

    def move(self):
        # Gère les déplacements du joueur
        self.CollisionType = []
        self.collision("climp_zone")

        if self.dashing_last[0] and self.current_time - self.dashing_last[1] > 100:
            self.dashing_last[0] = False

        if self.walljump is None and not self.in_jump:
            if self.running:
                self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR / 2
                self.collision("x")

            if self.dashing:
                self.dashing = False
                x, y = self.rect.x, self.rect.y
                self.rect.topleft = (x, y)
                for i in range(20):
                    self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR
                    self.collision("x")
                self.dashing_last[0] = True
                self.dashing_last[1] = pygame.time.get_ticks()

            self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR
            self.collision("x")
            self.rect.y += self.direction.y * PLAYER_SPEED_MULTIPLICATOR
            self.collision("y")

        elif self.in_jump and self.walljump is None:
            if self.wall_jump_jump_right or self.wall_jump_jump_left:
                self.direction.x = self.direction.x * WALL_JUMP_X_SPEED_MULTIPLICATOR
            else:
                if self.dashing:
                    self.dashing = False
                    x, y = self.rect.x, self.rect.y
                    self.rect.topleft = (x, y)
                    for i in range(20):
                        self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR
                        self.collision("x")
                    self.dashing_last[0] = True
                    self.dashing_last[1] = pygame.time.get_ticks()
            self.rect.x += self.direction.x * PLAYER_SPEED_MULTIPLICATOR
            self.collision("x")
            for i in range(2):
                self.direction.y = -1
                self.rect.y += self.direction.y * PLAYER_JUMP_MULTIPLICATOR
                self.collision("y")

        elif self.walljump is not None:
            if self.walljump == "gauche":
                self.direction.x = -1
            else:
                self.direction.x = 1
            self.rect.x += self.direction.x
            self.collision("x")
            self.direction.y = 1
            self.rect.y += self.direction.y
            self.collision("y")

    def apply_gravity(self):
        # Applique la gravité au mouvement vertical du joueur
        if self.walljump is None:
            self.direction.y += GRAVITY

    def all_cooldown(self):
        # Gère les temps de recharge pour diverses actions
        if self.walljump and self.current_time - self.walljump_time > WALL_JUMP_COOLDOWN * 10:
            self.walljump = None
        if self.in_jump and self.current_time - self.in_jump_time > JUMP_COOLDOWN:
            self.in_jump = False
        if self.lastwalljump and self.current_time - self.lastwalljump_cooldown > JUMP_COOLDOWN * 10:
            self.lastwalljump = None
        if self.wall_jump_jump_left and self.current_time - self.wall_jump_jump_left_cooldown > JUMP_COOLDOWN * 2:
            self.wall_jump_jump_left = False
        if self.wall_jump_jump_right and self.current_time - self.wall_jump_jump_right_cooldown > JUMP_COOLDOWN * 2:
            self.wall_jump_jump_right = False
        if self.attacking and self.current_time - self.attack_time > JUMP_COOLDOWN:
            self.attacking = False
            self.bowing = False
            self.attack_side = ""

    def collision(self, Direction):
        # Détecte et réagit aux collisions avec les obstacles
        if Direction == "x":
            for sprite in self.obs_groups:
                if sprite.rect.colliderect(self.rect):
                    if sprite.name == "climp_wall_g":
                        if sprite.rect.centerx < self.rect.centerx:
                            self.rect.left = sprite.rect.right
                            self.CollisionType += ["climp_gauche", "gauche"]
                        else:
                            self.rect.right = sprite.rect.left
                            self.CollisionType += ["droite"]
                    elif sprite.name == "climp_wall_r":
                        if sprite.rect.centerx > self.rect.centerx:
                            self.rect.right = sprite.rect.left
                            self.CollisionType += ["climp_droite", "droite"]
                        else:
                            self.rect.left = sprite.rect.right
                            self.CollisionType += ["gauche"]
                    elif self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                        self.CollisionType += ["droite"]
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                        self.CollisionType += ["gauche"]
        elif Direction == 'y':
            for sprite in self.obs_groups:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.CollisionType += ["bas"]
                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.CollisionType += ["haut"]

    def player_level_up(self, value=1):
        # Gère la montée en niveau du joueur
        self.player_xp_level += value

    def stats_update(self, nom_stats, value_update, max_value=None):
        # Met à jour les statistiques du joueur
        if max_value is not None:
            self.stats[nom_stats]["max_value"] = max_value

        current_value = self.stats[nom_stats]["value"]
        max_value = self.stats[nom_stats]["max_value"]

        if value_update + current_value > max_value:
            if nom_stats == "hp":
                self.stats[nom_stats]["value"] = max_value
            elif nom_stats == "mana":
                self.stats[nom_stats]["value"] = max_value
            elif nom_stats == "xp":
                self.stats[nom_stats]["value"] = 0
                self.player_level_up()

        elif value_update + current_value <= 0:
            if nom_stats == "hp":
                self.stats[nom_stats]["value"] = 0
                self.death()
            elif nom_stats == "mana":
                return False
            elif nom_stats == "xp":
                reste = value_update + current_value
                self.stats[nom_stats]["value"] = max_value
                self.player_level_up(-1)
                self.stats_update("xp", reste)
        else:
            self.stats[nom_stats]["value"] += value_update
        return True

    def update(self):
        # Boucle principale du joueur
        self.current_time = pygame.time.get_ticks()
        self.input()
        self.apply_gravity()
        self.get_status()
        self.animate()
        self.move()
        self.collision_event()
        self.all_cooldown()
        self.inventory.update()
