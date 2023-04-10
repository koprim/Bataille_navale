#! /usr/bin/env python3
# coding: UTF-8
"""
Script: outil.py
"""
import flottes

import terminal

import reseau

import outils

import ia


# Fonctions à développer selon le cahier des charges


def bataille_manuel(ma_flotte, sa_flotte, joueur):
    resultats = ['gagne', 'perd', 'abandonne']

    commandes = ['stop', 'sauv']

    j1 = ma_flotte
    j2 = sa_flotte
    if joueur == 'moi':
        i = -1
    else:
        i = 0
    resultat = False
    while not resultat:
        i += 1
        if i % 2 == 0:
            print("C'est au tour du joueur 1")
            saisie_joueur = terminal.saisie_cible_valide_ou_commande(commandes)
            if saisie_joueur == 'stop':
                return resultats[2]
            elif saisie_joueur == 'sauv':
                flottes.sauvegarde_partie(j1, j2)
            else:
                flottes.analyse_tir(j2, saisie_joueur)
            terminal.affiche_flotte_2d_couleurs(j1)
            terminal.affiche_flotte_2d_couleurs(j2, True)
            if flottes.est_flotte_coulee(j2):
                return resultats[0]
        else:
            print("C'est au tour du joueur 2")
            saisie_joueur = terminal.saisie_cible_valide_ou_commande(commandes)
            if saisie_joueur == 'stop':
                return resultats[2]
            elif saisie_joueur == 'sauv':
                flottes.sauvegarde_partie(j1, j2)
            else:
                flottes.analyse_tir(j1, saisie_joueur)
            terminal.affiche_flotte_2d_couleurs(j2)
            terminal.affiche_flotte_2d_couleurs(j1, True)
            if flottes.est_flotte_coulee(j1):
                return resultats[1]


def bataille_auto(ma_flotte, sa_flotte, joueur, mode_jeu):
    resultats = ['gagne', 'perd', 'abandonne']

    commandes = ['stop', 'sauv']

    j1 = ma_flotte
    j2 = sa_flotte
    if joueur == 'moi':
        i = -1
    else:
        i = 0
    resultat = False
    while not resultat:
        if mode_jeu == 'auto':
            i += 1
            if i % 2 == 0:
                print("C'est au tour du joueur 1")
                saisie_joueur = terminal.saisie_cible_valide_ou_commande(commandes)
                if saisie_joueur == 'stop':
                    return resultats[2]
                elif saisie_joueur == 'sauv':
                    flottes.sauvegarde_partie(j1, j2)
                else:
                    flottes.analyse_tir(j2, saisie_joueur)
                terminal.affiche_flotte_2d_couleurs(j1)
                terminal.affiche_flotte_2d_couleurs(j2, True)
                if flottes.est_flotte_coulee(j2):
                    return resultats[0]
            else:
                print("C'est au tour de l'adversaire")
                saisie_joueur = flottes.tir_aleatoire(j1)
                flottes.analyse_tir(j1, saisie_joueur)
                terminal.affiche_flotte_2d_couleurs(j2)
                terminal.affiche_flotte_2d_couleurs(j1, True)
                if flottes.est_flotte_coulee(j1):
                    return resultats[1]
        elif mode_jeu == 'ia':
            i += 1
            if i % 2 == 0:
                print("C'est au tour du joueur 1")
                saisie_joueur = terminal.saisie_cible_valide_ou_commande(commandes)
                while saisie_joueur in j2['tirs']:
                    saisie_joueur = terminal.saisie_cible_valide_ou_commande(commandes)
                if saisie_joueur == 'stop':
                    return resultats[2]
                elif saisie_joueur == 'sauv':
                    flottes.sauvegarde_partie(j1, j2)
                else:
                    flottes.analyse_tir(j2, saisie_joueur)
                terminal.affiche_flotte_2d_couleurs(j1)
                terminal.affiche_flotte_2d_couleurs(j2, True)
                if flottes.est_flotte_coulee(j2):
                    return resultats[0]
            else:
                print("C'est au tour de l'adversaire")
                saisie_joueur = ia.auto(j1)
                flottes.analyse_tir(j1, saisie_joueur)
                terminal.affiche_flotte_2d_couleurs(j2)
                terminal.affiche_flotte_2d_couleurs(j1, True)
                if flottes.est_flotte_coulee(j1):
                    return resultats[1]


def initialisation_bataille_reseau(ma_flotte, sa_flotte, ip, port):
    socket_actif = reseau.connexion_serveur(ip, port)
    if socket_actif:
        commande = "pas_start"
        while commande[0] not in ['[start]', '[fin]', '[timeout]']:  # commande[0] = commande du serveur
            commande = reseau.parseur_commande(reseau.recuperation_commande_serveur(socket_actif))
            if commande[0] == '[pseudo]':
                mon_pseudo = terminal.saisie_pseudo()
                ma_flotte['pseudo'] = mon_pseudo
                reseau.repond_commande_au_serveur(socket_actif, commande[0], mon_pseudo)
            elif commande[0] == '[attente]':
                reseau.repond_commande_au_serveur(socket_actif, commande[0])
            elif commande[0] == '[start]':
                sa_flotte['pseudo'] = commande[1]  # Commande[1] = argument, dans notre cas le pseudo de l'adversaire
                reseau.repond_commande_au_serveur(socket_actif, commande[0])
            elif commande[0] in ['[fin]', '[timeout]']:
                reseau.deconnexion_serveur(socket_actif)
                return None
        return socket_actif


