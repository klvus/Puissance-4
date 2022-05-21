from audioop import minmax
from operator import truediv
import numpy as np
import random as rand
import time
import math as math

RANGEE = 6
COLONNES = 7
PIECE_1 = 1
PIECE_2 = 2
INFINI = math.inf


# Crée un tableau de taille ROWSxCOLONNES initialisé par des 0
def create_board():
    board = np.zeros((RANGEE, COLONNES))
    return board


# Place une piece dans une coordonnée du tableau
def insererPiece(board, row, colonne, piece):
    board[row][colonne] = piece


# Test la disponibilite d'une coordonnee(rangée, colonne) du tableau
def isDisponible(board, colonne):
    return board[RANGEE-1][colonne] == 0


# Retourne une liste des rangés disponibles
def getColonnesDisponibles(board):
    listeDisponibilite = []
    for colonne in range(COLONNES):
        if(isDisponible(board, colonne) == True):
            listeDisponibilite.append(colonne)

    return listeDisponibilite


# Verifie si le plateau est plein
def isBoardFull(board):
    boolean = True
    for i in range(COLONNES):
        boolean = isDisponible(board, i)
    return boolean


# Verifie si le plateau est vide
def isBoardEmpty(board):
    boolean = True
    for i in range(COLONNES):
        if(board[0, i] != 0):
            boolean = False
    return boolean


# Retourne la range disponible pour une colonne donnee
def getNextOpenRow(board, colonne):
    for r in range(RANGEE):
        if board[r][colonne] == 0:
            return r


# Renverse le tableau pour meilleur illustration du jeux
def printBoard(board):
    print(np.flip(board, 0))


