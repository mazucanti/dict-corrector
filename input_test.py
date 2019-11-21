# Pygame approach
'''
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

https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-python-from-the-terminal__
Pygame precisa de uma janela para receber os inputs, entao nao e uma boa opcao ao menos que queiramos fazer as coisas com GUI
'''

# Readline approach

'''
import readline

class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None

completer = MyCompleter(["hello", "hi", "how are you", "goodbye", "great"])
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

input = input("Input: ")
print ("You entered", input)
'''

''' Couldn't get it working and honestly doesn't seems like the best idea
    Note: I found by searching "typing suggestions on python" on google
https://stackoverflow.com/questions/7821661/how-to-code-autocompletion-in-python '''

# Curses approach

import curses

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()

curses.endwin()


# Could be useful
# https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-python-from-the-terminal