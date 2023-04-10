# -*- coding: utf-8 -*-
"""
Résumé du module reseau.py
==========================

Le module :mod:`outils_reseau` peut être utile pour implémenter le jeu en réseau (une des améliorations proposées pour la bataille navale).
Il centralise les **outils de communication réseau basée sur TCP** nécessaires
à la version du jeu avec serveur : 

* **connexion** au serveur avec le module :mod:`socket` permettant la création d'un objet `socket_actif` modélisant une extrémité du flux
  de communication entre un client et un serveur (cf. :mod:`reseau.connexion_serveur`)
 
* **lecture** des commandes envoyées par le serveur avec :func:`socket_actif.recv` (cf. :mod:`reseau.recuperation_commande_serveur`)

* **envoi** de données au serveur avec :func:`socket_actif.send` (cf. :mod:`reseau.repond_au_serveur`)

* **fermeture de la connexion** (cf. :mod:`reseau.deconnexion_serveur`)

Les échanges client/serveur devront respecter :ref:`le protocole de communication entre le serveur et les joueurs/clients <protocole-communication-label>`. 

On pourra utiliser la constante ``COMMANDES`` qui liste sous la forme d'un dictionnaire le nom des commandes envoyés par le serveur et le format des réponses attendues :

.. code-block:: python 

    COMMANDES = { '[pseudo]' : '[pseudo]nom',
                  '[attente]' : '[ack]', 
                  '[start]' : '[ack]',
                  '[cible]' : '[tir]Ln',
                  '[commande_invalide]' : '[ack]',
                  '[tir]' : '[resultat]Ln|res',
                  '[resultat]' : '[ack]',
                  '[flotte]' : '[flotteadverse]sous-marin|Ln|Ln|Ln|porte-avions|Ln|Ln|Ln|Ln|Ln|torpilleur|Ln|Ln|croiseur|Ln|Ln|Ln|Ln|contre-torpilleurs|Ln|Ln|Ln]', 
                  '[flotteadverse]' : '[ack]',
                  '[timeout]' : None,
                  '[fin]' : None
                  }
                  
.. seealso : la description du fonctionnement du serveur dans :py:mod:`serveur`, le script :py:mod:`client_serveur_basique.py` donnant un exemple de client se connectant au serveur

Détails du module reseau.py
===========================
              
"""
import socket

# %% Liste des commandes du serveur et des réponses (avec format) que chaque commande accepte
COMMANDES = {'[pseudo]': '[pseudo]nom',
             '[attente]': '[ack]',
             '[start]': '[ack]',
             '[cible]': '[tir]Ln',
             '[commande_invalide]': '[ack]',
             '[tir]': '[resultat]Ln|res',
             '[resultat]': '[ack]',
             '[flotte]': '[flotteadverse]sous-marin|Ln|Ln|Ln|porte-avions|Ln|Ln|Ln|Ln|Ln|torpilleur|Ln|Ln|croiseur|Ln|Ln|Ln|Ln|contre-torpilleurs|Ln|Ln|Ln]',
             '[flotteadverse]': '[ack]',
             '[timeout]': None,
             '[fin]': None
             }
TIMER = 60  # 60*3 # 3 minutes


def parseur_commande(recu):
    """
    Analyse les données reçues dans les échanges serveur/client et les découpe
    sur le format `[commande]donnee1|donnee2|donnee3|...`, en renvoyant les informations
    découpées dans une liste de la forme ``[ commande, donnees1, donnees2, donnees3, ...]``.
    Renvoie ``None`` si le découpage n'a pas réussi.

    :param recu: la commande à parser
    :type recu: str
    :return: la liste des données de la commande segmentée
    :rtype: list
    """

    ind_deb_commande = recu.find('[')
    ind_fin_commande = recu.find(']')
    if ind_deb_commande < 0 or ind_fin_commande < 0:  # Pas de commande dans l'info recu
        return None

    commande = recu[ind_deb_commande:ind_fin_commande + 1]
    donnees = recu[ind_fin_commande + 1:]
    decoupage = [commande]
    if len(donnees) > 0:  # Commande avec paramètre
        elmts = donnees.split('|')
        decoupage += elmts
    return decoupage


def connexion_serveur(hote, port):
    """
    Amorce la connexion au serveur de bataille navale (cf. script :mod:`serveur.py <serveur>`),
    dont l'ip et le port sont passés en paramètre.
    Renvoie le socket créé par la connexion, ou ``None`` si la connexion a échouée.

    :param hote: l'ip du serveur sous la forme xxx.xxx.xxx.xxx ou de localhost
    :type hote: str
    :param port: le port du serveur
    :type port: int
    :return: le socket créé par la connexion ou ``None`` en cas d'échec
    :rtype: instance
    """
    try:
        socket_actif = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_actif.connect((hote, port))
        socket_actif.settimeout(TIMER)  # Fixe un time out sur l'attente des commandes du serveur
        print("> Connexion établie avec le serveur %s:%d" % (hote, port))
    except socket.error:
        print("> La connexion au serveur %s:%d a échouée" % (hote, port))
        socket_actif = None
    return socket_actif