# Test l'ensemble des positionnements gagnant pour une piece(joueur) donne
def winning_moves(board, piece):
    # Horizontal
    for c in range(COLONNES-3):
        for r in range(RANGEE):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Vertical
    for c in range(COLONNES):
        for r in range(RANGEE-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Diagonal upwords
    for c in range(COLONNES-3):
        for r in range(RANGEE-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Diagonal downwords
    for c in range(COLONNES-3):
        for r in range(3, RANGEE):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False


# Système d'évaluation d'espaces de 4 pièces appellés "tranche"
def evalCombinaison(tranche, piece):
    # initialisation de la variable retourné "valeur"
    valeur = 0

    # initialisation piece_ennemis
    if(piece == 1):
        piece_ennemis = 2
    elif(piece == 2):
        piece_ennemis = 1

    # use case: puissance 4
    if (tranche.count(piece) == 4):
        valeur += 1000
    # use case: puissance 3 avec 1 case vide
    if(tranche.count(piece) == 3 and tranche.count(0) == 1):
        valeur += 80
    # use case: puissance 2 avec 2 case vides
    if(tranche.count(piece) == 2 and tranche.count(0) == 2):
        valeur += 8
    # use case: puissance 4 potentiel pour le joueur adverse
    if(tranche.count(piece_ennemis) == 3 and tranche.count(0) == 1):
        valeur -= 1000

    return valeur


# Retourne True si la situation de jeu est "terminal"
def is_terminal(board):
    return (winning_moves(board, PIECE_1) or winning_moves(board, PIECE_2) and isBoardFull(board))


# Algorithme minimax sans optimization alpha beta
def minimax(board, depth, maximizingPlayer):  # utilisation du pseudo code wikipedia
    terminal_status = is_terminal(board)
    colonnesDisponibles = getColonnesDisponibles(board)
    if(depth == 0 or terminal_status):
        if(terminal_status):
            if(winning_moves(board, PIECE_1)):  # l'IA à gagné
                return 100000000, None
            if(winning_moves(board, PIECE_2)):  # Le joueur humain adversaire à gagné
                return -10000000, None
            else:  # Le jeux est fini sans gagnant car tableau rempli
                return 0, None

        else:
            return valeurDecision(board, PIECE_1), None

    if(maximizingPlayer):
        colonneDecision = rand.choice(colonnesDisponibles)
        valeur = -INFINI
        for colonne in colonnesDisponibles:
            temporary_board = board.copy()
            rangee = getNextOpenRow(temporary_board, colonne)
            # simulation du coup pour la colonne donnée
            insererPiece(temporary_board, rangee, colonne, PIECE_1)
            nouvelle_valeur = minimax(
                temporary_board, depth-1, False)[0]  # car minimax retourne un tuple
            if(nouvelle_valeur > valeur):
                valeur = nouvelle_valeur
                colonneDecision = colonne
        return valeur, colonneDecision

    else:
        colonneDecision = rand.choice(colonnesDisponibles)
        valeur = INFINI
        for colonne in colonnesDisponibles:
            temporary_board = board.copy()
            rangee = getNextOpenRow(temporary_board, colonne)
            insererPiece(temporary_board, rangee, colonne, PIECE_2)
            nouvelle_valeur = minimax(
                temporary_board, depth-1, True)[0]  # car minimax retourne un tuple
            if(nouvelle_valeur < valeur):
                valeur = nouvelle_valeur
                colonneDecision = colonne
        return valeur, colonneDecision


# utilisation du pseudo code wikipedia avec implementation alpha beta
def minimaxAlphaBeta(board, depth, alpha, beta, maximizingPlayer):

    # (boolean) stock l'état (terminal ou non) du jeu courant
    terminal_status = is_terminal(board)

    # (int []) stock les colonnes disponibles
    colonnesDisponibles = getColonnesDisponibles(board)

    if(depth == 0 or terminal_status):
        if(terminal_status):
            if(winning_moves(board, PIECE_1)):  # l'IA à gagné
                return 100000000, None
            if(winning_moves(board, PIECE_2)):  # Le joueur humain adversaire à gagné
                return -10000000, None
            else:  # Le jeux est fini sans gagnant car tableau rempli
                return 0, None

        else:
            # le retour est un tuple: (valeur, colonne)
            return valeurDecision(board, PIECE_1), None

    if(maximizingPlayer):
        colonneDecision = rand.choice(colonnesDisponibles)
        valeur = -INFINI
        for colonne in colonnesDisponibles:
            temporary_board = board.copy()
            rangee = getNextOpenRow(temporary_board, colonne)
            insererPiece(temporary_board, rangee, colonne, PIECE_1)
            nouvelle_valeur = minimax(temporary_board, depth-1, False)[0]
            if(nouvelle_valeur > valeur):
                valeur = nouvelle_valeur
                colonneDecision = colonne
            alpha = max(valeur, alpha)
            if alpha >= beta:
                break
        # le retour est un tuple: (valeur, colonne)
        return valeur, colonneDecision

    else:
        colonneDecision = rand.choice(colonnesDisponibles)
        valeur = INFINI
        for colonne in colonnesDisponibles:
            temporary_board = board.copy()
            rangee = getNextOpenRow(temporary_board, colonne)
            insererPiece(temporary_board, rangee, colonne, PIECE_2)
            nouvelle_valeur = minimax(temporary_board, depth-1, True)[0]
            if(nouvelle_valeur < valeur):
                valeur = nouvelle_valeur
                colonneDecision = colonne
            beta = min(valeur, beta)
            if alpha < beta:
                break
        # le retour est un tuple: (valeur, colonne)
        return valeur, colonneDecision


# Donne une valeur plus ou moins grande, dependant des placements avantageux des pieces placées
def valeurDecision(board, piece):

    valeur = 0
    
    # preferer les cases au centre du tableau
    center_array = [int(j) for j in list(board[:, COLONNES//2])]
    center_count = center_array.count(piece)
    valeur += center_count * 2

    # Horizontal
    for i in range(RANGEE):

        # Get les rangés du tableau de jeux dans un array plus facile de manipuler
        row_array = [int(j) for j in list(board[i, :])]
        for colonne in range(COLONNES-3):
            tranche = row_array[colonne:colonne+4]  # De row[0] à row[4]
            valeur += evalCombinaison(tranche, piece)

    # Vertical
    for i in range(COLONNES):

        col_array = [int(j) for j in list(board[:, i])]
        for rangE in range(RANGEE-3):
            tranche = col_array[rangE:rangE+4]
            valeur += evalCombinaison(tranche, piece)

    # Diagonal upwords
    for colonne in range(COLONNES-3):
        for rangE in range(RANGEE-3):
            diag_array = [board[rangE+i, colonne+i] for i in range(4)]
        valeur += evalCombinaison(diag_array, piece)

    # Diagonal downwords
    for colonne in range(COLONNES-3):
        for rangE in range(RANGEE-3):
            diag_array = [board[rangE+3-i, colonne+i] for i in range(4)]
        valeur += evalCombinaison(diag_array, piece)

    return valeur


# "IA" qui utilise le systeme de valeur pour faire ces decisions
def mediumAI(board, piece):
    colonnesDisponibles = getColonnesDisponibles(board)
    valeurMax = 0
    colonneDecision = rand.choice(colonnesDisponibles)
    for colonne in colonnesDisponibles:
        temporary_board = board.copy()
        rangee = getNextOpenRow(temporary_board, colonne)
        insererPiece(temporary_board, rangee, colonne, piece)
        valeur = valeurDecision(temporary_board, piece)
        if(valeur > valeurMax):
            valeurMax = valeur
            colonneDecision = colonne

    return colonneDecision


# Une IA faisant des choix aleatoires
def randomAI(board, piece):
    r = rand.randrange(0, COLONNES-1)
    if(isDisponible(board, r)):
        return r


mode = int(input("1: .vs AI(random)\n2: .vs AI(medium)\n3: .vs Joueur2\n4: .vs MiniMax"))
board = create_board()
game_over = False
turn = rand.randrange(0, 1)

if(mode == 4):
    depth = int(input("1: Easy\n3: Medium\n5: Hard\n"))

print("BEGIN\n")
printBoard(board)
while not game_over:

    # Mode de Jeux: .vs AI(random)
    while(mode == 1):

        # Input AI random
        if turn == 1 and mode == 1:
            colonne = randomAI(board, 2)
            row = getNextOpenRow(board, colonne)
            insererPiece(board, row, colonne, 2)
            print("\nAI à joué\n")
            time.sleep(0.2)  # Sleep for 0.2 seconds
            printBoard(board)
            if winning_moves(board, 2):
                print("AI WINS !!")
                game_over = True
                mode = 0
            turn += 1
            turn = turn % 2

        # Demande Input de l'HUMAIN
        if turn == 0 and mode == 1:
            colonne = int(input("Joueur 2 Selectionnez(0-6): "))
            if isDisponible(board, colonne):
                row = getNextOpenRow(board, colonne)
                insererPiece(board, row, colonne, 1)
                if winning_moves(board, 1):
                    print("YOU WIN !!")
                    game_over = True
                    mode = 0
                turn += 1
                turn = turn % 2
            else:
                print("L'espace n'est pas disponible !")
            printBoard(board)

    # Mode de jeux .vs AI(medium)
    while(mode == 2):

        # Input AI 1 tour
        if turn == 1 and mode == 2:
            colonne = mediumAI(board, 1)
            row = getNextOpenRow(board, colonne)
            insererPiece(board, row, colonne, 1)
            time.sleep(0.2)  # Sleep for 0.2 seconds
            printBoard(board)
            print("\nAI à joué\n")
            if winning_moves(board, 1):
                print("AI WINS !!")
                game_over = True
                mode = 0
            turn += 1
            turn = turn % 2

        # Demande Input de l'HUMAIN
        if turn == 0 and mode == 2:
            colonne = int(input("Joueur 2 Selectionnez(0-6): "))
            if isDisponible(board, colonne):
                row = getNextOpenRow(board, colonne)
                insererPiece(board, row, colonne, 2)
                if winning_moves(board, 2):
                    print("YOU WIN !!")
                    game_over = True
                    mode = 0
                turn += 1
                turn = turn % 2
            else:
                print("L'espace n'est pas disponible !")
            printBoard(board)

    # Mode de jeux .vs AI(minimax)
    while(mode == 4):

        # Input AI 1 tour
        if turn == 1 and mode == 4:
            valeurMinimax, colonne = minimaxAlphaBeta(
                board, depth, -INFINI, INFINI, True)
            row = getNextOpenRow(board, colonne)
            insererPiece(board, row, colonne, 1)
            time.sleep(0.2)  # Sleep for 0.2 seconds
            printBoard(board)
            print("\nAI à joué\n")
            if winning_moves(board, 1):
                print("AI WINS !!")
                game_over = True
                mode = 0
            turn += 1
            turn = turn % 2

        # Demande Input de l'HUMAIN
        if turn == 0 and mode == 4:
            colonne = int(input("Joueur 2 Selectionnez(0-6): "))
            if isDisponible(board, colonne):
                row = getNextOpenRow(board, colonne)
                insererPiece(board, row, colonne, 2)
                if winning_moves(board, 2):
                    print("YOU WIN !!")
                    game_over = True
                    mode = 0
                turn += 1
                turn = turn % 2
            else:
                print("L'espace n'est pas disponible !")
            printBoard(board)

    # Mode de jeux: .vs Joueur2
    while(mode == 3):
        # Demander Input de Joueur 1
        if turn == 0:
            colonne = int(input("Joueur 1 Selectionnez (0-6): "))
            if isDisponible(board, colonne):
                row = getNextOpenRow(board, colonne)
                insererPiece(board, row, colonne, 1)

                if winning_moves(board, 1):
                    print("PLAYER 1 WINS !!")
                    game_over = True
                    mode = 0
                turn += 1
                turn = turn % 2
            else:
                print("L'espace n'est pas disponible !")

        # Demander Input de Joueur 2
        else:
            colonne = int(input("Joueur 2 Selectionnez(0-6): "))
            if isDisponible(board, colonne):
                row = getNextOpenRow(board, colonne)
                insererPiece(board, row, colonne, 2)

                if winning_moves(board, 2):
                    print("PLAYER 2 WINS !!")
                    game_over = True
                    mode = 0
                turn += 1
                turn = turn % 2
            else:
                print("L'espace n'est pas disponible !")

        printBoard(board)
