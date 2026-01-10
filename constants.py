
# BSIZ (board side size) i ST_PLAYER (stones per player) s'ha passat al main per aixi puguin ser introduides, per tant deixen de ser constants

# Define the colors we will use in RGB format
BLACK =   (  0,   0,   0)
GRAY =    (255, 255, 255) 
WHITE =   (45, 55, 70)
# Chosen so that they are still friendly to colorblind people:
BLUISH =  (0, 255, 240)
REDDISH = (255, 0, 127)
PLAYER_COLOR = (BLUISH, REDDISH)

# Define the game window width and height and the slot size and separation in pixels
SLOT = 125        # squares size
SEP = 25          # squares separation
ROOM = SLOT + SEP # extra room at sides 

#HEIGHT (room for 3 squares with margin and internal separators and extra below) i WIDTH (extra at both sides) tambe s'han passat al main

RAD = SLOT / 3                     # circle radius

NO_PLAYER = -1