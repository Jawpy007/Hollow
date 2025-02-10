# Paramètres du jeu
WIDTH, HEIGHT = 1280, 720 #Longueur
FPS = 60
GRAVITY = 1.8
TILE_SIZE=32

#ui main menu

PLAY_BUT_SIZE= {"x": 250, "y": 30}

#ui setup world
UI_FONT="Coding/graphics/font/times.ttf"
UI_FONT_SIZE=30

ITEM_BOX_SIZE=80

HEALTH_BAR_HEIGHT=20
HEALTH_BAR_WIDTH=200

XP_BAR_HEIGHT=20
XP_BAR_WIDTH=200

ENERGY_BAR_HEIGHT=20
ENERGY_BAR_WIDTH=200

#color setup

GREEN=(0,255,0)
BLUE=(0,0,255)
BLUEXP=(0,0,100)
YELLOW=(255,255,0)

#player
PLAYER_RUNNING_SPEED_MULTIPLICATOR=6
PLAYER_JUMP_MULTIPLICATOR  = 3
PLAYER_SPEED_MULTIPLICATOR = 5
WALL_JUMP_X_SPEED_MULTIPLICATOR=2
WALL_JUMP_COOLDOWN=200
JUMP_COOLDOWN=200
MAXJUMP=2
MAX_HEALTH=100

# Entite 
ENTITE_SPEED_MULTIPLICATOR=5

# Monstre


#Spectre


VOID_CHR=" "

#map setup
"""
Ci dessous la carte, voici la legende :

    - x -> un obstacle
    - p -> le joueur
    - ' ' -> Zone de deplacement du joueur
"""
WORLD_MAP = [
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['climp_wall_g','m',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x'],
['climp_wall_g',' ',' ',' ','climp_wall_r','x','x','x','x','x','x',' ','x','x',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ',' ',' ','climp_wall_r',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ',' ',' ','climp_wall_r',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ',' ',' ','climp_wall_r',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ',' ',' ','climp_wall_r',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ',' ',' ','climp_wall_r',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ',' ',' ','climp_wall_r',' ',' ','s',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ',' ',' ','climp_wall_r',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ',' ',' ','climp_wall_r',' ',' ',' ',' ',' ',' ',' ',' ','x','x','x',' ',' ',' ','x'],
['climp_wall_g',' ',' ',' ',' ',' ',' ','x','p','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ','x','x',' ',' ','x','x','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ',' ',' ',' ',' ',' ','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['climp_wall_g',' ','',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
['climp_wall_g',' ',' ',' ',' ','x','x','x',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' '],
['climp_wall_g',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x',' ',' ',' ',' '],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','n','x','x','x',' ',' '],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
]
