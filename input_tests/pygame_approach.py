import pygame, time
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Pygame Keyboard Test')
pygame.mouse.set_visible(0)


while True:
    for event in pygame.event.get():
        if (event.type == KEYDOWN):
            print (event.key)
            time.sleep(0.1)

'''
https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-python-from-the-terminal__
Pygame precisa de uma janela para receber os inputs, entao nao e uma boa opcao ao menos que queiramos fazer as coisas com GUI
'''
