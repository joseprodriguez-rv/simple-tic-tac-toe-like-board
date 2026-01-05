"""
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Pygame-based handling of a simple tic-tac-toe-like board, 2021.
Intended for Grau en Intel-ligencia Artificial, Programacio i Algorismes 1.
"""

# Import library for game programming 
import pygame

# Import: colors BLACK, GRAY, WHITE, PLAYER_COLOR; 
#         board dimensions BSIZ, WIDTH, HEIGHT, SLOT, SEP, ROOM, RAD
from constants import *
pygame.font.init() #Iniciem el sistema de textos de pygame per poder enunciar el guanyador

# Initialize the game engine, indicate a caption and
# set the height and width of the screen.
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("A name here for your game")
clock = pygame.time.Clock()

# Import initialization of the separately programmed abstract board:
from abs_board import set_board_up

# Prepare board:
# this will set up all stones as unplayed, select a first stone to play,
# and obtain functions to handle them as follows:
#   the call stones() allows one to loop on all stones,
#   the call select_st(i, j) marks as selected the stone at these coordinates,
#   the call move_st(i, j) 
#     if the square at these coordinates is free, moves the selected  
#     stone there, changes player, unselects the stone and checks for 
#     end of game; otherwise, does nothing, leaving the stone selected;
#     returns: bool "stone still selected", next player (may be the same), 
#     and bool "end of game"
#   the call to draw_txt(end) prints a text-based version of the board
stones, select_st, move_st, draw_txt = set_board_up()

# Grid:
def trans_coord(x, y):
    i = ((x - ROOM - SEP)//(SLOT + SEP)) # Tradueix el clic del ratolí a la columna de la matriu.
	j = ((y - SEP)//(SLOT + SEP)) # Tradueix el clic del ratolí a la fila de la matriu obtenint la casella exacta.
if 0 <= i < BSIZ and BSIZ> j >= 0:
	return i,j
return -1,-1 # Si clica fora del tauler retorna -1.


def draw_square(screen, i, j):
    pygame.draw.polygon(screen, GRAY,
        ( (ROOM + SEP + i*(SLOT + SEP), SEP + j*(SLOT + SEP)),
          (ROOM + SEP + i*(SLOT + SEP) + SLOT, SEP + j*(SLOT + SEP)),
          (ROOM + SEP + i*(SLOT + SEP) + SLOT, SEP + j*(SLOT + SEP) + SLOT),
          (ROOM + SEP + i*(SLOT + SEP), SEP + j*(SLOT + SEP) + SLOT)
        )) 
#Dibuixa les vores de les caselles.
    pygame.draw.polygon(screen, BLACK,
		( (ROOM + SEP + i*(SLOT + SEP), SEP + j*(SLOT + SEP)),
		  (ROOM + SEP + i*(SLOT + SEP) + SLOT, SEP + j*(SLOT + SEP)),
		  (ROOM + SEP + i*(SLOT + SEP) + SLOT, SEP + j*(SLOT + SEP) + SLOT),
		  (ROOM + SEP + i*(SLOT + SEP), SEP + j*(SLOT + SEP) + SLOT)
		), 2)
def draw_stone(screen, i, j, color):
    pygame.draw.circle(screen, color, 
        (ROOM + 0.5*SEP + (i + 0.5)*(SLOT + SEP), 0.5*SEP + (j + 0.5)*(SLOT + SEP)), 
        RAD)
#Dibuixa les vores de les fitxes.
    pygame.draw.circle(screen, BLACK, 
		(ROOM + 0.5*SEP + (i + 0.5)*(SLOT + SEP), 0.5*SEP + (j + 0.5)*(SLOT + SEP)), 
		RAD, 2)
def draw_board(curr_player = 0, end = False):
    'on fresh screen, draw grid, stones, player turn mark, then make it appear'
    screen.fill(WHITE if not end else GRAY)
    for i in range(BSIZ):
        for j in range(BSIZ):
            draw_square(screen, i, j)
    for s in stones():
        draw_stone(screen, *s)
    if not end:
        'colored rectangle indicates who plays next'
        pygame.draw.rect(screen, PLAYER_COLOR[curr_player], 
        (ROOM + SEP, BSIZ*(SEP + SLOT) + SEP, BSIZ*(SEP + SLOT) - SEP, SLOT)
        )
#Dibuixa les vores de l'indicador de torn
        pygame.draw.rect(screen, BLACK, 
            (ROOM + SEP, BSIZ*(SEP + SLOT) + SEP, BSIZ*(SEP + SLOT) - SEP, SLOT), 2
        )
    pygame.display.flip()
#Dibuixa com serà el missatge.
def dibuixa_missatge_guanyador(screen,curr_player):
	#Escull tipus de lletra i forma el missatge (.render() crea una imatge del text i la suavitza).
	tipus_lletra = pygame.font.SysFont('Arial',40)
	text_final = f"Victoria del Jugador {curr_player}"
   	missatge = tipus_lletra.render(text_final, True, BLACK)
    #Creem un fons
   	amplada_fons, altura_fons = 400, 100
    #Centrem el fons a la pantalla.
   	fons = pygame.Rect(0, 0, amplada_fons, altura_fons)
   	fons.center = (WIDTH // 2, HEIGHT // 2) 
    
    #Centrem també el missatge.
    text = missatge.get_rect(center=fons.center)
    
    #Dibuixa primer el fons blanc i després el text a sobre.
    pygame.draw.rect(screen, WHITE, fons)
   	pygame.draw.rect(screen, BLACK, fons, 3) #Afegeix una vora.
    screen.blit(missatge, text)

# set_board_up() already selects a first stone; set curr_player to zero.
stone_selected = True
curr_player = 0

# Show grid and stones:
draw_board()

# Loop until the user clicks the close button.
done = False

# Play until game ends
end = False

while not done:
    
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)
    
    for event in pygame.event.get(): 
        "User did something"
        if event.type == pygame.QUIT:
            "User clicked 'close window', set flag to exit loop"
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and not end:
				i,j = trans_coord(*event.pos)
			 "game is afoot and user clicked something"
				#Únicament mou o selecciona fitxa dins dels límits del tauler.
				if i != -1:
					"User should click on a free destination square, otherwise ignore event"
					if stone_selected:
                		stone_selected, curr_player, end = move_st(i,j)
					else:
						stone_selected = select_st(i,j)
				else:
					print("Per moure una fitxa has de clickar dins dels límits del tauler")
	#Afegim screen i stones per poder dibuixar a sobre i dibuixem el missatge guanyador, definit prèviament, al finalitzar la partida.
	draw_board(screen,stones,curr_player, end)
	if end:
		dibuixa_missatge_guanyador(screen,curr_player)
	#Actualitzem la pantalla amb .display.update().
	pygame.display.update()
# Friendly finish-up:
pygame.quit()
