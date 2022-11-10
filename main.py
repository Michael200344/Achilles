import pygame
import os
pygame.init()

W, H = 1200, 600
GROUND_LEVEL = 480
win = pygame.display.set_mode((W, H))

bgOrig = pygame.image.load("bg.png").convert()
bg = pygame.transform.scale(bgOrig, (W, H))
bgx = bg.get_width()

pygame.display.set_caption("Practice with Character Movement")

bg_music = pygame.mixer.music.load("music1.mp3")
#pygame.mixer.music.play(-1)

jump_land_sound = pygame.mixer.Sound("jumpland.wav")
jump_sound = pygame.mixer.Sound("jump.wav")
sword_whoosh_sound = pygame.mixer.Sound("sword_whoosh.mp3")
running_sound = pygame.mixer.Sound("run.wav")

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.y = GROUND_LEVEL
        self.width = W
        self.height = H - GROUND_LEVEL
        self.rect = pygame.rect.Rect(0, GROUND_LEVEL, self.width, self.height)

class Player(pygame.sprite.Sprite):
    run = [pygame.transform.scale(pygame.image.load(os.path.join('Walk', 'GreekBasic_Walk_' + str(x) + '.png')), 
    (200, 200)) for x in range(0,11)]
    idle = [pygame.transform.scale(pygame.image.load(os.path.join('Idle', 'GreekBasic_Idle_0' + str(x) + '.png')), 
    (160, 200)) for x in range(0,17)]
    attack = [pygame.transform.scale(pygame.image.load(os.path.join('Attack', 'GreekBasic_Attack_' + str(x) + '.png')), 
    (450, 210)) for x in range(0,7)]
    jump = [pygame.transform.scale(pygame.image.load(os.path.join('Jump', 'GreekBasic_Jump-Start_0' + str(x) + '.png')), 
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
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        self.jumping = False
        self.jumpCount = 0
        self.health = 10
    
    def draw(self, win):
        if self.attacking:
            if self.attackCount + 1 >= 140:
                pygame.mixer.Sound.play(sword_whoosh_sound)
                self.attackCount = 0
                self.attacking = False
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
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def gravity(self):
        if self.jumping:
            self.move(0, -(self.jumpCount**2) * .0000028)
    
player = Player(0, GROUND_LEVEL - 180) # 180 = player.height
ground = Ground()

def redrawWindow():
    win.blit(bg, (0,0))
    win.blit(bg, (bgx, 0))
    #pygame.draw.rect(win, (255, 0, 0), player.rect, 2) HITBOXES
    #pygame.draw.rect(win, (255, 0, 0), ground.rect, 2)
    player.draw(win)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Health: ' + str(player.health), True, (0, 0, 0))
    textRect = text.get_rect()
    win.blit(text, textRect)
    pygame.display.flip()

def main(): # Main game loop
    FPS = 60
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
main() # Run the program
    