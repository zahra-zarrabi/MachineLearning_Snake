import pygame

width=900
height=600
my_screen=pygame.display.set_mode((width,height))
bg = pygame.image.load('background.jpg')
pygame.mixer.init()
pygame.mixer.music.load("sound.wav")
pygame.mixer.music.play()
clock=pygame.time.Clock()
my_screen.fill((3,200,0))
pygame.display.set_caption('python game made by zahra ')
my_screen.blit(bg, (0, 0))