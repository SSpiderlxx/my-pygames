# Pygame template - skeleton for a new pygame project
import pygame
import random
import time
import os

WIDTH = 460
HEIGHT = 580
FPS = 30
score = 0

#define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
TEAL = (0,128,128)
YELLOW = (255,255,0)

game_folder = os.path.dirname(__file__)

class Mouse_Pos(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Play_Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = play_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, 200)
    def update(self):
        self.rect.x += 0

class Quit_Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = quit_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, 300)

    def update(self):
        self.rect.x += 0

        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, 540) 
        self.speedx = 0
        self.shoot_cooldown = 200
        self.last = pygame.time.get_ticks()
    def update(self):
        self.rect.x += self.speedx
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        now = pygame.time.get_ticks()
        if now - self.last >= self.shoot_cooldown:
            if keystate[pygame.K_SPACE]:
                self.last = now
                bullet = Bullet(self.rect.centerx, self.rect.top + - 30)
                all_sprites.add(bullet)
                all_bullets.add(bullet)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left  < 0:
            self.rect.left = 0
            
        

class Mobs(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img, (30, 30))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(-100, -40)
        self.rect.x = random.randrange(0, WIDTH)
        self.speedy = random.randrange(1, 8)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += 0
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Mob_Shooter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = shooter_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(-100, -40)
        self.rect.x = random.randrange(0, WIDTH)
        self.speedy = random.randrange(1, 8)
        self.shoot_cooldown = 3000
        self.last = pygame.time.get_ticks()
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += 0
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        now = pygame.time.get_ticks()
        if now - self.last >= self.shoot_cooldown:
            self.last = now
            mob_bullet = Mob_bullet(self.rect.centerx, self.rect.bottom + 30)
            all_sprites.add(mob_bullet)
            Mob_bullets.add(mob_bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 10))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        effect = pygame.mixer.Sound('lazershot.wav')
        effect.play()

        
    def update(self):
        self.rect.y += -10
        if self.rect.bottom < 0:
            self.kill()

class Mob_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 10))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        effect = pygame.mixer.Sound('lazershot.wav')
        effect.play()
    def update(self):
        self.rect.y += 10
        if self.rect.top > HEIGHT:
            self.kill()


#initialize pygame and create window
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("invasion")
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

#images

background_img = pygame.image.load(os.path.join(game_folder, "background.png")).convert()
background_rect = background_img.get_rect()
bullet_img = pygame.image.load(os.path.join(game_folder, "bullet.png")).convert()
mob_img = pygame.image.load(os.path.join(game_folder, "mob.png")).convert()
play_img = pygame.image.load(os.path.join(game_folder, "play.png")).convert()
player_img = pygame.image.load(os.path.join(game_folder, "player.png")).convert()
quit_img = pygame.image.load(os.path.join(game_folder, "quit.png")).convert()
shooter_img = pygame.image.load(os.path.join(game_folder, "shooter.png")).convert()

all_sprites = pygame.sprite.Group()
all_mobs = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
all_menu = pygame.sprite.Group()
mouse = pygame.sprite.Group()
Mob_bullets = pygame.sprite.Group()

play_button = Play_Button()
mouse_pos = Mouse_Pos()

quit_button = Quit_Button()

player = Player()

for i in range (4):
    mob = Mobs()
    all_sprites.add(mob)
    all_mobs.add(mob)

for i in range (2):
    shooter_mob = Mob_Shooter()
    all_sprites.add(shooter_mob)
    all_mobs.add(shooter_mob)
    
all_sprites.add(player)
all_sprites.add(mob)

all_menu.add(play_button)

all_menu.add(quit_button)

mouse.add(mouse_pos)
#menu loop
running = False
Menu = True
while Menu:
    # keep loop running at the right speed
    clock.tick(FPS)
    #Process inputs (events)
    for event in pygame.event.get():
        #check for closing the window
        if event.type == pygame.QUIT:
            Menu = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            hit = pygame.sprite.spritecollide(play_button, mouse, False)
            if hit:
                running = True
                Menu = False

            hit = pygame.sprite.spritecollide(quit_button, mouse, False)
            if hit:
                running = False
                Menu = False

            
    #update
    all_menu.update()
    mouse.update()

    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play(-1)
    
    #Draw / Render
    screen.fill(BLACK)
    screen.blit(background_img, background_rect)
    all_menu.draw(screen)
    title = myfont.render('INVASION', False, YELLOW)
    # *after* drawing everything, flip the display
    screen.blit(title, (WIDTH / 3, 100))
    pygame.display.flip()
    
#Game loop
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    #Process inputs (events)
    for event in pygame.event.get():
        #check for closing the window
        if event.type == pygame.QUIT:
            running = False
    hits = pygame.sprite.spritecollide(player, all_mobs, True)
    if hits:
        DEATH = myfont.render('YOUR DEAD', False, YELLOW)
        screen.blit(DEATH,(WIDTH / 3, 200))
        pygame.display.flip()
        time.sleep(5)
        running = False

     # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(all_mobs, all_bullets, True, True)
    if hits:
        m = Mobs()
        s_m = Mob_Shooter()
        all_sprites.add(m)
        all_mobs.add(m)
        all_sprites.add(s_m)
        all_mobs.add(s_m)
        score += 1
    #check to see if player has been hit from bullet
    hits = pygame.sprite.spritecollide(player, Mob_bullets, True)
    if hits:
        DEATH = myfont.render('YOUR DEAD', False, YELLOW)
        screen.blit(DEATH,(WIDTH / 3, 100))
        pygame.display.flip()
        time.sleep(5)
        running = False

    #update
    all_sprites.update()
    #Draw / Render
    screen.blit(background_img, background_rect)
    all_sprites.draw(screen)
    score_text = myfont.render('score:', False, YELLOW)
    score_number = myfont.render(str(score), False, YELLOW)
    screen.blit(score_text,(10,10))
    screen.blit(score_number,(100,10))
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
