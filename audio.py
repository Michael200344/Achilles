import pygame
import os

pygame.init()

menu_music = pygame.mixer.music.load(os.path.join("Assets", "Sounds", "menu_music.mp3"))
jump_land_sound = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "jumpland.wav"))
jump_sound = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "jump.wav"))
sword_whoosh_sound = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "sword_whoosh.mp3"))
running_sound = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "run.wav"))
death_sound = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "death_sound.mp3"))
enemy_death_sound = pygame.mixer.Sound(os.path.join("Assets", "Sounds", "enemy_death_sound.mp3"))