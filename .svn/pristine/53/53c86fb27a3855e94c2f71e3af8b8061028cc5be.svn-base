#! /usr/bin/env python3
# coding: UTF-8
"""
Script: flottes.py
"""

import pickle
import os
import string
import random
import outils
import terminal

# Fonctions à développer selon le cahier des charges


def nombre_tirs_touchant_flotte(flotte):
    tirs_touchant = 0
    for case_tir in flotte['tirs']:
        for typeBateau in flotte['bateaux']:
            for case in flotte['bateaux'][typeBateau]:
                if case_tir == case:
                    tirs_touchant += 1
    return tirs_touchant
    """return len(set(flotte['tirs']).intersection(set(flotte['bateaux'][typebateau]for typebateau in flotte['bateaux'])))"""


def initialisation_flotte_par_dictionnaire_fixe(nom):
    if nom == "flotte1":
        return {'bateaux': {'porte-avions': ["A1", "B1", "C1", "D1", "E1"],
                            'croiseur': ["A3", "A4", "A5", "A6"],
                            'contre-torpilleurs': ["J8", "J9", "J10"],
                            'sous-marin': ["F1", "F2", "F3"],
                            'torpilleur': ["D2", "E2"]},
                'tirs': [],
                'effets': [],
                'pseudo': 'moi',
                'nbreTouche': 0,
                'nbreCoule': 0}

    if nom == "flotte2":
        return {'bateaux': {'porte-avions': ["A1", "A2", "A3", "A4", "A5"],
                            'croiseur': ["B1", "B2", "B3", "B4"],
                            'contre-torpilleurs': ["D1", "D2", "D3"],
                            'sous-marin': ["E1", "E2", "E3"],
                            'torpilleur': ["H3", "H4"]},
                'tirs': [],
                'effets': [],
                'pseudo': 'adversaire',
                'nbreTouche': 0,
                'nbreCoule': 0}

    if nom == "flotte_bateau_touche":
        return {'bateaux': {'porte-avions': ["A1", "B1", "C1", "D1", "E1"],
                            'croiseur' : ["A3" , "A4" , "A5", "A6"],
                            'contre-torpilleurs' : ["J8", "J9", "J10"],
                            'sous-marin' : ["F1", "F2", "F3"],
                            'torpilleur' : ["D2", "E2"]},
                'tirs': ["A3", "A4", "A5"],
                'effets': ["touche", "touche", "touche"],
                'pseudo': 'moi',
                'nbreTouche': 3,
                'nbreCoule': 0}

    if nom == "flotte_presque_coulee":
        return {'bateaux': {'porte-avions': ["A1", "A2", "A3", "A4", "A5"],
                            'croiseur': ["B1", "B2", "B3", "B4"],
                            'contre-torpilleurs': ["D1", "D2", "D3"],
                            'sous-marin': ["E1", "E2", "E3"],
                            'torpilleur': ["H3", "H4"]},
                'tirs': ["A1", "A2", "A3", "A4", "A5",
                         "B1", "B2", "B3", "B4",
                         "D1", "D2", "D3",
                         "E1", "E2", "E3",
                         "H3"],
                'effets': ["touche", "touche", "touche", "touche", "coule",
                           "touche", "touche", "touche", "coule",
                           "touche", "touche", "coule",
                           "touche", "touche", "coule",
                           "touche"],
                'pseudo': 'moi',
                'nbreTouche': 11,
                'nbreCoule': 5}

    if nom == "flotte_vide":
        return {"bateaux": {"porte-avions": [],
                            "croiseur": [],
                            "contre-torpilleurs": [],
                            "sous-marin": [],
                            "torpilleur": []},
                "tirs": [],
                "effets": [],
                "pseudo": "anonymous",
                "nbreTouche": 0,
                "nbreCoule": 0}


