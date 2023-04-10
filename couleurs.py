"""
.. _SequencesANSI:


Résumé du module couleurs.py
----------------------------

.. topic:: Affichage en couleur sur le terminal

    Pour afficher en couleur sur le terminal, on utilise des
    `séquences d'échappement ANSI <https://en.wikipedia.org/wiki/ANSI_escape_code>`_.

    Une séquence d'échappement commence par le caractère non imprimable ``ESC``
    (caractère ASCII de valeur décimale 27, hexadécimale 0x1b, octale 033) et se poursuit
    par un nombre variable de caractères. L'effet produit peut être le changement de la
    couleur des caractères, le déplacement du curseur ou encore l'effacement de l'écran.
    Par exemple::

        print '\\033[31m' + 'ce texte est rouge'
        print '\\033[0m'       # et retour à la couleur de caractère et à la couleur de fond par défaut

    Voici quelques séquences ANSI pour les couleurs :

    =================  ======================     ===============          ========
    Séquence ANSI      Couleur des caractères     Séquence ANSI            Couleur du fond
    =================  ======================     ===============          ========
    ``'\\033[30m'``     noir                       ``'\\033[40m'``           fond noir
    ``'\\033[31m'``     rouge                      ``'\\033[41m'``           fond rouge
    ``'\\033[32m'``     vert                       ``'\\033[42m'``           fond vert
    ``'\\033[33m'``     jaune                      ``'\\033[43m'``           fond jaune
    ``'\\033[34m'``     bleu                       ``'\\033[44m'``           fond bleu
    ``'\\033[35m'``     magenta                    ``'\\033[45m'``           fond magenta
    ``'\\033[36m'``     cyan                       ``'\\033[46m'``           fond cyan
    ``'\\033[37m'``     blanc                      ``'\\033[47m'``           fond blanc
    ``'\\033[38m'``     noir                       ``'\\033[48m'``           fond noir
    ``'\\033[39m'``     couleur par défaut         ``'\\033[49m'``           fond par défaut
    =================  ======================     ===============          ========

    et quelques autres utiles :

    =========================     ======================================================
    Séquence ANSI                 Effet
    =========================     ======================================================
    ``'\\033[2J\\033[1;1H'``        efface l'écran et positionne le curseur en (1,1)
    ``'\\033[0m'``                 *reset* couleur
    ``'\\033[1m``                  couleur des caractères de forte intensité
    ``'\\033[2m``                  couleur des caractères de faible intensité
    =========================     ======================================================

    .. note:: On peut faire plusieurs actions dans la même séquence ANSI
        (couleur blanche + fond rouge + forte intensité):

        .. code-block:: python

            print '\\033[37;41;1mTexte en blanc brillant sur rouge\\033[0m'

    .. note:: Support des séquences ANSI sous Windows

        Les séquences d'échappement ANSI sont interprétées nativement par les consoles Unix et MacOS,
        mais pas par la console Windows. Sous Windows, le module
        `colorama <https://pypi.python.org/pypi/colorama>`_
        permet de traduire les séquences ANSI en appels systèmes Win32.
        Pour activer ``colorama``, il suffit d'ajouter les instructions :
        ::

            import colorama
            colorama.init()

        Une alternative pour interpréter les séquences ANSI sous Windows consiste à
        exécuter le programme python dans `ansicon.exe <http://adoxa.altervista.org/ansicon/index.html>`_
        en remplacement de la console standard ``cmd.exe``


.. seealso:: :mod:`outils`, :mod:`terminal`, `colorama <https://pypi.python.org/pypi/colorama>`_
"""

import os

if os.name == 'nt':  # pragma: no cover
    try:
        import colorama

        colorama.init()
        AVEC_COLORAMA = True
    except:
        AVEC_COLORAMA = False
else:
    AVEC_COLORAMA = False

if AVEC_COLORAMA:  # pragma: no cover
    COULEURS = {'rouge': colorama.Fore.RED,
                'fond_rouge': colorama.Fore.WHITE + colorama.Back.RED + colorama.Style.BRIGHT,
                'bleu': colorama.Fore.BLUE,
                'fond_bleu': colorama.Fore.WHITE + colorama.Back.BLUE + colorama.Style.BRIGHT,
                'magenta': colorama.Fore.MAGENTA,
                'fond_magenta': colorama.Fore.WHITE + colorama.Back.MAGENTA + colorama.Style.BRIGHT,
                'vert': colorama.Fore.GREEN,
                'fond_vert': colorama.Fore.WHITE + colorama.Back.GREEN + colorama.Style.BRIGHT,
                'jaune': colorama.Fore.YELLOW,
                'fond_jaune': colorama.Fore.BLACK + colorama.Back.YELLOW + colorama.Style.BRIGHT,
                'cyan': colorama.Fore.CYAN,
                'fond_cyan': colorama.Fore.WHITE + colorama.Back.CYAN + colorama.Style.BRIGHT,
                'blanc': "\033[0m"}
else:
    COULEURS = {'rouge': '\033[31m', 'fond_rouge': '\033[41m',
                'bleu': '\033[34m', 'fond_bleu': '\033[44m',
                'magenta': '\033[35m', 'fond_magenta': '\033[45m',
                'vert': '\033[32m', 'fond_vert': '\033[42m',
                'jaune': '\033[33m', 'fond_jaune': '\033[43m',
                'cyan': '\033[36m', 'fond_cyan': '\033[36m',
                'blanc': '\033[37m'}