def bataille_reseau_tir_recu(ma_flotte, sa_flotte, case, socket_actif, no_iteration):
    effet = flottes.analyse_tir(ma_flotte, case)
    commande = "[resultat]" + case + "|" + effet
    reseau.repond_au_serveur(socket_actif, commande)
    return effet


def bataille_reseau_envoyer_tir(ma_flotte, sa_flotte, socket_actif, no_iteration):
    saisie = ia.auto(sa_flotte)
    if saisie == "stop":
        reseau.repond_au_serveur(socket_actif, "[fin]")
        return "stop"
    else:
        case = saisie
        commande = "[tir]" + case
        reseau.repond_commande_au_serveur(socket_actif, commande)
        recu = reseau.recuperation_commande_serveur(socket_actif)
        effet = reseau.parseur_commande(recu)[2]
        sa_flotte["tirs"].append(case)
        sa_flotte["effets"].append(effet)
        if effet == "touche":
            sa_flotte['nbreTouche'] += 1
        elif effet in ["coule", "gagne"]:
            sa_flotte['nbreTouche'] += 1
            sa_flotte['nbreCoule'] += 1
        reseau.repond_au_serveur(socket_actif, commande)
        reseau.repond_au_serveur(socket_actif, "[ack]")
        return effet


def bataille_reseau(ma_flotte, ip, port):
    sa_flotte = flottes.initialisation_flotte_vide()
    socket_actif = initialisation_bataille_reseau(ma_flotte, sa_flotte, ip, port)
    if socket_actif:
        no_iter = 0
        fini = False
        while not fini:
            no_iter += 1
            commande = reseau.parseur_commande(reseau.recuperation_commande_serveur(socket_actif))
            if commande[0] == '[cible]':
                resultat_tir = bataille_reseau_envoyer_tir(ma_flotte, sa_flotte, socket_actif, no_iter)
                if resultat_tir == "stop":
                    return "abandonne"
                if resultat_tir == "gagne":
                    return resultat_tir
            elif commande[0] == '[tir]':
                resultat_tir = bataille_reseau_tir_recu(ma_flotte, sa_flotte, commande[1], socket_actif, no_iter)
                if resultat_tir == "gagne":
                    return "perd"
            elif commande[0] == '[attente]':
                reseau.repond_commande_au_serveur(socket_actif, commande[0])
            elif commande[0] == '[fin]':
                return "abandonne"
        return "gagne"
    else:
        return


def choix_flotte():

    fini = False
    while not fini:
        choix = terminal.saisie_mode_initialisation_flottes()
        if choix == 'endur':
            ma_flotte = flottes.initialisation_flotte_par_dictionnaire_fixe('flotte1')
            sa_flotte = flottes.initialisation_flotte_par_dictionnaire_fixe('flotte2')
            fini = True
        elif choix == 'manuel':
            ma_flotte = flottes.initialisation_flotte_vide()
            terminal.choix_flotte_manuel_console(ma_flotte)
            sa_flotte = flottes.initialisation_flotte_vide()
            fini = True
        elif choix == 'manuel+aleatoire':
            ma_flotte = flottes.initialisation_flotte_vide()
            terminal.choix_flotte_manuel_console(ma_flotte)
            sa_flotte = flottes.initialisation_flotte_vide()
            flottes.choix_flotte_aleatoire(sa_flotte)
            fini = True
        elif choix == 'aleatoires':
            ma_flotte = flottes.initialisation_flotte_vide()
            flottes.choix_flotte_aleatoire(ma_flotte)
            sa_flotte = flottes.initialisation_flotte_vide()
            flottes.choix_flotte_aleatoire(sa_flotte)
            fini = True
        elif choix == 'restaurees':
            ma_flotte = flottes.initialisation_flotte_vide()
            sa_flotte = flottes.initialisation_flotte_vide()
            if flottes.restauration_partie(ma_flotte, sa_flotte):
                fini = True
            else:
                fini = False
    return [ma_flotte, sa_flotte]


def partie():
    flottes = choix_flotte()
    ma_flotte = flottes[0]
    sa_flotte = flottes[1]
    joueur = outils.joueur_aleatoire()
    stop = False
    while not stop:
        choix_jeu = terminal.saisie_mode_choix_jeu()
        if choix_jeu == "manuel":
            mon_pseudo = terminal.saisie_pseudo()
            res = bataille_manuel(ma_flotte, sa_flotte, joueur)
            outils.ajoute_statistiques_joueur(mon_pseudo, res)
            stop = True
        elif choix_jeu == "auto":
            mon_pseudo = terminal.saisie_pseudo()
            res = bataille_auto(ma_flotte, sa_flotte, joueur, "auto")
            outils.ajoute_statistiques_joueur(mon_pseudo, res)
            stop = True
        elif choix_jeu == "ia":
            mon_pseudo = terminal.saisie_pseudo()
            res = bataille_auto(ma_flotte, sa_flotte, joueur, "ia")
            outils.ajoute_statistiques_joueur(mon_pseudo, res)
            stop = False
        elif choix_jeu == "reseau":
            server = terminal.saisie_adresse_reseau()
            res = bataille_reseau(ma_flotte, server[0], server[1])
            outils.ajoute_statistiques_joueur(ma_flotte['pseudo'], res)
            stop = True
        outils.affichage_statistiques_joueurs()
    return


# Programme principal pour tester vos fonctions
def main():
    pass


if __name__ == '__main__':
    main()
