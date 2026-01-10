# Importa la biblioteca per a la programació de jocs
import pygame

# Importa: colors BLACK, GRAY, WHITE, PLAYER_COLOR; 
#         dimensions del tauler BSIZ, WIDTH, HEIGHT, SLOT, SEP, ROOM, RAD
from constants import *
pygame.font.init() #Inicia el sistema de textos de pygame per poder enunciar el guanyador

# Inicialització d'importació del tauler abstracte programat per separat:
from abs_board import set_board_up

# 1. DEMANAR LA MIDA A L'USUARI
try:
    str_input = input("Introdueix la mida del tauler (ex: 3, 4, 5...): ")
    BSIZ = int(str_input)
except ValueError:
    print("Valor incorrecte, s'usarà mida 3.")
    BSIZ = 3

print("Tria el mode (0: Clàssic, 1: Invers): ")
try:
    mode_input = input("Mode: ")
    GAME_MODE = int(mode_input)
except ValueError:
    print("Opció no vàlida. S'usarà el mode Clàssic (0).")
    GAME_MODE = 0

# 2. FER ELS CÀLCULS AQUÍ (Abans eren a constants.py)
HEIGHT = BSIZ * SLOT + (BSIZ + 1) * SEP + ROOM 
WIDTH = HEIGHT + ROOM
ST_PLAYER = (BSIZ**2 - 1) // 2  # Càlcul automàtic de fitxes

print(f"Jugarem amb un tauler de {BSIZ}x{BSIZ} i {ST_PLAYER} fitxes per jugador.")

# Inicialitza el motor del joc, indica un peu de foto i
# defineix l'alçada i l'amplada de la pantalla.
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("X en ratlla")
clock = pygame.time.Clock()

# Prepara el tauler:
stones, select_st, move_st, draw_txt = set_board_up(ST_PLAYER, BSIZ, GAME_MODE)

# Quadrícula:
def trans_coord(x, y):
    i = ((x - ROOM - SEP)//(SLOT + SEP)) # Tradueix el clic del ratolí a la columna de la matriu.
    j = ((y - SEP)//(SLOT + SEP)) # Tradueix el clic del ratolí a la fila de la matriu obtenint la casella exacta.
    if 0 <= i < BSIZ and 0 <= j < BSIZ:
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
    cx = int(ROOM + 0.5*SEP + (i + 0.5)*(SLOT + SEP))
    cy = int(0.5*SEP + (j + 0.5)*(SLOT + SEP))
    pygame.draw.circle(screen, color, (cx, cy), int(RAD))
    #Dibuixa les vores de les fitxes.
    pygame.draw.circle(screen, BLACK, (cx, cy), int(RAD), 2)

def draw_board(curr_player = 0, end = False):
    #en una pantalla nova, dibuixa una quadrícula, fitxes, la marca del torn del jugador i fes-la aparèixer.
    screen.fill(WHITE if not end else GRAY)
    for i in range(BSIZ):
        for j in range(BSIZ):
            draw_square(screen, i, j)
    for s in stones():
        draw_stone(screen, s.x, s.y, s.color)
    if not end:
        #el ractangle de color indica a qui li toca
        pygame.draw.rect(screen, PLAYER_COLOR[curr_player], 
        (ROOM + SEP, BSIZ*(SEP + SLOT) + SEP, BSIZ*(SEP + SLOT) - SEP, SLOT)
        )
        #Dibuixa les vores de l'indicador de torn
        pygame.draw.rect(screen, BLACK, 
            (ROOM + SEP, BSIZ*(SEP + SLOT) + SEP, BSIZ*(SEP + SLOT) - SEP, SLOT), 2
        )
    pygame.display.flip()

#Dibuixa com serà el missatge.
def dibuixa_missatge_guanyador(screen, curr_player):
    #Mida de la caixa, el retangle on hi haurà el missatge
    amplada_caixa = WIDTH - 40
    altura_caixa = 150
    #Calcula la posició per centrar-ho
    pos_x = 20
    pos_y = (HEIGHT - altura_caixa) // 2
    dimensions_rect = (pos_x, pos_y, amplada_caixa, altura_caixa)
    #Posa la mida de la lletra
    tipus_lletra = pygame.font.SysFont('Arial', 50)
    text_final = f"Victoria del Jugador {curr_player + 1}"
    
    imatge_text = tipus_lletra.render(text_final, True, WHITE)
    rect_text = imatge_text.get_rect()
    #Dibuixa fons i vora
    pygame.draw.rect(screen, BLACK, dimensions_rect)
    pygame.draw.rect(screen, WHITE, dimensions_rect, 2)
    #Centra el text a la pantalla
    rect_text.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(imatge_text, rect_text)
    
    pygame.display.flip()

# Inicialització de variables globals que faltaven
stone_selected = True
curr_player = 0

# Mostra la quadrícula i les pedres:
draw_board()


# Repetició fins que l'usuari fa clic al botó de tancament.
done = False

# Juga fins que acabi el joc
end = False

while not done:
    
    # Això limita el bucle while a un màxim de 10 vegades per segon.
    # Si ometem això, utilitzarem tota la CPU que puguem.
    clock.tick(10)
    
    for event in pygame.event.get(): 
        #l'usuari ha fet algo
        if event.type == pygame.QUIT:
         #El usuari ha fet clic a 'tancar finestra', ha establert la bandera per sortir del bucle.
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and not end:
            i,j = trans_coord(*event.pos)
            #El joc està en marxa i l'usuari ha fet clic a alguna cosa
            #Únicament mou o selecciona fitxa dins dels límits del tauler.
            if i != -1:
                #L'usuari ha de fer clic en una casella de destinació lliure; en cas contrari, ignora l'esdeveniment.
                if stone_selected:
                    stone_selected, curr_player, end = move_st(i,j)
                else:
                    stone_selected = select_st(i,j)
                
                draw_board(curr_player, end)

                if end:
                    dibuixa_missatge_guanyador(screen,curr_player)
            else:
                print("Per moure una fitxa has de clickar dins dels límits del tauler")

    #Actualitzem la pantalla amb .display.update().
    pygame.display.update()
# Final:
pygame.quit()
