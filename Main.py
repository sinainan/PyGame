import pygame as pg
import random
from Sprites import *
from Settings import *
from Platforms import *
from Spritesheets import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "sprites")
        with open(path.join(self.dir, HIGHSCORE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.spritesheet1 = Spritesheet1(path.join(img_dir, SPRITESHEET))
        self.spritesheet2 = Spritesheet2(path.join(img_dir, SPRITESHEET))
        self.spritesheet3 = Spritesheet3(path.join(img_dir, SPRITESHEET))

    def new(self):
        # Variables that are difind as txt
        self.score = 0
        self.musictxt = "On"
        self.mutxt = "Music:"
        # Music
        pg.mixer.music.load("Music/TLB.ogg")
        pg.mixer.music.play(-1)
        # Start new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.player = Player(self)
        # platforms
        for plat in PLATFROM_LIST:
            Platform(self, *plat)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right and \
                   self.player.pos.x > lowest.rect.left:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # When player reaches the top of the screen the screen will move up
        # will get 10 points for that
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(int(abs(self.player.vel.y)), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10


        # Spawning new platforms when the player reaches the top of the screen
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                     random.randrange(-75, -30))


        #powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                #self.boost_sound.play()
                self.player.vel.y = -POWER
                self.player.jumping = False

        # When player dies what to do
        # when player reaches the height of the screen.
        # if the platform reaches the bottom of the screen it will be removed
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(int(self.player.vel.y), 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False



    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_k:
                    pg.mixer.music.stop()
                    self.musictxt = "OFF"
                if event.key == pg.K_m:
                    pg.mixer.music.play(-1)
                    self.musictxt = "ON"
                if event.key == pg.K_ESCAPE:
                    self.show_start_screen()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(GOLD)
        self.screen.blit(BG, (0, 0))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, 20, 15)
        self.draw_text(str(self.musictxt), 22, WHITE, 442, 15)
        self.draw_text(str(self.mutxt), 22, WHITE, 400, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.blit(SC, (0, 0))
        pg.mixer.music.load("Music/TLB.ogg")
        pg.mixer.music.play(-1)
        self.draw_text("Highscore: " + str(self.highscore), 35, RED, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_time()

    def show_go_screen(self):
        # game over/continue
        self.screen.blit(GO, (0, 0))
        pg.mixer.music.load("Music/GO.ogg")
        pg.mixer.music.play(1)
        self.draw_text("Score: " + str(self.score), 35, RED, WIDTH / 2, 225)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!!", 35, RED, WIDTH / 2, 415)
            with open(path.join(self.dir, HIGHSCORE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 35, RED, WIDTH / 2, 415)
        pg.display.flip()
        self.go_time()

    def wait_time(self):
        wait = True
        while wait:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    wait = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        wait = False
                    if event.key == pg.K_k:
                        pg.mixer.music.stop()
                        self.musictxt = "OFF"
                    if event.key == pg.K_m:
                        pg.mixer.music.play(-1)
                        self.musictxt = "ON"
                    

    def go_time(self):
        wait = True
        while wait:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    wait = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        wait = False
                    if event.key == pg.K_ESCAPE:
                        self.show_start_screen()



    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (int(x), int(y))
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()