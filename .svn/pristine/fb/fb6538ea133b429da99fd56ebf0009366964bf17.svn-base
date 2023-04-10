#! /usr/bin/env python3
# coding: UTF-8
"""
Script: terminal.py
"""
import flottes
import outils
import string
import couleurs as coul
import reseau


# Fonctions à développer selon le cahier des charges
def affiche_flotte_textuelle(flotte):
    bateaux = flotte['bateaux']  # fait un dictionnaire avec les bateaux et leurs positions
    liste_bateaux = list(bateaux.keys())  # met dans une liste les différents noms de bateaux
    liste_positions = list(bateaux.values())  # met dans une liste les différentes positions de bateaux
    phrase = ""
    for i in range(len(liste_positions)):
        phrase += "   > "+liste_bateaux[i]+" : "
        for case in liste_positions[i]:
            phrase += case+", "
        phrase = phrase[:-2] + "\n"
    print(phrase[:-1])


def affiche_flotte_2d(flotte, cachee=False):  # Affiche un tableau 2D contenant la flotte

    types_bateaux = {'porte-avions': "p",
                'croiseur': "c",
                'contre-torpilleurs': "q",
                'sous-marin': "s",
                'torpilleur': "t"}

    taille_grille = 10

    print("   |", end="")  # Affiche les colonnes
    for n in range(taille_grille):
        print(" {}".format(n+1), end="")
    print("|")

    print("-" * 3 + "|" + "--" * taille_grille + "-|")  # Affiche la ligne séparatrice

    if not cachee:  # Affiche la flotte et les tirs
        positions_bateaux = flottes.positions_bateaux(flotte)
        for L in string.ascii_uppercase[:taille_grille]:
            print(" {} |".format(L), end="")

            for n in range(taille_grille):
                case = L + str(n+1)

                if case in flotte['tirs']:
                    effet = flottes.analyse_tir_sans_modif(flotte, case)
                else:
                    effet = "sauf"

                if case in positions_bateaux.keys():
                    lettre_bateau = types_bateaux[positions_bateaux[case]]
                    if effet == "sauf":
                        print(" {}".format(lettre_bateau), end="")
                    else:
                        print(" {}".format(lettre_bateau.upper()), end="")
                else:
                    if case in flotte['tirs']:
                        print(" O", end="")
                    else:
                        print("  ", end="")
            print(' |')

    elif cachee:
        positions_bateaux = flottes.positions_bateaux(flotte)
        for L in string.ascii_uppercase[:taille_grille]:
            print(" {} |".format(L), end="")

            for n in range(taille_grille):
                case = L + str(n + 1)

                if case in flotte['tirs']:
                    effet = flottes.analyse_tir_sans_modif(flotte, case)
                else:
                    effet = "sauf"

                if case in positions_bateaux.keys():
                    if not effet == "sauf":
                        print(" X", end="")
                    else:
                        print("  ", end="")
                else:
                    if case in flotte['tirs']:
                        print(" O", end="")
                    else:
                        print("  ", end="")
            print(' |')
    print("-" * 3 + "|" + "--" * taille_grille + "-|")  # Affiche la ligne séparatrice


def affiche_flotte_2d_couleurs(flotte, cachee = False):

    couleurs = {'porte-avions': "rouge",
                'croiseur': "cyan",
                'contre-torpilleurs': "jaune",
                'sous-marin': "vert",
                'torpilleur': "magenta"}

    signes = {'sauf': "#",
              'touche': 'X',
              'coule': 'X',
              'gagne': 'X',
              'eau': "O"}

    taille_grille = 10

    print("   |", end="")
    for n in range(taille_grille):
        print(" {}".format(n+1), end="")
    print("|")

    print("-" * 3 + "|" + "--" * taille_grille + "-|")

    if not cachee:
        positions_bateaux = flottes.positions_bateaux(flotte)
        for L in string.ascii_uppercase[:taille_grille]:
            print(" {} |".format(L), end="")

            for n in range(taille_grille):
                case = L + str(n + 1)

                if case in flotte['tirs']:
                    effet = flottes.analyse_tir_sans_modif(flotte, case)
                else:
                    effet = "sauf"

                if case in positions_bateaux.keys():

                    couleur = couleurs[positions_bateaux[case]]
                    exec('print(coul.COULEURS["{}"], end="")'.format(couleur))
                    print(" {}".format(signes[effet]), end="")
                    print(coul.COULEURS["blanc"], end="")  # et retour à la couleur de caractère par défaut

                else:
                    if case in flotte['tirs']:
                        print(" O", end="")
                    else:
                        print("  ", end="")
            print(' |')

    elif cachee:
        for L in string.ascii_uppercase[:taille_grille]:
            print(" {} |".format(L), end="")

            for n in range(taille_grille):
                case = L + str(n + 1)
                if case in flotte['tirs']:
                    effet = flottes.analyse_tir_sans_modif(flotte, case)
                    if effet == "eau":
                        print(" {}".format(signes[effet]), end="")
                    else:
                        print(coul.COULEURS['rouge'], end="")
                        print(" {}".format(signes[effet]), end="")
                        print(coul.COULEURS["blanc"], end="")  # et retour à la couleur de caractère par défaut
                else:
                    print("  ", end="")
            print(' |')

    print('---|' + '--' * taille_grille + '-|')


def saisie_cible_valide_ou_commande(commandes):
    valide = False
    while not valide:
        saisie = input('Entrez cible ou commande : ')
        if outils.est_case_valide(saisie) or saisie in commandes:
            valide = True
    return saisie


