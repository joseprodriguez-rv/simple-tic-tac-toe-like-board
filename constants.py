
BSIZ = 4 # board side size

ST_PLAYER = 4 # stones per player

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
HEIGHT = BSIZ * SLOT + (BSIZ + 1) * SEP + ROOM # room for 3 squares with margin and internal separators and extra below
WIDTH = HEIGHT + ROOM              # extra at both sides
RAD = SLOT / 3                     # circle radius

NO_PLAYER = -1
