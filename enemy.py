import pygame
from audio import *
import os

GROUND_LEVEL = 480
W, H = 1200, 600

class Enemy(pygame.sprite.Sprite):
    run = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Animations", "Animations - Enemy", 'Walk', 'GreekBasic_Walk_0' + str(x) + '.png')), 
    (200, 200)) for x in range(0,11)]
    idle = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Animations", "Animations - Enemy", 'Idle', 'GreekBasic_Idle_0' + str(x) + '.png')), 
    (160, 200)) for x in range(0,17)]
    attack = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Animations", "Animations - Enemy", 'Attack', 'GreekBasic_Attack_' + str(x) + '.png')), 
    (450, 210)) for x in range(0,7)]
    death = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Animations", "Animations - Enemy", 'Die', 'GreekBasic_Die_0' + str(x) + '.png')), 
    (420, 270)) for x in range(0,9)]
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = 130
        self.height = 180
        self.runCount = 0
        self.running = True
        self.attackCount = 0
        self.attacking = False
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.dead = False
        self.deadCount = 0
    
    def draw(self, win):
        # if self.attacking:
        #     if self.attackCount + 1 >= 140:
        #         pygame.mixer.Sound.play(sword_whoosh_sound)
        #         self.attackCount = 0
        #         self.attacking = False
        #     win.blit(self.attack[self.attackCount//20], (self.x - 120, self.y - 10))
        #     self.attackCount += 1
        if self.dead:
            self.running = False
            if self.deadCount + 1 < 135:
                win.blit(self.death[self.deadCount//15], (self.x,self.y + 10))
                self.deadCount += 1
        elif self.running:
            if self.runCount + 1 >= 330:
                self.runCount = 0
            win.blit(self.run[self.runCount//30], (self.x,self.y))
            self.runCount += 1

    def move(self, val):
        self.x -= val
        self.rect = pygame.rect.Rect(self.x + 70, self.y, self.width, self.height)