def saisie_direction_valide():
    valide = False
    while not valide:
        saisie = input("Veuillez entrer une direction : ")
        if saisie.lower() in ["h", "horizontal"]:
            return "horizontal"
        elif saisie.lower() in ["v", "vertical"]:
            return "vertical"


def choix_bateau_a_positionner(flotte):     # Pas fini, à faire avec longueur bateau et liste bateaux
    print("Choisir le bateau à (re)positionner parmi :")
    n = 0
    for bateau in flottes.liste_bateaux():
        n += 1
        print("   {}) {} ({} cases), ".format(n, bateau, flottes.longueur_bateau(bateau)), end="")
        if flotte['bateaux'][bateau] == []:
            print("actuellement non positionné")
        else:
            print("actuellement en ", end="")
            print(str(flotte['bateaux'][bateau]).replace("'", "").replace("[", "").replace("]", ""))
    print("Taper stop pour stopper le choix de la flotte")
    valide = False
    while not valide:
        saisie = input("Entre le numéro du bateau ou stop : ")
        if saisie in [str(n) for n in range(1, len(flottes.liste_bateaux()) + 1)]:
            return int(saisie)
        elif saisie == "stop":
            if flottes.est_flotte_complete(flotte):
                return "stop"


def affiche_flotte_inconnue_2d(flotte):
    signes = {'sauf': "#",
              'touche': 'X',
              'coule': 'X',
              'gagne': 'X',
              'eau': "O"}
    taille_grille = 10
    nb_touche = 0
    nb_coule = 0
    print("   |", end="")
    for n in range(taille_grille):
        print(" {}".format(n+1), end="")
    print("|")
    print("-" * 3 + "|" + "--" * taille_grille + "-|")
    for L in string.ascii_uppercase[:taille_grille]:
        print(" {} |".format(L), end="")
        for n in range(taille_grille):
            case = L + str(n + 1)
            if case in flotte['tirs']:
                effet = flotte['effets'][flotte['tirs'].index(case)]
                if effet == "eau":
                    pass
                elif effet == "touche":
                    nb_touche += 1
                elif effet == "coule" or "gagne":
                    nb_touche += 1
                    nb_coule += 1
                print(" {}".format(signes[effet]), end="")
            else:
                print("  ", end="")
        print(' |')
    print('---|' + '--' * taille_grille + '-|')
    print("\nIndicateurs : {} touches / {} bateau(x) coulé(s)".format(nb_touche, nb_coule))


def saisie_mode_initialisation_flottes():
    mode_flotte = ['endur', 'manuel', 'manuel+aleatoire', 'aleatoires', 'restaurees']
    valide = False
    while not valide:
        print("""
Mode de choix de la flotte :
----------------------------
 1> flottes initialisées en dur
 2> flotte du joueur initialisée manuellement et flotte de l'adversaire vide
 3> flotte du joueur initialisée manuellement et flotte de l'adversaire aléatoirement
 4> flottes initialisées aléatoirement (defaut)
 5> flottes restaurées de la dernière partie sauvegardée
""")
        saisie = input("Veuillez saisir le mode de flotte: ")
        if saisie in [str(i) for i in range(1, 6)]:
            saisie = int(saisie)
            valide = True
    return mode_flotte[saisie - 1]


def saisie_pseudo():
    valide = False
    while not valide:
        saisie = input("Veuillez entrer votre pseudo: ")
        if saisie != "":
            valide = True
    return saisie


def saisie_mode_choix_jeu():
    choix = ["manuel", "auto", "ia", "reseau"]
    valide = False
    while not valide:
        print("""
Mode de choix du jeu :
----------------------
 1> jeu entièrement manuel [utile pour le debug] (choix par defaut)
 2> jeu automatique contre l'ordinateur
 3> jeu automatique avancé contre l'ordinateur (tir avec IA)
 4> jeu en réseau
""")
        saisie = input("Veuillez saisir le mode de choix: ")
        if saisie in [str(i) for i in range(1, 5)]:
            saisie = int(saisie)
            valide = True
    return choix[saisie - 1]


def choix_flotte_manuel_console(flotte):
    bateau = {3: 'porte-avions',
              2: 'croiseur',
              1: 'contre-torpilleurs',
              4: 'sous-marin',
              5: 'torpilleur'}
    commandes = ['stop']
    fini = False
    while not fini:
        saisie = choix_bateau_a_positionner(flotte)
        if saisie == 'stop':
            return
        else:
            print("Choisir la case de début du {}".format(bateau[saisie]))
            position = saisie_cible_valide_ou_commande(commandes)
            cases_occupes = str(flotte["bateaux"].values())
            if position in cases_occupes:
                print("-> positionnement du {} échoué".format(bateau[saisie]))
            elif position not in commandes:
                direction = saisie_direction_valide()
                flottes.positionne_bateau_par_direction(flotte, bateau[saisie], position, direction)
                fini = flottes.est_flotte_complete(flotte)
            print("La flotte en 2D :")
            affiche_flotte_2d_couleurs(flotte)
            print()
    choix_bateau_a_positionner(flotte)
    return


def saisie_adresse_reseau():
    ok = False
    while not ok:
        saisie = input("Veuillez saisir l'adresse du serveur au format serveur:port : ")
        if saisie.find(":") > 0:
            repere = saisie.find(":")
            serveur = saisie[:repere]
            port = saisie[repere + 1:]
            if port.isnumeric():
                port = int(port)
                ok = True
    return [serveur, port]


# Programme principal pour tester vos fonctions
def main():
    pass


if __name__ == '__main__':
    main()
