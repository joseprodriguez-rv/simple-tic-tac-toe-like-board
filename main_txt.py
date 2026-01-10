
from abs_board import set_board_up

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

stones, select_st, move_st, draw_txt = set_board_up(ST_PLAYER, BSIZ, GAME_MODE)

stone_selected = True 

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
            print("Error: Introdueix dos números.")

    while stone_selected and not end:
        try:
            inp = input("Selecciona destí (fila col): ")
            if not inp: continue
            i, j = inp.split()
            stone_selected, curr_player, end = move_st(int(i), int(j))
            draw_txt(end)
        except ValueError:
            print("Error: Introdueix dos números.")

input('\nGame over.')