def positions_bateaux(flotte, excepte=''):    # Donne le type de bateau correspond à chaque cases

    positions_des_bateaux = {}
    for typeBateaux in flotte['bateaux']:

        if typeBateaux != excepte:
            for case in flotte["bateaux"][typeBateaux]:
                positions_des_bateaux[case] = typeBateaux
    return positions_des_bateaux


def est_bateau_coule(flotte, type_bateau):      # Test pour savoir si le bateau est coulé

    if flotte["bateaux"][type_bateau] == []:
        return False

    for case in flotte["bateaux"][type_bateau]:  # Retourne False si une des cases du bateau n'est pas dans les tirs
        if case not in flotte["tirs"]:
            return False
    return True     # Si aucune case du bateau ne manque dans les tirs alors retourne True


def nombre_bateaux_coules(flotte):

    bateaux_coules = 0
    for type_bateau in flotte['bateaux']:
        if est_bateau_coule(flotte, type_bateau):
            bateaux_coules += 1

    return bateaux_coules


def analyse_tir(flotte, Ln):

    positions_des_bateaux = positions_bateaux(flotte, Ln)
    flotte["tirs"].append(Ln)
    if Ln in positions_des_bateaux:  # Si case du tir est occupé par un bateau
        type_bateau = positions_des_bateaux[Ln]     # Utilisé pour déterminer le type du bateau touché
        if est_bateau_coule(flotte, type_bateau):     # Appel de la fonction est_bateau_coule pour savoir si le bateau est coulé
            if est_flotte_coulee(flotte):  # Càd que la flotte est coulée à cause du tir
                resultat_tir = "gagne"
                flotte["nbreCoule"] += 1
                flotte["nbreTouche"] += 1
            else:
                resultat_tir = "coule"
                flotte["nbreCoule"] += 1
                flotte["nbreTouche"] += 1
        else:
            resultat_tir = "touche"
            flotte["nbreTouche"] += 1
    else:
        resultat_tir = "eau"
    flotte['effets'].append(resultat_tir)
    return resultat_tir


def analyse_tir_sans_modif(flotte, Ln):
    positions_des_bateaux = positions_bateaux(flotte, Ln)
    if Ln in positions_des_bateaux:  # Si case du tir est occupé par un bateau
        type_bateau = positions_des_bateaux[Ln]     # Utilisé pour déterminer le type du bateau touché
        if est_bateau_coule(flotte, type_bateau):     # Appel de la fonction est_bateau_coule pour savoir si le bateau est coulé
            if est_flotte_coulee(flotte):  # Càd que la flotte est coulée à cause du tir
                resultat_tir = "gagne"
            else:
                resultat_tir = "coule"
        else:
            resultat_tir = "touche"
    else:
        resultat_tir = "eau"
    return resultat_tir


def est_flotte_coulee(flotte):
    for type_bateau in flotte['bateaux']:
        if not est_bateau_coule(flotte, type_bateau):
            return False
    return True


def liste_bateaux():    # Renvoie la liste des bateaux par ordre alphabétique
    return sorted([type_bateau for type_bateau in ['porte-avions', 'croiseur', 'contre-torpilleurs', 'sous-marin', 'torpilleur']])


def sauvegarde_partie(ma_flotte, sa_flotte):
    with open("sauvegarde.bin", "wb") as fd:
        pickle.dump(ma_flotte, fd)
        pickle.dump(sa_flotte, fd)


def restauration_partie(ma_flotte, sa_flotte):
    if os.path.isfile('sauvegarde.bin'):
        with open('sauvegarde.bin', 'rb') as file:
            ma_flotte.update(pickle.load(file))
            sa_flotte.update(pickle.load(file))
        return True
    else:
        return False


def tir_aleatoire(flotte):
    tir = outils.case_aleatoire()
    while tir in flotte['tirs']:
        tir = outils.case_aleatoire()
    return tir


def longueur_bateau(bateau):
    longueurs_bateaux = {'porte-avions': 5,
                     'croiseur': 4,
                     'contre-torpilleurs': 3,
                     'sous-marin': 3,
                     'torpilleur': 2}
    return longueurs_bateaux[bateau]


