# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:40:28 2021

@author: jlucas
"""

import random
import time

# schéma initial de la grille avec placement des personnages
SCHEMA_GRILLE = """
#########################
#.......................#
#.@#..#...#####...#..#@.#
####..##.........##..####
###...#..#######..#...###
###.#.#..#.....#..#.#.###
....#....#O....#....#....
###...#..###.###..#...###
####..##.........##..####
#.@#..#...#####...#..#@.#
#.......................#
#########################
 
"""

#Dans tout le programme : direction est un chiffre, déplacement un liste de len = 2

grille = [] # matrice (liste de listes) du schema de la grille 

# positions de la forme [ligne][colonne]
pos_pacman = []
pos_fantomes = []

# "vecteurs" déplcament avec leur lettre de direction
# correspondante
DEPLACEMENTS = ((0,1), (0,-1), (-1,0), (1,0))
DIRECTIONS = ("d", "q", "z", "s")

# symboles utilisés
CAR_PACMAN = 'O'
CAR_FANTOME = '@'
CAR_DEAD = 'X'

GAME_OVER = """ 
 ██████╗  █████╗ ███╗   ███╗███████╗
██╔════╝ ██╔══██╗████╗ ████║██╔════╝
██║  ███╗███████║██╔████╔██║█████╗  
██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  
╚██████╔╝██║  ██║██║ ╚═╝ ██║███████

  ██████╗ ██╗   ██╗███████╗██████╗ 
██╔═══██╗██║   ██║██╔════╝██╔══██╗
██║   ██║██║   ██║█████╗  ██████╔╝
██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
 ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝"""

GAGNE = """ 
██████╗  █████╗  ██████╗ ███╗   ██╗███████╗██████╗     ██╗
██╔════╝ ██╔══██╗██╔════╝ ████╗  ██║██╔════╝██╔══██╗    ██║
██║  ███╗███████║██║  ███╗██╔██╗ ██║█████╗  ██████╔╝    ██║
██║   ██║██╔══██║██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗    ╚═╝
╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║███████╗██║  ██║    ██╗
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝    ╚═╝"""

PAC_MAN = """
██████╗  █████╗  ██████╗    ███╗   ███╗ █████╗ ███╗   ██╗
██╔══██╗██╔══██╗██╔════╝    ████╗ ████║██╔══██╗████╗  ██║
██████╔╝███████║██║         ██╔████╔██║███████║██╔██╗ ██║
██╔═══╝ ██╔══██║██║         ██║╚██╔╝██║██╔══██║██║╚██╗██║
██║     ██║  ██║╚██████╗    ██║ ╚═╝ ██║██║  ██║██║ ╚████║
╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝"""

def generer_grille():
    """Génère la grille sous forme d'un matrice contenant à
    partir du schéma."""
    li, col = -1, 0 # ligne, colonne où placer un certain caractère
    # ignorer le caractère de retour de lignes de la fin de la chaine SCHEMA_GRILLE
    for car in SCHEMA_GRILLE[:-1]:
        if car == "\n":
            grille.append([])
            li += 1
            col = 0
        else:
            if car == CAR_PACMAN:
                pos_pacman.extend([li, col])
                grille[li].append('.')
            elif car == CAR_FANTOME:
                pos_fantomes.append([li, col])
                grille[li].append('.')
            else:
                grille[li].append(car)
            col += 1

def afficher_grille(game_over):
    """
    Affiche la grille, avec une croix si il y a eu un
    game over.
    """
    for i in range(len(grille)):
        ligne = ""
        for j in range(len(grille[i])):
            pos_case = [i, j]
            if pos_case == pos_pacman:
                if game_over:
                    ligne += CAR_DEAD
                else:
                    ligne += CAR_PACMAN
            elif pos_case in pos_fantomes:
                ligne += CAR_FANTOME
            else:
                ligne += grille[i][j]
        print(ligne)

def appliquer_direction(position, direction):
    """Retourne la nouvelle position en suivant la direction donnée"""
    i, j = position
    di, dj = DEPLACEMENTS[direction]
    ni = (i + di) % len(grille) #modulo pour pouvoir passerr d'un bord a l'autre
    nj = (j + dj) % len(grille[0])
    return ni, nj

def deplacer(personnage, direction):
    """Deplace d'une case les coordonées du personnage"""
    ni, nj = appliquer_direction(personnage, direction)
    personnage[0] = ni
    personnage[1] = nj

def mouvement_possible(position, direction):
    """
    Retourne True si la case suivante depuis la position donnée
    dans la direction donnée n'est pas un mur. False sinon ou
    si la case à la position donnée est déjà un mur.
    """
    i, j = position
    ni, nj = appliquer_direction(position, direction)
    return grille[i][j] != '#' and grille[ni][nj] != '#'

def tester_intersection(position):
    """
    Retourne True si la position donnée correspond à une intersection
    ou à une bifurcation dans la grille.
    """
    # droite, gauche, haut, bas = 0, 1, 2, 3
    mvt_droite = mouvement_possible(position, 0)
    mvt_gauche = mouvement_possible(position, 1)
    mvt_haut = mouvement_possible(position, 2)
    mvt_bas = mouvement_possible(position, 3)

    return (mvt_droite or mvt_gauche) and (mvt_haut or mvt_bas)

