import pygame
from audio import *
import os

GROUND_LEVEL = 480
W, H = 1200, 600

class Player(pygame.sprite.Sprite):
    run = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Animations", 'Walk', 'GreekBasic_Walk_' + str(x) + '.png')), 
    (200, 200)) for x in range(0,11)]
    idle = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Animations", 'Idle', 'GreekBasic_Idle_0' + str(x) + '.png')), 
    (160, 200)) for x in range(0,17)]
    attack = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Animations", 'Attack', 'GreekBasic_Attack_' + str(x) + '.png')), 
    (450, 210)) for x in range(0,7)]
    jump = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Animations", 'Jump', 'GreekBasic_Jump-Start_0' + str(x) + '.png')), 
    (220, 240)) for x in range(0,18)]
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = 130
        self.height = 180
        self.runCount = 0
        self.running = False
        self.isIdle = True
        self.idleCount = 0
        self.attackCount = 0
        self.attacking = False
        self.rect = pygame.rect.Rect(self.x - 20, self.y, self.width, self.height)
        self.jumping = False
        self.jumpCount = 0
        self.health = 10

    def draw(self, win):
        if self.attacking:
            if self.attackCount > 80 and self.attackCount < 120:
                self.rect = pygame.rect.Rect(self.x, self.y, self.width + 50, self.height)
            if self.attackCount + 1 >= 140:
                pygame.mixer.Sound.play(sword_whoosh_sound)
                self.attackCount = 0
                self.attacking = False
                self.rect = pygame.rect.Rect(self.x - 20, self.y, self.width, self.height)
            win.blit(self.attack[self.attackCount//20], (self.x - 120, self.y - 10))
            self.attackCount += 1
        elif self.jumping:
            if self.jumpCount == 5:
                pygame.mixer.Sound.play(jump_sound)
            if self.jumpCount == 600:
                pygame.mixer.Sound.play(jump_land_sound)
            if self.jumpCount + 1 >= 630:
                self.jumpCount = 0
                self.jumping = False
            elif self.jumpCount + 1 >= 105 and self.jumpCount + 1 < 280:
                self.move(0, 19999/(self.jumpCount**2))
            elif self.jumpCount + 1 >= 315:
                self.gravity()
            win.blit(self.jump[self.jumpCount//35], (self.x - 28, self.y - 40))
            self.jumpCount += 1
        elif self.running:
            if self.runCount + 1 >= 220:
                self.runCount = 0
            win.blit(self.run[self.runCount//20], (self.x,self.y))
            self.runCount += 1
            #pygame.mixer.Sound.play(running_sound)
            self.running = False
        elif self.isIdle:
            if self.idleCount + 1 >= 680:
                self.idleCount = 0
            win.blit(self.idle[self.idleCount//40], (self.x,self.y))
            self.idleCount += 1

    def move(self, x, y):
        self.x += x
        self.y -= y
        if self.x <= 0:
            self.x = 0
        if self.x >= W - self.width:
            self.x = W - self.width
        # if self.y <= 0:
        #     self.y = 0
        if self.y >= GROUND_LEVEL - 180:
            self.y = GROUND_LEVEL - 180
        self.rect = pygame.rect.Rect(self.x - 20, self.y, self.width, self.height)

    def gravity(self):
        if self.jumping:
            self.move(0, -(self.jumpCount**2) * .0000028)