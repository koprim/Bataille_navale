"""
Script définissant les flottes de test et des informations utiles
"""

import itertools
import json
import random
import re
import string
from itertools import chain

import couleurs

LONGUEURS_BATEAUX = {'porte-avions': 5, 'croiseur': 4, 'contre-torpilleurs': 3, 'sous-marin': 3,
                     'torpilleur': 2}
NOMBRE_CASES_BATEAUX = sum(LONGUEURS_BATEAUX.values())

TYPE_BATEAUX = list(LONGUEURS_BATEAUX.keys())

CASES_POSSIBLES = ["%s%d" % (x[0], x[1]) for x in itertools.product(string.ascii_uppercase[0:10], range(1, 11))]

if couleurs.AVEC_COLORAMA:  # pragma: no cover
    __PATTERN_COLOR = re.compile(r"\033\[3\d*m")
else:
    __PATTERN_COLOR = re.compile(r"\033\[([34][0-9])m")


def flotte_lecture(file):
    """
    Lecture d'une flotte depuis un fichier json

    :param file:
    :return: la flotte
    :rtype: dict
    """
    if isinstance(file, str):
        with open(file) as fh:
            return json.load(fh)
    else:
        return json.load(file.open("rb"))


def flotte_vide():
    return {'bateaux': {'contre-torpilleurs': [],
                        'croiseur': [],
                        'porte-avions': [],
                        'sous-marin': [],
                        'torpilleur': []},
            'tirs': [],
            'effets': [],
            'pseudo': 'anonymous',
            'nbreTouche': 0,
            'nbreCoule': 0
            }


def flotte_random():
    return {'bateaux': {bateau: [CASES_POSSIBLES for i in range(taille)] for bateau, taille in
                        LONGUEURS_BATEAUX.items()},
            'tirs': [],
            'effets': [],
            'pseudo': 'anonymous',
            'nbreTouche': random.randint(0, NOMBRE_CASES_BATEAUX),
            'nbreCoule': random.randint(0, 5)
            }


def flotte_coulee(flotte):
    """
    Coule toute la flotte

    :param flotte: la flotte
    :type flotte: dir
    :return: la flotte modifiée
    :rtype: dict
    """
    # Mise à plat des cases occupées par le bateau et mélange
    cases_bateaux = list(chain.from_iterable(flotte['bateaux'].values()))
    random.shuffle(cases_bateaux)

    # Mise en place des tirs correspondant au cases des bateaux
    flotte = flotte.copy()
    flotte['tirs'] = cases_bateaux
    return flotte


def flotte_bateau_coule(flotte, bateau):
    """
    Coule un bateau de la flotte

    :param flotte: la flotte
    :type flotte: dir
    :param bateau: un nom de bateau
    :return: la flotte modifiée
    :rtype: dict
    """
    # Mise à plat des cases occupées par le bateau et mélange
    cases_bateaux = list(flotte['bateaux'][bateau])
    random.shuffle(cases_bateaux)

    # Mise en place des tirs correspondant au cases du bateau
    flotte = flotte.copy()
    flotte['tirs'] = cases_bateaux
    return flotte


def remise_a_zero_tirs(flotte):
    """
    Remise à zero des tirs sur la flotte.

    :param flotte: la flotte
    """
    flotte['tirs'] = []
    flotte['effets'] = []
    flotte['nbreTouche'] = 0
    flotte['nbreCoule'] = 0


def calcul_direction(positions):
    """
    Calcule la direction du bateau, à partir de la position. On suppose que les positions sont valides

    :param positions: la liste des positions
    :return: la direction `"horizontal"`` ou ``"vertical"``
    """
    if len(positions) == 0:
        raise Exception("Aucune position")

    L = [p[0] for p in positions]
    n = ["0" if p[1:] == "10" else p[1:] for p in positions]
    if L.count(L[0]) == len(positions) and "".join(n) in string.digits[1:] + "0":
        return "horizontal"
    elif n.count(n[0]) == len(positions) and "".join(L) in string.ascii_uppercase:
        return "vertical"

    raise Exception("Positions incorrectes: %s" % positions)


def suppression_couleurs(content):
    """
    Retourne le contenu en ayant supprimé les informations de couleur

    :param content: le contenu à traiter
    :type content: str
    :return: le même contenu sans les couleurs
    :rtype: str
    """
    if couleurs.AVEC_COLORAMA:
        res = content
        for c in couleurs.COULEURS.values():
            res = res.replace(str(c), "")
    else:
        res = __PATTERN_COLOR.sub(r"", content)
    return res


def __find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


def compte_couleurs(content):
    """

    :param content:
    :return:
    """
    if couleurs.AVEC_COLORAMA:
        res = 0
        for c in couleurs.COULEURS.values():
            res += len(list(__find_all(content, str(c))))
    else:
        res = len(__PATTERN_COLOR.findall(content))
    return res


def flotte_read_flotte2d(file, suppression_couleurs=False):
    """
    Lecture de la flotte 2D depuis un fichier avec traduction des couleurs
    :param file: le fichier à lire
    :type file: str
    :param suppression_couleurs: True pour supprimer les couleurs à la lecture du fichier
    :type suppression_couleurs: bool
    :return: le contenu
    :rtype: str
    """
    with open(str(file), encoding="UTF-8") as fd:
        content = fd.read()

    # \033[31
    if suppression_couleurs:
        return re.sub(r"\\033\[([34][0-9])m", r"", content)
    else:
        return re.sub(r"\\033\[([34][0-9])m", r"\033[\1m", content)


def corrige_fin_lignes(text):
    """
    Correction de la fin des lignes du texte pour être au format Linux (cad LF)

    :param text: le texte à corriger
    :type text: str
    :return: le texte corrigé
    :rtype: str
    """
    return "\n".join(text.splitlines())


if __name__ == '__main__':
    flotte = flotte_lecture("data/flotte1.json")
    cases_bateaux = list(chain.from_iterable(flotte['bateaux'].values()))
    random.shuffle(cases_bateaux)

    # cases_bateaux = [ random.choice(CASES_POSSIBLES) for i in range(17) ]
    print(json.dumps(cases_bateaux))