def deconnexion_serveur(socket_actif):
    """
    Déconnexion du serveur.

    :param socket_actif: le socket assurant le dialogue client/serveur
    :type socket_actif: instance
    """
    try:
        socket_actif.close()
        print("Deconnexion réussie")
    except:
        pass


def recuperation_commande_serveur(socket_actif):
    """
    Attend la commande envoyée par le serveur et la renvoie.
    Si la commande n'a pas pu être lue dans le temps imparti (cf. :func:`socket.settimeout`),
    renvoie ``"[timeout]"`` ; dans tous les autres cas, renvoie ``"[commande_invalide]"``.

    :param socket_actif: le socket assurant le dialogue client/serveur
    :type socket_actif: instance
    :return: la ligne de commande, ``"[timeout]"`` ou ``None``
    :rtype: str
    """
    try:
        commande = socket_actif.recv(1024)
        print("serveur>client:" + commande)
    except socket.timeout:
        commande = "[timeout]"
        print("client> Délai de réponse du serveur dépassé; " + commande)
    except Exception as e:
        commande = "[commande_invalide]"
        print("client> Exception dans la réception de la commande du serveur; " + e)
    return commande


def repond_commande_au_serveur(socket_actif, commande, parametre=None):
    """
    Envoi au serveur la réponse apropriée à la commande qu'il a envoyée, pour
    assurer le bon déroulement des échanges client/serveur. La réponse est
    constituée d'une commande et d'un éventuel paramètre.

    Fonction interne: la réponse est calculée à partir de la commande du serveur.

    :param socket_actif: le socket assurant le dialogue client/serveur
    :type socket_actif: instance
    :param commande: la commande à renvoyer au serveur
    :type commande: str parmi [start], [pseudo], [attente], [tir], [resultat], [gagne]
    :param parametres: les paramètres de la commande
    :type parametres: str
    """
    if commande in COMMANDES:
        cmdAttendu = parseur_commande(COMMANDES[commande])[0]
        reponse = cmdAttendu + (parametre if parametre else "")
        repond_au_serveur(socket_actif, reponse)
    else:
        print("client>serveur: réponse au serveur inappropriée pour la commande", commande)


def repond_au_serveur(socket_actif, reponse):
    """
    Envoi au serveur la réponse apropriée à la commande qu'il a envoyée, pour
    assurer le bon déroulement des échanges client/serveur.

    :param socket_actif: le socket assurant le dialogue client/serveur
    :type socket_actif: instance
    :param reponse: la commande à renvoyer au serveur avec ses éventuels paramètres (cf :ref:`commandes-serveur-label`)
    :type reponse: str
    """
    print("client>serveur:", reponse)
    socket_actif.send(reponse)


#    # Commandes informatives
#    if "[start]" in commande : reponse = "[ack]"
#    elif "[pseudo]" in commande : reponse = "[pseudo]" + parametre
#    elif "[attente]" in commande : reponse = "[ack]"
#    elif "[cible]" in commande : reponse = "[tir]" + parametre
#    elif "[tir]" in commande : reponse = "[resultat]" + parametre
#    elif "[resultat]" in commande : reponse = "[ack]"
#    elif "[flotte]" in commande : reponse = "[flotteadverse]" + parametre
#    elif "[flotteadverse]" in commande : reponse = "[ack]"
#    else : reponse = None
#
#    if reponse :
#        print "client>serveur:", reponse
#        socketActif.send( reponse )
#    else :
#        print "client>serveur: réponse au serveur inappropriée;" , commande

class Client:
    def __init__(self):
        """
        Centralise les infos de connexion au serveur pour le jeuGraphique, et les
        échanges client/serveur dont a besoin le jeu (console ou graphique)
        pour être joué en réseau.
        """
        self.connecte = False  # indique si le client est connecte
        self.socket_actif = None
        self.commande = ""  # mémorise la dernière commande lue
        self.donnees = []  # mémorise les dernières données parsées
        self.actif = True  # indique si la thread tourne

    def connexion_serveur(self, hote, port):
        """
        Connexion au serveur de bataille navale (cf. script ``serveur.py``) avec
        renvoie d'un booléen pour indiquer si la connexion a réussi.
        """
        if isinstance(port, str): port = int(port)
        self.socket_actif = connexion_serveur(hote, port)
        # self.socketActif.settimeout( 90 )
        self.connecte = (self.socket_actif != None)
        return self.connecte

    def recuperation_commande_serveur(self):
        """
        Attend la commande envoyée par le serveur, la parse et la mémorise
        dans les attributs commande et donnees.
        """
        cmd = recuperation_commande_serveur(self.socket_actif)
        self.donnees = parseur_commande(cmd) if cmd != None else None
        self.commande = self.donnees[0]

    def deconnexion_serveur(self):
        """
        Déconnexion du serveur.
        """
        deconnexion_serveur(self.socket_actif)
        self.connecte = False

    def repond_au_serveur(self, parametre=None):
        """
        Repond au serveur
        """
        repond_commande_au_serveur(self.socket_actif, self.commande, parametre)

