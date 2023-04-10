# -*- coding: utf-8 -*-
"""
Script client_serveur_basique.py
==============================

Script permettant de tester manuellement le protocole d'échange avec le serveur de
la bataille navale.
"""
__author__ = "C. BARAS"
__version__ = "1.0"

if __name__ == '__main__':
    import socket

    print("*** Script client_serveur_basique.py ***")

    # Variable globale
    COMMANDES = {
        '[pseudo]': '[pseudo]nom',
        '[attente]': '[ack]',
        '[start]': '[ack]',
        '[cible]': '[tir]Ln',
        '[commande_invalide]': '[ack]',
        '[tir]': '[resultat]Ln|res',
        '[resultat]': '[ack]',
        '[flotte]': '[flotteadverse]sous-marin|Ln|Ln|Ln|porte-avions|Ln|Ln|Ln|Ln|Ln|torpilleur|Ln|Ln|croiseur|Ln|Ln|Ln|Ln|contre-torpilleurs|Ln|Ln|Ln]',
        '[flotteadverse]': '[ack]',
        '[fin]': None
    }
    print("> Liste des commandes du serveur et des réponses à fournir")
    print("\n".join([" " * 3 + cle + " -> " + (valeur if valeur is not None else "pas de reponse") for (cle, valeur) in
                     list(COMMANDES.items())]))

    # Initialisations des paramètres du serveur
    hote = '10.0.26.2'  # ip
    port = 2010  # port

    # Connexion au serveur par création et ouverture d'un objet socket
    # permettant la connexion avec le serveur
    try:
        socket_actif = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_actif.connect((hote, port))
        est_connecte = True
        print("> Connexion établie avec le serveur %s sur le port %d" % (hote, port))
    except socket.error:
        print("> La connexion a échouée")
        socket_actif = None
        est_connecte = False

    # Boucle traitant les échanges avec le serveur : chaque commande
    # reçue du serveur doit être suivie d'une réponse appropriée
    # envoyée parle client
    reponse = ""
    while reponse != "[fin]" and est_connecte == True:

        # Lecture de la commande du serveur
        try:
            recu = socket_actif.recv(1024)
            print("commande reçue du serveur : ", recu)
        except socket.error:
            # Problème dans la connexion impliquant la déconnexion du client
            est_connecte = False

        # Saisie de la réponse du client
        reponse = input("saisir votre reponse ou [fin]>")

        # Envoi de la réponse au serveur
        if reponse != "[fin]":
            socket_actif.send(reponse)
    # Fin de la boucle de traitement

    # Déconnexion du serveur
    try:
        socket_actif.send("[fin]")
        socket_actif.close()
        print("Deconnexion du serveur %s réussie" % hote)
    except:
        pass

    # Fin du sript
    print("*** fin du script client_serveur_basique.py ***")
