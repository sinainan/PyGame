import pygame as pg

# Settings of the game and the options
TITLE = "Jumping Marly"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HIGHSCORE = 'score.txt'
SPRITESHEET = "sprite.png"

# Background image AS BG , Startscreen Image AS SC, Gameover Image AS GO
BG = pg.image.load("Images/marley.png")
SC = pg.image.load("Images/SC.png")
GO = pg.image.load("Images/GO.png")

# Player properties ( acceleration, Friction, Gravity, Jump )
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

#powerup properties
POWER = 50
POWER_SPAWN = 7

# List for platforms
PLATFROM_LIST = [(0, HEIGHT - 20), # base Platform
                 (100, 400), # bottom Platform
                 (312, HEIGHT - 350), # Mid/Bot Platform
                 (122, 200), # Mid/Top platform
                 (300, 100)] # top platform

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255,215,0)










