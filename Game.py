# ====================
#   INITIALIZATION
# ====================

# import modules
import pygame, sys
from pygame.locals import *

import random
from Classes import *

# initialize filenames
bgfile = "bg.png"
feltfile = "felt.png"
deckfile = "deck.png"
deckbackfile = "deckback.png"

# initialize pygame
pygame.init()

# set up the screen params are resolution, flags(?), # of bits (color?)
screen = pygame.display.set_mode((400,200),0,32)

# loading images (...convert_alpha for images with transparancy)
bg = pygame.image.load(bgfile).convert()
felt = pygame.image.load(feltfile).convert()
deckback = pygame.image.load(deckbackfile).convert()

# initialize fonts
font = pygame.font.SysFont("monospace", 12)

# initialize colors
neongreen = (11, 232, 22)
mustard = (133, 133, 11)
darkred = (80, 0, 0)

# initialize deck spritesheet
decksheet = SpriteSheet(deckfile)

# initialize input handler
inputs = InputHandler()

# initialize game logic handler
logic = LogicHandler()

# initialize draw handler
draw = DrawHandler(felt, decksheet, deckback)

# initialize hands
shoe = Hand()
player = Hand()
dealer = Hand()
shoe.cards = logic.newdeck(8)

# ====================
#  END INITIALIZATION
# ====================


# ====================
#   MAIN GAME LOOP
# ====================

while True:
    
    # event checks (quit, key events)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            inputs.keydown(event.key)
        if event.type == KEYUP:
            inputs.keyup(event.key)
                
    # update logic
    logic.update(inputs, shoe, player, dealer)
    
    # draw to screen        
    draw.update(screen, font, logic, player, dealer)
            
    # display screen
    pygame.display.update()
    
# ====================
#    END GAME LOOP
# ====================