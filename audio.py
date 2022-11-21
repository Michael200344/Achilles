import pygame
import os

pygame.init()

bg_music = pygame.mixer.music.load(os.path.join("Assets", "Sounds", "music1.mp3"))
jump_land_sound = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "jumpland.wav"))
jump_sound = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "jump.wav"))
sword_whoosh_sound = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "sword_whoosh.mp3"))
running_sound = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "run.wav"))