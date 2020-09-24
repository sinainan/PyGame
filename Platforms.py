import pygame as pg
from Sprites import *
from Settings import *
from random import choice, randrange
vec = pg.math.Vector2

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y,):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet1.get_image(0, 0, 560, 80),
                  self.game.spritesheet2.get_image(0, 924, 310, 44)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POWER_SPAWN:
            Powerup(self.game, self)

class Powerup(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(["boost"])
        self.image = self.game.spritesheet3.get_image(420, 63, 126, 127)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()