def initialisation_flotte_vide():
    flotte = {'bateaux': {'porte-avions': [],
                             'croiseur': [],
                             'contre-torpilleurs': [],
                             'sous-marin': [],
                             'torpilleur': []},
                 'tirs': [],
                 'effets': [],
                 'pseudo': 'anonymous',
                 'nbreTouche': 0,
                 'nbreCoule': 0}
    return flotte


def choix_flotte_aleatoire(flotte):

    liste_bateaux = ['porte-avions', 'croiseur', 'contre-torpilleurs', 'sous-marin', 'torpilleur']

    for bateau in liste_bateaux:
        position = outils.case_aleatoire()
        direction = random.choice(['horizontal', 'vertical'])
        if bateau == 'porte-avions':  # taille : 5

            emplacement = positionne_bateau_par_direction(flotte, bateau, position, direction)
            while not emplacement:
                position = outils.case_aleatoire()
                emplacement = positionne_bateau_par_direction(flotte, bateau, position, direction)

        elif bateau == 'croiseur':  # taille : 4

            emplacement = positionne_bateau_par_direction(flotte, bateau, position, direction)
            while not emplacement:
                position = outils.case_aleatoire()
                emplacement = positionne_bateau_par_direction(flotte, bateau, position, direction)

        elif bateau == 'contre-torpilleurs':  # taille : 3

            emplacement = positionne_bateau_par_direction(flotte, bateau, position, direction)
            while not emplacement:
                position = outils.case_aleatoire()
                emplacement = positionne_bateau_par_direction(flotte, bateau, position, direction)

        elif bateau == 'sous-marin':  # taille : 3

            emplacement = positionne_bateau_par_direction(flotte, bateau, position, direction)
            while not emplacement:
                position = outils.case_aleatoire()
                emplacement = positionne_bateau_par_direction(flotte, bateau, position, direction)

        elif bateau == 'torpilleur':  # taille : 2

            emplacement = positionne_bateau_par_direction(flotte, bateau, position, direction)
            while not emplacement:
                position = outils.case_aleatoire()
                emplacement = positionne_bateau_par_direction(flotte, bateau, position, direction)


def est_flotte_complete(flotte):

    liste_bateaux = ['porte-avions', 'croiseur', 'contre-torpilleurs', 'sous-marin', 'torpilleur']
    for bateau in liste_bateaux:
        if bateau == 'porte-avions':
            if not flotte['bateaux'][bateau] or len(flotte['bateaux'][bateau]) < longueur_bateau(bateau):
                return False
        elif bateau == 'croiseur':
            if not flotte['bateaux'][bateau] or len(flotte['bateaux'][bateau]) < longueur_bateau(bateau):
                return False
        elif bateau == 'contre-torpilleurs':
            if not flotte['bateaux'][bateau] or len(flotte['bateaux'][bateau]) < longueur_bateau(bateau):
                return False
        elif bateau == 'sous-marin':
            if not flotte['bateaux'][bateau] or len(flotte['bateaux'][bateau]) < longueur_bateau(bateau):
                return False
        elif bateau == 'torpilleur':
            if not flotte['bateaux'][bateau] or len(flotte['bateaux'][bateau]) < longueur_bateau(bateau):
                return False
    return True


def positionne_bateau_par_direction(flotte, bateau, case, direction):

    longueur = longueur_bateau(bateau)

    position = calcul_positions_bateau(case, direction, longueur)
    if not position:
        return False
    for case in position:
        for case2 in positions_bateaux(flotte):
            if case == case2:
                return False
    flotte['bateaux'][bateau] = position
    print("-> positionnement du {} en {} effectué".format(bateau, ", ".join(position)))
    return True


def positionne_bateau_par_direction_silence(flotte, bateau, case, direction):

    longueur = longueur_bateau(bateau)

    position = calcul_positions_bateau(case, direction, longueur)
    if not position:
        return False
    for case in position:
        for case2 in positions_bateaux(flotte):
            if case == case2:
                return False
    flotte['bateaux'][bateau] = position
    return True


