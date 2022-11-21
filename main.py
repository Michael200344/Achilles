import pygame
import os
# from camera import *
from player import Player
from enemy import Enemy
import random

pygame.init()

W, H = 1200, 600
GROUND_LEVEL = 480
win = pygame.display.set_mode((W, H))

bgOrig = pygame.image.load(os.path.join("Assets", "bg.png")).convert()
bg = pygame.transform.scale(bgOrig, (W, H))
bgx = bg.get_width()

pygame.display.set_caption("Practice with Character Movement")


#pygame.mixer.music.play(-1)
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.y = GROUND_LEVEL
        self.width = W
        self.height = H - GROUND_LEVEL
        self.rect = pygame.rect.Rect(0, GROUND_LEVEL, self.width, self.height)
    
player = Player(0, GROUND_LEVEL - 180) # 180 = player.height
ground = Ground()
en = Enemy(W - 200, GROUND_LEVEL - 180)
enemies = pygame.sprite.Group()
enemies.add(en)
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
    en.draw(win)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Health: ' + str(player.health), True, (0, 0, 0))
    textRect = text.get_rect()
    win.blit(text, textRect)
    pygame.display.flip()

def main(): # Main game loop
    FPS = 30
    clock = pygame.time.Clock()
    clock.tick(FPS)
    running = True
    while running:
        redrawWindow()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            
        keys_pressed = pygame.key.get_pressed()
        
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
        if not(en.dead):
            en.running = True
            en.move(0.22)
        if pygame.sprite.spritecollideany(player, enemies):
            if player.attacking:
                en.dead = True
                pass
            if not(en.dead):
                en.attacking = True
                player.health -= 1
                en.dead = True
            enemies.empty
        if player.health == 0:
            pygame.QUIT
main() # Run the program
    