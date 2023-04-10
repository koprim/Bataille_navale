#! /usr/bin/env python3
# coding: UTF-8
"""
Script: outil.py
"""
import string
import random
import os


# Fonctions à développer selon le cahier des charges
def est_case_valide(case):  # Vérifie que la case en format Ln soit valide
    if len(case) in [2, 3]:
        case_Ln = [case[0], case[1:]]
    else:
        return False
    lettres = string.ascii_uppercase
    lettres = list(lettres[:10])
    chiffres = [str(i) for i in range(1, 11)]
    if case_Ln[1] in chiffres and case_Ln[0] in lettres:
        return True
    else:
        return False


def indices_vers_case_ln(indices):  # Convertie une case au format d'indices en format Ln
    alphabet = string.ascii_uppercase
    if indices[0] in range(10) and indices[1] in range(10):
        indice_ligne = indices[1]+1
        indice_colonne = alphabet[indices[0]]
        case_ln = indice_colonne + "{}".format(indice_ligne)
        return case_ln


def case_ln_vers_indices(case_Ln):  # Convertie une case au format Ln en format d'indices
    alphabet = [str(car) for car in string.ascii_uppercase[:10]]
    if str(case_Ln[0]) in alphabet and case_Ln[1:] in [str(i) for i in range(1, 11)]:
        indice_colonne = int(case_Ln[1:]) - 1
        indice_ligne = alphabet.index(case_Ln[0])
        case = [indice_ligne, indice_colonne]
        return case


def case_aleatoire():
    return random.choice(string.ascii_uppercase[:10]) + str(random.randint(1, 10))


def joueur_aleatoire():
    return random.choice(['moi', 'adversaire'])


def affichage_statistiques_joueurs():
    if os.path.isfile('statistiques.txt'):
        with open('statistiques.txt', 'r') as file:
            if file.readlines() == []:
                vide = True
            else:
                vide = False
        if not vide:
            with open('statistiques.txt', 'r') as file:
                longueur_pseudo_max = max([len(ligne.replace("\n", "").split(";")[0]) for ligne in file])
                if longueur_pseudo_max < 7:
                    ecart = 9     # Nombre utilisé pour obtenir le bon nombre de tirets / égales
                else:
                    ecart = longueur_pseudo_max + 2
                affichage = "+" + "-" * ecart + "+----------------+-----------+----------+----------+\n"
                affichage += "| Joueurs" + " " * (ecart - 8) + "| Parties jouées | Victoires | Défaites | Abandons |\n"
                affichage += "+" + "=" * ecart + "+================+===========+==========+==========+\n"
            with open('statistiques.txt', 'r') as file:
                for ligne in file:
                    donnees = ligne.replace("\n", "").split(";")
                    pseudo = donnees[0]
                    longueur_pseudo = len(pseudo) + 1
                    jouees = donnees[1]
                    victoires = donnees[2]
                    defaites = donnees[3]
                    abandons = str(int(donnees[1]) - int(donnees[2]) - int(donnees[3]))
                    affichage += "| {}".format(pseudo) + " " * (ecart - longueur_pseudo) + "| {:15}| {:10}| {:9}| {:9}|\n".format(jouees, victoires, defaites, abandons)
                    affichage += "+" + "-" * ecart + "+----------------+-----------+----------+----------+\n"
        else:
            affichage = """+---------+----------------+-----------+----------+----------+
| Joueurs | Parties jouées | Victoires | Défaites | Abandons |
+=========+================+===========+==========+==========+\n"""
        return affichage
    else:
        return ""


def ajoute_statistiques_joueur(pseudo, resultat):
    ajout_jouee, ajout_victoire, ajout_defaite = 1, 0, 0
    if resultat == "gagne":
        ajout_victoire = 1
    elif resultat == "perd":
        ajout_defaite = 1

    if os.path.isfile('statistiques.txt'):  # On vérifie si le fichier existe déjà ou non
        with open('statistiques.txt', 'r') as fichier:
            # On crée un dictionnaire qui contient les valeurs de statistiques triées par pseudo
            donnees = {ligne.replace("\n", "").split(";")[0]: ligne.replace("\n", "").split(";")[1:] for ligne in fichier.readlines()}

            if pseudo in donnees.keys():    # On regarde si le pseudo était déjà présent ou non
                donnees[pseudo][0] = str(int(donnees[pseudo][0]) + ajout_jouee)
                donnees[pseudo][1] = str(int(donnees[pseudo][1]) + ajout_victoire)
                donnees[pseudo][2] = str(int(donnees[pseudo][2]) + ajout_defaite)
            else:
                donnees[pseudo] = [str(ajout_jouee), str(ajout_victoire), str(ajout_defaite)]
    else:
        donnees = {pseudo: [str(ajout_jouee), str(ajout_victoire), str(ajout_defaite)]}

    with open('statistiques.txt', 'w') as fichier:
        for pseudo in donnees:
            ligne = pseudo
            for val in donnees[pseudo]:
                ligne += ";" + val
            fichier.write(ligne + "\n")


def case_min(liste_cases):  # Renvoie la case minimale parmis les cases d'un bateau
    cases = [case for case in liste_cases if len(case) <= 2]
    if cases:
        return min(cases)
    else:
        return min(liste_cases)


def case_max(liste_cases):  # Renvoie la case maximale parmis les cases d'un bateau
    sup3 = 0
    for case in liste_cases:
        if len(case) == 3:
            sup3 += 1
    if sup3 > 0:
        return max([case for case in liste_cases if len(case) == 3])
    else:
        return max(liste_cases)


# Programme principal pour tester vos fonctions
def main():
    pass


if __name__ == '__main__':
    main()

