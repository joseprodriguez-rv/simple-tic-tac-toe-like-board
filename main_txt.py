"""
Autors: Ariel i Josep
Data: 2026
Descripció: Interfície de Text (Frontend).
Recull la configuració de l'usuari i executa el bucle principal del joc.
"""

from abs_board import set_board_up

# demanem les dades, si estan posadesmalament o no acceptades assumim un valor
# despres tmb es fan els calculs
  
try:
    str_input = input("Introdueix la mida del tauler (ex: 3, 4, 5...): ")
    BSIZ = int(str_input)
except ValueError:
    print("Valor incorrecte, s'usarà mida 3.")
    BSIZ = 3

print("\nMODES DE JOC:")
print("0: Clàssic (Fer 3 en ratlla GUANYA)")
print("1: Invers (Fer 3 en ratlla PERD)")
try:
    mode_input = input("Tria el mode (0 o 1): ")
    GAME_MODE = int(mode_input)
    if GAME_MODE not in [0, 1]: raise ValueError
except ValueError:
    print("Opció no vàlida. S'usarà el mode Clàssic (0).")
    GAME_MODE = 0


ST_PLAYER = (BSIZ**2 - 1) // 2 
#------------------------------

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

stones, select_st, move_st, draw_txt = set_board_up(ST_PLAYER, BSIZ, GAME_MODE)

# set_board_up() already selects a first stone
stone_selected = True 

# Loop until game ends
end = False
draw_txt(False)

print(f"Joc de tauler {BSIZ}x{BSIZ}. Mode: {'INVERS' if GAME_MODE == 1 else 'CLÀSSIC'}.")
print("Format: FILA COLUMNA (ex: 1 1)")

while not end:
    while not stone_selected and not end:
        try:
            inp = input("Selecciona fitxa origen (fila col): ")
            if not inp: continue
            i, j = inp.split()
            stone_selected = select_st(int(i), int(j))
            draw_txt(end)
        except ValueError:
            print("Error: Introdueix dos números valids.")

    while stone_selected and not end:
        try:
            inp = input("Selecciona destí (fila col): ")
            if not inp: continue
            i, j = inp.split()
            stone_selected, curr_player, end = move_st(int(i), int(j))
            draw_txt(end)
        except ValueError:
            print("Error: Introdueix dos números valids.")
    
    """
    Forma original:l'essencia es la mateixa pero ara ens salta un error.
    No te una gran gestio del error ja que nomes diu que tronis a posar, no informa els motius; possible millora.

    while not stone_selected:
        i, j = input("Select stone coordinates: ").split()
        stone_selected = select_st(int(i), int(j))
        draw_txt(end)
    while stone_selected and not end:
        i, j = input("Select destination coordinates: ").split()
        stone_selected, curr_player, end = move_st(int(i), int(j))
        draw_txt(end) 
    """    
    

# Wait for the user to look at the screen before ending the program.
input('\nGame over.')
