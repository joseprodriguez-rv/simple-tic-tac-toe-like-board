from constants import PLAYER_COLOR, NO_PLAYER, GRAY
from collections import namedtuple

Stone = namedtuple('Stone', ('x', 'y', 'color'))

def set_board_up(stones_per_player, size, game_mode=0):
    
    BSIZ = size 

    # Creem el tauler
    board = [[NO_PLAYER for _ in range(BSIZ)] for _ in range(BSIZ)]
    
    state = {
        'current_player': 0,
        'selected': None,
        'stones_count': 0,
        'max_stones': stones_per_player * 2,
        'mode': game_mode 
    }

    def stones():
        stone_list = []
        for i in range(BSIZ):
            for j in range(BSIZ):
                if board[i][j] != NO_PLAYER:
                    stone_list.append(Stone(i, j, PLAYER_COLOR[board[i][j]]))
        return stone_list

    def select_st(i, j):
        if 0 <= i < BSIZ and 0 <= j < BSIZ:
            if board[i][j] == state['current_player']:
                state['selected'] = (i, j)
                return True
        return False

    def end():
        p = state['current_player']
        n = BSIZ

        # 1. FILES
        for i in range(n):
            comptador = 0 
            for j in range(n):
                if board[i][j] == p:
                    comptador += 1
            if comptador == n: return True

        # 2. COLUMNES
        for j in range(n):
            comptador = 0
            for i in range(n):
                if board[i][j] == p:
                    comptador += 1
            if comptador == n: return True

        # 3. DIAGONAL 1
        comptador = 0
        for i in range(n):
            if board[i][i] == p:
                comptador += 1
        if comptador == n: return True

        # 4. DIAGONAL 2
        comptador = 0
        for i in range(n):
            if board[i][n - 1 - i] == p:
                comptador += 1
        if comptador == n: return True

        return False
    
    def check_winner_logic():
        if end():
            if state['mode'] == 1: # Mode Invers: Si fas línia, guanya l'altre
                state['current_player'] = 1 - state['current_player']
            return True
        return False

    def move_st(i, j):
        # Validar coordenades
        dins_del_tauler = (0 <= i < BSIZ) and (0 <= j < BSIZ)
        
        if not dins_del_tauler:
            estem_posant = state['stones_count'] < state['max_stones']
            tinc_fitxa_agafada = state['selected'] is not None
            # Si fem click fora, mantenim l'estat actual
            keep_going = estem_posant or tinc_fitxa_agafada
            return keep_going, state['current_player'], False

        # --- FASE 1: POSAR FITXES ---
        if state['stones_count'] < state['max_stones']:
            
            # Si la casella està ocupada, ignorem
            if board[i][j] != NO_PLAYER:
                return True, state['current_player'], False

            # Posem la fitxa
            board[i][j] = state['current_player']
            state['stones_count'] += 1

            # Mirem si ha guanyat (o perdut)
            game_over = check_winner_logic()
            if game_over:
                return True, state['current_player'], True

            # Canviem torn
            state['current_player'] = 1 - state['current_player']
            
            # DECISIÓ CRÍTICA: Hem acabat de posar fitxes?
            # Si count < max, retornem True (seguim posant/demanant destí).
            # Si count == max, retornem False (sortim del bucle i demanarem Origen).
            seguim_posant = state['stones_count'] < state['max_stones']
            
            return seguim_posant, state['current_player'], False

        # --- FASE 2: MOURE FITXES ---
        else:
            # Si no hi ha res seleccionat, no podem moure
            if state['selected'] is None:
                return False, state['current_player'], False

            # Si el destí està ocupat, ignorem
            if board[i][j] != NO_PLAYER:
                return True, state['current_player'], False

            # Fem el moviment
            old_i, old_j = state['selected']

            board[old_i][old_j] = NO_PLAYER
            board[i][j] = state['current_player']
            state['selected'] = None 

            # Mirem si ha guanyat
            game_over = check_winner_logic()
            if game_over:
                return False, state['current_player'], True

            # Canviem torn
            state['current_player'] = 1 - state['current_player']
            return False, state['current_player'], False

    def draw_txt(end_game=False):
        print("\n--- TAULER ---")

        simbols = {NO_PLAYER: '.', 0: 'X', 1: 'O'}

        # Capçalera columnes
        text_capçalera = "  "  
        for columna in range(BSIZ):
            text_capçalera += str(columna) + " "
        print(text_capçalera)

        # Cos del tauler
        for fila in range(BSIZ):
            text_de_la_fila = str(fila) + " "
            for columna in range(BSIZ):
                
                # Primer la FILA, després la COLUMNA.
                # Això arregla que el tauler es vegi girat.
                valor_casella = board[fila][columna] 

                dibuix = simbols[valor_casella]
                text_de_la_fila += dibuix + " "

            print(text_de_la_fila)

        if end_game:
            guanyador_num = state['current_player']
            guanyador_lletra = simbols[guanyador_num]
            print(f"JOC ACABAT! Guanyador: {guanyador_lletra}")

    return stones, select_st, move_st, draw_txt