def etape_de_deplacement(direction_pacman, directions_fantomes):
    """Déplace chaque personnages d'une case (ou 0 si ils ont atteint une
    intersection) et teste si un fantome et pacman se croisent sur la case
    après déplacement."""
    deplacer(pos_pacman, direction_pacman)
    if croisement_pacman_fantome():
        return True
    for i in range(len(pos_fantomes)):
        if mouvement_possible(pos_fantomes[i], directions_fantomes[i]):
            deplacer(pos_fantomes[i], directions_fantomes[i])
    if croisement_pacman_fantome():
        return True
    else: 
        manger_point()
    return False

def faire_prochaine_etape(direction_pacman):
    """ Renvoie True si on doit faire la prochaine étape de déplacement
    c'est à dire pacman n'a pas atteint un mur ou une bifurcation."""
    sur_intersection = tester_intersection(pos_pacman)
    mvt_possible = mouvement_possible(pos_pacman, direction_pacman)
    return not sur_intersection and mvt_possible

def deplacements(direction_pacman, directions_fantomes):
    """Effectue les étapes de déplacement d'un tour jusqu'à
    ce que pacman atteigne un mur ou une bifurcation, ou bien
    jusqu'à un game over."""
    croisement = etape_de_deplacement(direction_pacman, directions_fantomes)
    faire_etape = faire_prochaine_etape(direction_pacman)
    while not croisement and faire_etape:
        croisement = etape_de_deplacement(direction_pacman, directions_fantomes)
        faire_etape = faire_prochaine_etape(direction_pacman)
    return croisement

def manger_point():
    """
    Retire un point de la grille (remplace par un espace/case vide).
    """
    i, j = pos_pacman
    grille[i][j] = " "

def compter_points_restants():
    """
    Compte et retourne le nombre de points restants dans la grille.
    """
    points = 0
    for ligne in grille:
        for car in ligne:
            if car == '.':
                points += 1
    return points

def croisement_pacman_fantome():
    """
    Détecter si un fantome croise pacman.
    """
    for pos_fantome in pos_fantomes:
        if pos_fantome == pos_pacman:
            return True
    return False

def choix_direction_pacman():
    """
    Attente d'entrée d'une lettre par le joueur qui donne une
    direction valide à suivre.
    """

    msg = "Entrez une direction (z/q/s/d): "
    dir_clavier = input(msg)
    direction = None
    
    if dir_clavier in DIRECTIONS:
        direction = DIRECTIONS.index(dir_clavier)

    # redemander la direction tant que l'utilisateur n'entre pas
    # de direction valide.
    while direction == None or not mouvement_possible(pos_pacman, direction):
        print("La direction choisie n'est pas valide !")
        dir_clavier = input(msg)
        if dir_clavier in DIRECTIONS:
            direction = DIRECTIONS.index(dir_clavier)
    
    return direction
    

def choix_direction_fantome():
    """
    Donne une direction aléatoire à chaque fantomes
    """
    nb_fantomes = len(pos_fantomes)
    directions_fantomes = [0] * nb_fantomes
    
    for i in range(nb_fantomes):
        nouv_dir = random.randint(0, 3)
        while not mouvement_possible(pos_fantomes[i], nouv_dir):
            nouv_dir = random.randint(0, 3)
        directions_fantomes[i] = nouv_dir
    
    return directions_fantomes

def jouer_tour():
    """Joue un tour : demande la direction à prendre au joueur et réalise les
    déplacement. Retourne si il y a eur croisement avec un fantome."""
    
    direction_pacman = choix_direction_pacman()
    directions_fantomes = choix_direction_fantome()

    croisement = deplacements(direction_pacman, directions_fantomes)

    return croisement


def debut():
    print(PAC_MAN)

    time.sleep(0.5)
    print("""\n \n\n Bienvenue ! \n""")
    time.sleep(1)
    print("""
          -Votre personnage est "O"
          -Votre but est de manger tous les points
          -Mais attention aux fantomes "@" ! un contact et ils vous tuent
          -z : monter
          -s : descendre
          -q : gauche
          -d : droite
          -entrée pour valider
          """)
          
    entre = input("Presser e puis entrée pour commencer :  ")
    while entre.lower() != "e":
        entre = input("Presser e puis entrée pour commencer : ")
    print("\n"*30)    

def recommencer():
    consigne = input("Voulez vous refaire une partie ? O/N   ") 
    print("\n\n")
    if consigne.lower() == "o":
        return True
    return False
           
def tab_score():
    fichier = open("score.txt", "r")
    score = fichier.read()
    fichier.close()
    print(score)

def joueur(score):
    nom = input("Votre nom ?")
    score = str(score)
    nom_score = "  " + nom + " : " + score + "\n"
    fichier = open("score.txt", "a")
    fichier.write(nom_score)
    fichier.close()

def demo():
    
    global grille
    global pos_pacman
    global pos_fantomes
    
    
    debut()
    encore = True 
    
    
    
    while encore:
        
        grille = []
        pos_pacman = []
        pos_fantomes = []
        
        generer_grille()
        afficher_grille(False)
        points_initiaux = compter_points_restants()
        manger_point() # manger le point à la position intiale
        
        croisement = jouer_tour()
        afficher_grille(croisement)
        nb_points = compter_points_restants()
        while not croisement and nb_points > 0:
            croisement = jouer_tour()
            nb_points = compter_points_restants()
            afficher_grille(croisement)
    
        # score : on ne compte pas le point mangé
        # initialement
        score =  points_initiaux - nb_points - 1
        if nb_points == 0:
            print(GAGNE)
        else:
            print(GAME_OVER)
        print("SCORE :", score)
        encore = recommencer()
    joueur(score) 
    tab_score()

        

    
