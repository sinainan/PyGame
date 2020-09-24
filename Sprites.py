# Sprite classes for platform game
import pygame as pg
from Settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.cur_frame = 0
        self.last_frame = 0
        self.loadimage()
        self.image = self.game.spritesheet.get_image(0, 84, 207, 372)
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 200) # Position of the player at the beginning
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def loadimage(self):
        self.lookl = self.game.spritesheet.get_image(0, 84, 207, 372)
        self.lookl.set_colorkey(BLACK)

        self.lookr = self.game.spritesheet.get_image(210, 84, 207, 372)
        self.lookr.set_colorkey(BLACK)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP


    def update(self):
        self.movelr()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC


        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def movelr(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_frame > 25:
                self.last_frame = now
                bottom = self.rect.bottom
                if self.vel.x > 0 :
                    self.image = self.lookr
                else:
                    self.image = self.lookl
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
