"""
Autors: Ariel i Josep
Data: 2026
Descripció: Backend del joc (Lògica pura).
Gestiona el tauler, els moviments, la detecció de victòria i 
els diferents modes de joc (Clàssic i Invers).
"""

from constants import PLAYER_COLOR, NO_PLAYER, GRAY
from collections import namedtuple

Stone = namedtuple('Stone', ('x', 'y', 'color'))

def set_board_up(stones_per_player, size, game_mode=0):
    
    """
    Configura el tauler i l'estat inicial del joc.    
    Paràmetres: - stones_per_player, peces per jugador- size, mides - game_mode, classic o altrenatiu
    """

    BSIZ = size 

    # Creem el tauler, la qual es una matriu BSIZxBSIZ
    board = [[NO_PLAYER for _ in range(BSIZ)] for _ in range(BSIZ)]
    
    # Les variables canvien durant la partida per tant un diccionari q es mutable permet canviar-lo
    estat = {
        'current_player': 0,
        'selected': None,
        'stones_count': 0,
        'max_stones': stones_per_player * 2,
        'mode': game_mode 
    }

    def stones():
        """
        Llista amb totes les fitxes posades--->interfície gràfica.
        """
        stone_list = []
        for i in range(BSIZ):
            for j in range(BSIZ):
                if board[i][j] != NO_PLAYER:
                    # Si la casella no és buida, creem una 'Stone' del jugador
                    stone_list.append(Stone(i, j, PLAYER_COLOR[board[i][j]]))
        return stone_list

    def select_st(i, j):
        """
        Fase 2 ---> Retorna True si la selecció és vàlida, False si no ho és.
        """
        # 1. Coordenades dins del tauler i fitxa pertany al jugador q toca
        if 0 <= i < BSIZ and 0 <= j < BSIZ:
            if board[i][j] == estat['current_player']:
                estat['selected'] = (i, j)
                return True
        return False

    def end():

        """
        Logica per dir que s'acaba la partida
        Comprova Files, Columnes i les dues Diagonals.
        Retorna True si algú ha fet el tres en ratlla.
        """

        p = estat['current_player']
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

        # Si no s'ha complert cap condició.
        return False
    
    def check_winner_logic():
        """
        Mode de joc triat (Clàssic o Invers) tria qui guanya i qui perd .
        Retorna True si la partida s'ha d'acabar.
        """
        if end():
            if estat['mode'] == 1: # Mode Invers: Si fas línia, guanya l'altre
                estat['current_player'] = 1 - estat['current_player']
            return True
        return False

    def move_st(i, j):
        
        """
        Funció principal de moviment. Gestiona les dues fases del joc.
        """

        # Validar coordenades
        dins_del_tauler = (0 <= i < BSIZ) and (0 <= j < BSIZ)
        
        if not dins_del_tauler:  # Si esta fora, mantenim l'estat actual.
            estem_posant = estat['stones_count'] < estat['max_stones']
            tinc_fitxa_agafada = estat['selected'] is not None
            continua_fase = estem_posant or tinc_fitxa_agafada
            return continua_fase, estat['current_player'], False

        # fase1: posar
        if estat['stones_count'] < estat['max_stones']:
            
            # Si la casella està ocupada, ignorem
            if board[i][j] != NO_PLAYER:
                return True, estat['current_player'], False

            # Posem la fitxa
            board[i][j] = estat['current_player']
            estat['stones_count'] += 1

            # Mirem si ha guanyat (o perdut)
            game_over = check_winner_logic()
            if game_over:
                return True, estat['current_player'], True

            # Canviem torn
            estat['current_player'] = 1 - estat['current_player']
            
            # Si count < max, retornem True (seguim posant/demanant destí).
            # Si count == max, retornem False (sortim del bucle i demanarem Origen).
            seguim_posant = estat['stones_count'] < estat['max_stones']
            
            return seguim_posant, estat['current_player'], False

        # fase2: moure
        else:
            # Si no hi ha res seleccionat, no podem moure
            if estat['selected'] is None:
                return False, estat['current_player'], False

            # Si el destí està ocupat, ignorem
            if board[i][j] != NO_PLAYER:
                return True, estat['current_player'], False

            # Fem el moviment
            old_i, old_j = estat['selected']

            board[old_i][old_j] = NO_PLAYER
            board[i][j] = estat['current_player']
            estat['selected'] = None 

            # Mirem si ha guanyat
            game_over = check_winner_logic()
            if game_over:
                return False, estat['current_player'], True

            # Canviem torn
            estat['current_player'] = 1 - estat['current_player']
            return False, estat['current_player'], False

    def draw_txt(end_game=False):
        """
        Dibuixa l'estat actual del tauler a la terminal.
        """
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
                valor_casella = board[fila][columna] 

                # Traduïm el número (NO_PLAYER, 0, 1) al símbol (., X, O)
                dibuix = simbols[valor_casella]
                text_de_la_fila += dibuix + " "

            print(text_de_la_fila)

        # La partida s'ha acabat
        if end_game:
            guanyador_num = estat['current_player']
            guanyador_lletra = simbols[guanyador_num]
            print(f"JOC ACABAT! Guanyador: {guanyador_lletra}")
    
    # Retornem les funcions per poder usar-les des del main.
    return stones, select_st, move_st, draw_txt