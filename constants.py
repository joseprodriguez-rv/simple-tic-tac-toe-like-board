"""
Autors: Ariel i Josep
Data: 2024
Descripció: Fitxer de constants. Conté colors i mides fixes que no canvien
"""

# BSIZ (board side size) i ST_PLAYER (stones per player) s'ha passat al main per aixi puguin ser introduides, per tant deixen de ser constants

# Definim els colors que farem servir en format RGB
BLACK =   (  0,   0,   0)
GRAY =    (255, 255, 255) 
WHITE =   (45, 55, 70)
# Escollits perquè siguin amigables per a les persones daltòniques:
BLUISH =  (0, 255, 240)
REDDISH = (255, 0, 127)
PLAYER_COLOR = (BLUISH, REDDISH)

# Defineix l'amplada i l'alçada de la finestra del joc i la mida i separació de les ranures en píxels
SLOT = 125        # mida de les caselles
SEP = 25          # separació de les caselles
ROOM = SLOT + SEP # espai addicional als costats 


#ALÇADA (espai per a 3 quadrats amb marge i separadors interns i extra a sota) i AMPLADA (extra a banda i banda) també s'han passat al main

RAD = SLOT / 3                     # radi del cercle

NO_PLAYER = -1