def choix_flotte_aleatoire_silence(flotte):

    liste_bateaux = ['porte-avions', 'croiseur', 'contre-torpilleurs', 'sous-marin', 'torpilleur']

    for bateau in liste_bateaux:
        position = outils.case_aleatoire()
        direction = random.choice(['horizontal', 'vertical'])
        if bateau == 'porte-avions':  # taille : 5

            emplacement = positionne_bateau_par_direction_silence(flotte, bateau, position, direction)
            while not emplacement:
                position = outils.case_aleatoire()
                emplacement = positionne_bateau_par_direction_silence(flotte, bateau, position, direction)

        elif bateau == 'croiseur':  # taille : 4

            emplacement = positionne_bateau_par_direction_silence(flotte, bateau, position, direction)
            while not emplacement:
                position = outils.case_aleatoire()
                emplacement = positionne_bateau_par_direction_silence(flotte, bateau, position, direction)

        elif bateau == 'contre-torpilleurs':  # taille : 3

            emplacement = positionne_bateau_par_direction_silence(flotte, bateau, position, direction)
            while not emplacement:
                position = outils.case_aleatoire()
                emplacement = positionne_bateau_par_direction_silence(flotte, bateau, position, direction)

        elif bateau == 'sous-marin':  # taille : 3

            emplacement = positionne_bateau_par_direction_silence(flotte, bateau, position, direction)
            while not emplacement:
                position = outils.case_aleatoire()
                emplacement = positionne_bateau_par_direction_silence(flotte, bateau, position, direction)

        elif bateau == 'torpilleur':  # taille : 2

            emplacement = positionne_bateau_par_direction_silence(flotte, bateau, position, direction)
            while not emplacement:
                position = outils.case_aleatoire()
                emplacement = positionne_bateau_par_direction_silence(flotte, bateau, position, direction)


def calcul_positions_bateau(case, direction, longueur):

    liste_cases_bateau = []

    if outils.est_case_valide(case):

        liste_cases_bateau = [case]

        if direction == 'horizontal':

            for i in range(1, longueur):
                case_supp = case[0] + str(int(case[1:]) + i)
                if outils.est_case_valide(case_supp):
                    liste_cases_bateau.append(case_supp)
                else:
                    liste_cases_bateau = []
                    return liste_cases_bateau

        elif direction == 'vertical':

            for i in range(1, longueur):
                case_supp = string.ascii_uppercase[string.ascii_uppercase[:10].index(case[0]) + i] + case[1:]
                if outils.est_case_valide(case_supp):
                    liste_cases_bateau.append(case_supp)
                else:
                    liste_cases_bateau = []
                    return liste_cases_bateau

        return liste_cases_bateau
    else:
        return liste_cases_bateau


def memorise_action_tir_sur_flotte_inconnue(flotte, case, resultat):
    flotte['tirs'].append(case)
    flotte['effets'].append(resultat)
    if resultat == "touche":
        flotte['nbreTouche'] += 1
    elif resultat in ["coule", "gagne"]:
        flotte['nbreTouche'] += 1
        flotte['nbreCoule'] += 1


def envoi_flotte_via_serveur(flotte):
    return ''.join(c for c in str([bateau + "|" + str(flotte["bateaux"][bateau]) for bateau in flotte["bateaux"]])
                   .replace(",", "|") if c not in " []\'\"")


def initialisation_flotte_par_commande_du_serveur(flotte, liste):
    flotte_temp = {"bateaux": {bateau: [] for bateau in liste_bateaux()}}
    for val in liste:
        if val in liste_bateaux():
            bateau = val
        else:
            flotte_temp["bateaux"][bateau].append(val)
    flotte.update(flotte_temp)


# Programme principal pour tester vos fonctions
def main():
    pass


if __name__ == '__main__':
    main()
