import pygame
import os
# from camera import *
from player import Player
from enemy import Enemy
from audio import *
import random

pygame.init()

W, H = 1200, 600
GROUND_LEVEL = 480
win = pygame.display.set_mode((W, H))

menu_font = pygame.font.Font("\Windows\Fonts\papyrus.ttf", 100)
menu_f2 = pygame.font.Font("\Windows\Fonts\papyrus.ttf", 20)
menu_bg_orig = pygame.image.load(os.path.join("Assets", "menu_bg.jpg")).convert()
menu_bg = pygame.transform.scale(menu_bg_orig, (W, H))

bgOrig = pygame.image.load(os.path.join("Assets", "bg.png")).convert()
bg = pygame.transform.scale(bgOrig, (W, H))
bgx = bg.get_width()

pygame.display.set_caption("Practice with Character Movement")
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.y = GROUND_LEVEL
        self.width = W
        self.height = H - GROUND_LEVEL
        self.rect = pygame.rect.Rect(0, GROUND_LEVEL, self.width, self.height)
    
player = Player(0, GROUND_LEVEL - 180) # 180 = player.height
ground = Ground()
enemy = Enemy(W - 200, GROUND_LEVEL - 180)
enemies = pygame.sprite.Group()
enemies.add(enemy)
# camera = Camera(player)
# follow = Follow(camera, player)
# camera.setmethod(follow)

def redrawWindow():
    win.blit(bg, (0, 0))
    # Hitboxes Below!
    #pygame.draw.rect(win, (255, 0, 0), player.rect, 2)
    #pygame.draw.rect(win, (255, 0, 0), en, 2)
    #pygame.draw.rect(win, (255, 0, 0), ground.rect, 2)

    player.draw(win)
    for en in enemies:
        en.draw(win)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Health: ' + str(player.health), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (textRect.width - 70, textRect.height - 10)
    scoreText = font.render('Score: ' + str(player.score), True, (0, 0, 0), )
    scoreRect = scoreText.get_rect()
    scoreRect.center = (W - scoreRect.width + 50, scoreRect.height - 10)
    win.blit(text, textRect)
    win.blit(scoreText, scoreRect)
    pygame.display.flip()

def drawMenu():
    win.blit(menu_bg, (0, 0))
    menu_text = menu_font.render('ACHILLES',  True, (255, 255, 255))
    menu_rect = menu_text.get_rect()
    menu_rect.center = (W / 2, H / 2)
    win.blit(menu_text, menu_rect)
    
    t2 = menu_f2.render('BY: MICHAEL RHEINTGEN',  True, (255, 255, 255))
    t2_rect = t2.get_rect()
    t2_rect.center = (W / 2, H / 2 + 100)
    win.blit(t2, t2_rect)
    pygame.display.flip()

def checkColision(en):
    if pygame.sprite.collide_rect(en, player):
        if not(en.dead):
            if player.attacking:
                player.score += 1
            else:
                player.health -= 1
            en.dead = True
            return True

def main(): # Main game loop
    FPS = 60
    clock = pygame.time.Clock()
    clock.tick(FPS)
    running = True
    menu = True
    music_playing = False
    enemy_speed = 0.25
    while running:
        if menu:
            drawMenu()
            if not(music_playing):
                pygame.mixer.music.play(-1)
                music_playing = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN:
                menu = False
            
        keys_pressed = pygame.key.get_pressed()

        if not(menu):
            if pygame.time.get_ticks() % 1200 == 0 and enemy_speed < 1.3:
                enemy_speed += 0.05
            redrawWindow()
            if keys_pressed[pygame.K_SPACE]:
                if not(player.jumping):
                    player.attacking = True
            elif keys_pressed[pygame.K_LEFT]:
                player.move(-0.5, 0)
            elif keys_pressed[pygame.K_UP] and player.y == GROUND_LEVEL - 180:
                player.jumping = True
            elif keys_pressed[pygame.K_RIGHT]:
                if player.attacking or player.jumping:
                    player.running = False
                else:
                    player.running = True
                    player.move(0.5, 0)
            else:
                player.isIdle = True

            if not(player.dead):
                for en in enemies:
                    checkColision(en)
                    if en.deadCount > 130:
                        randDist = random.randint(0, 200)
                        enemies.add(Enemy(W + randDist, GROUND_LEVEL - 180))
                        en.kill()
                        break
                    elif not(en.dead):
                        en.move(enemy_speed)
            if player.health == 0:
                player.dead = True
                pygame.mixer.Sound.play(death_sound)
            if player.deadCount > 700:
                running = False
main() # Run the program
    