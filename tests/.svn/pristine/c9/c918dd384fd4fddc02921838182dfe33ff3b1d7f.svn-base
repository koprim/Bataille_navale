"""
Script de tests unitaires de flottes.py
"""

from itertools import chain
from pprint import pprint

import mock
import pytest

import echeance
import utils_tests

try:
    import flottes
except:
    pass


# *********************************************************************************************************
# Tests de la fonction liste_bateaux()
# *********************************************************************************************************
class TestListeBateaux:
    pytestmark = echeance.ECHEANCE2
    pytestfunction = 'flottes.liste_bateaux'

    def test_liste_bateaux(self):
        assert ['contre-torpilleurs', 'croiseur', 'porte-avions', 'sous-marin', 'torpilleur'] == flottes.liste_bateaux()


# *********************************************************************************************************
# Tests de la fonction initialisation_flotte_par_dictionnaire_fixe()
# *********************************************************************************************************

class TestInitialisationFlotteParDictionnaireFixe():
    """
    Tests de la fonction :py:func:`flottes.initialisation_flotte_par_dictionnaire_fixe`
    """
    pytestmark = echeance.ECHEANCE1
    pytestfunction = 'flottes.initialisation_flotte_par_dictionnaire_fixe'

    @pytest.mark.parametrize("nom_flotte", [
        pytest.param("flotte1"),
        pytest.param("flotte2"),
    ])
    def test_initialisation_flotte_par_dictionnaire_fixe_structure(self, nom_flotte):
        """
        Teste le type de la valeur de retour
        """
        r = flottes.initialisation_flotte_par_dictionnaire_fixe(nom_flotte)
        assert isinstance(r, dict) is True
        assert 'bateaux' in r
        assert 'tirs' in r
        assert 'effets' in r
        assert 'pseudo' in r
        assert 'nbreTouche' in r
        assert 'nbreCoule' in r

    @pytest.mark.parametrize("nom_flotte, pseudo", [
        pytest.param("flotte1", "moi", id="flotte1"),
        pytest.param("flotte2", "adversaire", id="flotte2"),
        pytest.param("flotte_bateau_touche", "moi", id="flotte_bateau_touche"),
        pytest.param("flotte_presque_coulee", "moi", id="flotte_presque_coulee"),
    ])
    def test_initialisation_flotte_par_dictionnaire_fixe(self, datadir, nom_flotte, pseudo):
        """
        Teste la valeur renvoyée
        """

        flotte = utils_tests.flotte_lecture(datadir["{nom_flotte}.json".format(nom_flotte=nom_flotte)])
        # Correction de pseudo
        flotte['pseudo'] = pseudo
        assert flottes.initialisation_flotte_par_dictionnaire_fixe(nom_flotte) == flotte


# *********************************************************************************************************
# Tests de la fonction initialisation_flotte_vide()
# *********************************************************************************************************

class TestInitialisationFlotteVide:
    pytestmark = echeance.ECHEANCE5
    pytestfunction = 'flottes.initialisation_flotte_vide'

    def test_initialisation_flotte_vide(self, datadir):
        """
        Teste la valeur renvoyée par :py:func:`flottes.initialisation_flotte_vide`
        """
        flottevide = utils_tests.flotte_lecture(datadir["flotte_vide.json"])
        assert flottes.initialisation_flotte_vide() == flottevide


# *********************************************************************************************************
# Tests de la fonction initialisation_flotte_vide()
# *********************************************************************************************************
class TestRemiseFlotteAVide:
    """
    Tests de la fonction :py:func:`flottes.remise_flotte_a_vide`
    """

    def test_remise_flotte_a_vide_return(self, flotte_random):
        """
        Teste le type de la valeur de retour
        """
        assert flottes.remise_flotte_a_vide(flotte_random) is None

    def test_remise_flotte_a_vide_flotte_random(self, flotte_random, datadir):
        """
        Teste le résultat de la fonction
        """
        flottevide = utils_tests.flotte_lecture(datadir["flotte_vide.json"])
        flottes.remise_flotte_a_vide(flotte_random)
        assert flotte_random == flottevide


# *********************************************************************************************************
# Tests de la fonction positions_bateaux()
# *********************************************************************************************************
class TestPositionsDesBateaux:
    """
    Tests de la fonction :py:func:`flottes.positions_bateaux`
    """
    pytestmark = echeance.ECHEANCE1
    pytestfunction = 'flottes.positions_bateaux'

    @pytest.mark.parametrize("flotte_nom, positions", [
        pytest.param("flotte1",
                     {'F1': 'sous-marin', 'F2': 'sous-marin', 'F3': 'sous-marin', 'J8': 'contre-torpilleurs',
                      'J9': 'contre-torpilleurs', 'E1': 'porte-avions', 'B1': 'porte-avions', 'A1': 'porte-avions',
                      'A3': 'croiseur', 'A5': 'croiseur', 'A4': 'croiseur', 'A6': 'croiseur', 'C1': 'porte-avions',
                      'D1': 'porte-avions', 'D2': 'torpilleur', 'J10': 'contre-torpilleurs', 'E2': 'torpilleur'},
                     id="flotte1"),
        pytest.param("flotte2",
                     {'A1': 'porte-avions', 'E1': 'sous-marin', 'B3': 'croiseur', 'H4': 'torpilleur', 'B4': 'croiseur',
                      'A3': 'porte-avions', 'A2': 'porte-avions', 'A5': 'porte-avions', 'B1': 'croiseur',
                      'B2': 'croiseur', 'H3': 'torpilleur', 'A4': 'porte-avions', 'E2': 'sous-marin',
                      'D2': 'contre-torpilleurs', 'D3': 'contre-torpilleurs', 'E3': 'sous-marin',
                      'D1': 'contre-torpilleurs'}, id="flotte2")
    ])
    def test_positions_des_bateaux(self, datadir, flotte_nom, positions):
        """
        Teste le résultat de la fonction sans exception
        """
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        assert flottes.positions_bateaux(flotte) == positions

    @pytest.mark.parametrize("flotte_nom, positions", [
        pytest.param("flotte1",
                     {'F1': 'sous-marin', 'F2': 'sous-marin', 'F3': 'sous-marin', 'J8': 'contre-torpilleurs',
                      'J9': 'contre-torpilleurs', 'A3': 'croiseur', 'A5': 'croiseur', 'A4': 'croiseur',
                      'A6': 'croiseur', 'D2': 'torpilleur', 'J10': 'contre-torpilleurs', 'E2': 'torpilleur'},
                     id="flotte1"),
        pytest.param("flotte2",
                     {'E1': 'sous-marin', 'B3': 'croiseur', 'H4': 'torpilleur', 'B4': 'croiseur', 'B1': 'croiseur',
                      'B2': 'croiseur', 'H3': 'torpilleur', 'E2': 'sous-marin', 'D2': 'contre-torpilleurs',
                      'D3': 'contre-torpilleurs', 'E3': 'sous-marin', 'D1': 'contre-torpilleurs'}, id="flotte2")
    ])
    def test_positions_des_bateaux_excepte_porte_avions(self, datadir, flotte_nom, positions):
        """
        Teste le résultat de la fonction sans exception
        """
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        assert flottes.positions_bateaux(flotte, excepte="porte-avions") == positions

    @pytest.mark.parametrize("flotte_nom, positions", [
        pytest.param("flotte1",
                     {'J8': 'contre-torpilleurs', 'J9': 'contre-torpilleurs', 'E1': 'porte-avions',
                      'B1': 'porte-avions', 'A1': 'porte-avions', 'A3': 'croiseur', 'A5': 'croiseur', 'A4': 'croiseur',
                      'A6': 'croiseur', 'C1': 'porte-avions', 'D1': 'porte-avions', 'D2': 'torpilleur',
                      'J10': 'contre-torpilleurs', 'E2': 'torpilleur'}, id="flotte1"),
        pytest.param("flotte2",
                     {'A1': 'porte-avions', 'B3': 'croiseur', 'H4': 'torpilleur', 'B4': 'croiseur',
                      'A3': 'porte-avions', 'A2': 'porte-avions', 'A5': 'porte-avions', 'B1': 'croiseur',
                      'B2': 'croiseur', 'H3': 'torpilleur', 'A4': 'porte-avions', 'D2': 'contre-torpilleurs',
                      'D3': 'contre-torpilleurs', 'D1': 'contre-torpilleurs'}, id="flotte2")
    ])
    def test_positions_des_bateaux_excepte_sous_marin(self, datadir, flotte_nom, positions):
        """
        Teste le résultat de la fonction sans exception
        """
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        assert flottes.positions_bateaux(flotte, excepte="sous-marin") == positions


# *********************************************************************************************************
# Tests de la fonction est_bateau_coule()
# *********************************************************************************************************
class TestEstBateauCoule():
    """
    Tests de la fonction :py:func:`flottes.est_bateau_coule`
    """

    pytestmark = echeance.ECHEANCE1
    pytestfunction = 'flottes.est_bateau_coule'

    @pytest.mark.parametrize("bateau", utils_tests.TYPE_BATEAUX)
    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_est_bateau_coule_aucun_tir(self, datadir, flotte_nom, bateau):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        assert flottes.est_bateau_coule(flotte, bateau) is False

    @pytest.mark.parametrize("bateau", utils_tests.TYPE_BATEAUX)
    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_est_bateau_coule_unique(self, datadir, flotte_nom,  bateau):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        flotte_bateau_coule = utils_tests.flotte_bateau_coule(flotte, bateau)
        assert flottes.est_bateau_coule(flotte_bateau_coule, bateau) is True
        for autre_bateau in filter(lambda x: x != bateau, utils_tests.TYPE_BATEAUX):
            assert flottes.est_bateau_coule(flotte_bateau_coule, autre_bateau) is False

    @pytest.mark.parametrize("bateau", utils_tests.TYPE_BATEAUX)
    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_est_bateau_coule_tous(self, datadir, flotte_nom, bateau):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        flotte_coulee = utils_tests.flotte_coulee(flotte)
        assert flottes.est_bateau_coule(flotte_coulee, bateau) is True


# *********************************************************************************************************
# Tests de la fonction est_flotte_coulee()
# *********************************************************************************************************
class TestEstFlotteCoulee():
    """
    Tests de la fonction :py:func:`flottes.est_flotte_coulee`
    """

    pytestmark = echeance.ECHEANCE2
    pytestfunction = 'flottes.est_flotte_coulee'

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_est_flotte_coulee_aucun_tir(self, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        assert flottes.est_flotte_coulee(flotte) is False

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_est_flotte_coulee(self, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        flotte_coulee = utils_tests.flotte_coulee(flotte)
        assert flottes.est_flotte_coulee(flotte_coulee) is True


# *********************************************************************************************************
# Tests de la fonction analyse_tir()
# *********************************************************************************************************
class TestAnalyseTir():
    """
    Tests de la fonction :py:func:`flottes.analyse_tir`
    """

    pytestmark = echeance.ECHEANCE2
    pytestfunction = 'flottes.analyse_tir'

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_analyse_tir_eau(self, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        # Mise à plat des cases occupées par un bateau
        cases_bateaux = list(chain.from_iterable(flotte['bateaux'].values()))
        for case in filter(lambda x: x not in cases_bateaux, utils_tests.CASES_POSSIBLES):
            assert flottes.analyse_tir(flotte, case) == "eau"
            assert flotte['tirs'] == [case]
            assert flotte['effets'] == ["eau"]
            assert flotte['nbreTouche'] == 0
            assert flotte['nbreCoule'] == 0

            # Reset
            utils_tests.remise_a_zero_tirs(flotte)

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_analyse_tir_touche(self, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        # Mise à plat des cases occupées par un bateau
        cases_bateaux = list(chain.from_iterable(flotte['bateaux'].values()))
        for case in cases_bateaux:
            assert flottes.analyse_tir(flotte, case) == "touche"
            assert flotte['tirs'] == [case]
            assert flotte['effets'] == ["touche"]
            assert flotte['nbreTouche'] == 1
            assert flotte['nbreCoule'] == 0

            # Reset
            utils_tests.remise_a_zero_tirs(flotte)

    @pytest.mark.parametrize("bateau", utils_tests.TYPE_BATEAUX)
    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_analyse_tir_coule(self, datadir, flotte_nom, bateau):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        cases_bateau = list(flotte['bateaux'][bateau])
        for case in cases_bateau:
            tirs = [c for c in cases_bateau if c != case]
            flotte['tirs'] = tirs.copy()
            flotte['nbreTouche'] = len(tirs)
            assert flottes.analyse_tir(flotte, case) == "coule"
            assert flotte['tirs'] == tirs + [case]
            assert flotte['effets'] == ["coule"]
            assert flotte['nbreTouche'] == utils_tests.LONGUEURS_BATEAUX[bateau]
            assert flotte['nbreCoule'] == 1

            # Reset
            utils_tests.remise_a_zero_tirs(flotte)


# *********************************************************************************************************
# Tests de la fonction calcul_positions_bateau()
# *********************************************************************************************************
class TestCalculPositionsBateau:
    pytestmark = echeance.ECHEANCE6
    pytestfunction = 'flottes.calcul_positions_bateau'

    @pytest.mark.parametrize("case,direction,longueur,resultat", [
        ("A2", "horizontal", 3, ['A2', 'A3', 'A4']),
        ("B4", "vertical", 5, ['B4', 'C4', 'D4', 'E4', 'F4']),
        ("D8", "horizontal", 4, []),
    ])
    def test_calcul_positions_bateau(self, case, direction, longueur, resultat):
        assert flottes.calcul_positions_bateau(case, direction, longueur) == resultat


# *********************************************************************************************************
# Tests de la fonction longueur_bateau()
# *********************************************************************************************************
class TestLongueurBateau:
    pytestmark = echeance.ECHEANCE5
    pytestfunction = 'flottes.longueur_bateau'

    @pytest.mark.parametrize("bateau,longueur", utils_tests.LONGUEURS_BATEAUX.items())
    def test_longueur_bateau(self, bateau, longueur):
        assert flottes.longueur_bateau(bateau) == longueur


# *********************************************************************************************************
# Tests de la fonction positionne_bateau_par_direction()
# *********************************************************************************************************
class TestPositionneBateauParDirection:
    """
    Tests de la fonction :py:func:`flottes.positionne_bateau_par_direction`
    """

    pytestmark = echeance.ECHEANCE6
    pytestfunction = 'flottes.positionne_bateau_par_direction'

    @pytest.mark.parametrize("bateau", utils_tests.TYPE_BATEAUX)
    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_positionne_bateau_par_direction(self, datadir, flotte_nom, bateau):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        # Pour tester, on positionne le bateau à la même position que celui de la flotte initiale après l'avoir supprimé
        cases = flotte["bateaux"][bateau]
        flotte["bateaux"][bateau] = []
        direction = utils_tests.calcul_direction(cases)
        r = flottes.positionne_bateau_par_direction(flotte, bateau, cases[0], direction)
        assert r is True
        assert cases == flotte["bateaux"][bateau]

    @pytest.mark.parametrize("bateau", utils_tests.TYPE_BATEAUX)
    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_positionne_bateau_par_direction_occupe(self, datadir, flotte_nom, bateau):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        # Récupération des positions des bateaux
        positions = flottes.positions_bateaux(flotte, excepte=bateau)
        longueur_bateau = utils_tests.LONGUEURS_BATEAUX[bateau]
        # Suppression du
        flotte["bateaux"][bateau] = []
        for direction in ["vertical", "horizontal"]:
            for case in positions:
                r = flottes.positionne_bateau_par_direction(flotte, bateau, case, direction)

                assert r is False
                assert flotte["bateaux"][bateau] == []


# *********************************************************************************************************
# Tests de la fonction est_flotte_complete()
# *********************************************************************************************************
class TestEstFlotteComplete:
    """
    Tests de la fonction :py:func:`flottes.est_flotte_complete`
    """

    pytestmark = echeance.ECHEANCE6
    pytestfunction = 'flottes.est_flotte_complete'

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_est_flotte_complete(self, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        assert flottes.est_flotte_complete(flotte) is True

    @pytest.mark.parametrize("bateau", utils_tests.TYPE_BATEAUX)
    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_est_flotte_complete_bateau_manquant(self, datadir, bateau, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        # Suppression du bateau
        flotte["bateaux"][bateau] = []
        assert flottes.est_flotte_complete(flotte) is False

    @pytest.mark.parametrize("bateau", utils_tests.TYPE_BATEAUX)
    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_est_flotte_complete_bateau_incomplet(self,datadir,  bateau, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        # Suppression d'une case du bateau
        flotte["bateaux"][bateau].pop()
        assert flottes.est_flotte_complete(flotte) is False


# *********************************************************************************************************
# Tests de la fonction choix_flotte_aleatoire()
# *********************************************************************************************************
class TestChoixFlotteAleatoire:
    pytestmark = echeance.ECHEANCE6
    pytestfunction = 'flottes.choix_flotte_aleatoire'

    @pytest.mark.parametrize("idx", range(10))
    def test_choix_flotte_aleatoire(self, datadir, idx, flotte_vide):
        """
        Tests de la fonction :py:func:`flottes.choix_flotte_aleatoire`. Ce test execute la vérification pour 10 flottes aléatoires.

        ..note: Attention, ce test utilise la fonction :py:func:`flottes.est_flotte_complete` qui doit donc être fonctionnelle
        """
        print("Execution #%d" % idx)
        flottes.choix_flotte_aleatoire(flotte_vide)
        pprint(flotte_vide)
        assert flottes.est_flotte_complete(flotte_vide) is True

        # Vérification des bateaux
        for bateau, positions in flotte_vide["bateaux"].items():
            # La fonction lève une exception si la direction ne peux pas être calculées
            utils_tests.calcul_direction(positions)


# *********************************************************************************************************
# Tests de la fonction sauvegarde_partie()
# *********************************************************************************************************
class TestSauvegardePartie:
    pytestmark = echeance.ECHEANCE3
    pytestfunction = 'flottes.sauvegarde_partie'

    @pytest.mark.parametrize("flotte1, flotte2, expected", [
        pytest.param("flotte1", "flotte2", "test1.bin", id="test1"),
        pytest.param("flotte2", "flotte1", "test2.bin", id="test2"),
    ])
    def test_sauvegarde_partie(self, change_repertoire_courant_tmpdir, datadir, flotte1, flotte2, expected):
        flotte1 = utils_tests.flotte_lecture(datadir["{flotte1}.json".format(flotte1=flotte1)])
        flotte2 = utils_tests.flotte_lecture(datadir["{flotte2}.json".format(flotte2=flotte2)])

        # Ajout des tirs,
        flottes.sauvegarde_partie(flotte1, flotte2)

        actual_content = change_repertoire_courant_tmpdir.join("sauvegarde.bin").read_binary()
        expected_content = datadir["expected/{expected}".format(expected=expected)].read_binary()
        assert expected_content == actual_content


# *********************************************************************************************************
# Tests de la fonction restauration_partie()
# *********************************************************************************************************
class TestRestaurationPartie:
    """
    Tests de la fonction :py:func:`flottes.restauration_partie`
    """

    pytestmark = echeance.ECHEANCE3
    pytestfunction = 'flottes.restauration_partie'

    @pytest.mark.parametrize("partie, flotte1, flotte2", [
        pytest.param("partie1", "flotte1", "flotte2", id="partie1"),
        pytest.param("partie2", "flotte2", "flotte1", id="partie2"),
    ])
    def test_restauration_partie(self, change_repertoire_courant_tmpdir, datadir, partie, flotte1, flotte2):
        flotte1 = utils_tests.flotte_lecture(datadir["expected/{flotte1}.json".format(flotte1=flotte1)])
        flotte2 = utils_tests.flotte_lecture(datadir["expected/{flotte2}.json".format(flotte2=flotte2)])

        ma_flotte = utils_tests.flotte_vide()
        sa_flotte = utils_tests.flotte_vide()
        datadir[partie].chdir()
        assert flottes.restauration_partie(ma_flotte, sa_flotte) is True

        assert ma_flotte == flotte1
        assert sa_flotte == flotte2

    def test_restauration_partie_fichier_manquant(self, change_repertoire_courant_tmpdir):
        ma_flotte = utils_tests.flotte_vide()
        sa_flotte = utils_tests.flotte_vide()
        assert flottes.restauration_partie(ma_flotte, sa_flotte) is False


# *********************************************************************************************************
# Tests de la fonction memorise_action_tir_sur_flotte_inconnue()
# *********************************************************************************************************
class TestMemoriseActionTirSurFlotteInconnue:
    """
    Tests de la fonction :py:func:`flottes.memorise_action_tir_sur_flotte_inconnue`
    """

    pytestmark = echeance.ECHEANCE6
    pytestfunction = 'flottes.memorise_action_tir_sur_flotte_inconnue'

    @pytest.mark.parametrize("flotte, case, resultat", [
        pytest.param("flotte_vide", "A1", "eau", id="flotte_vide-A1-eau"),
        pytest.param("flotte_vide", "A1", "touche", id="flotte_vide-A1-touche"),
        pytest.param("flotte_vide", "A1", "coule", id="flotte_vide-A1-coule"),
        pytest.param("flotte_vide", "A1", "gagne", id="flotte_vide-A1-gagne"),
        pytest.param("flotte1", "A1", "eau", id="flotte1-A1-eau"),
        pytest.param("flotte1", "A1", "touche", id="flotte1-A1-touche"),
        pytest.param("flotte1", "A1", "coule", id="flotte1-A1-coule"),
        pytest.param("flotte1", "A1", "gagne", id="flotte1-A1-gagne"),
    ])
    def test_memorise_action_tir_sur_flotte_inconnue(self, datadir, flotte, case, resultat):
        expected_flotte = utils_tests.flotte_lecture(datadir["{flotte}-{case}-{resultat}.json".format(flotte=flotte, case=case, resultat=resultat)])
        flotte = utils_tests.flotte_lecture(datadir["{flotte}.json".format(flotte=flotte)])

        flottes.memorise_action_tir_sur_flotte_inconnue(flotte, case, resultat)

        assert flotte == expected_flotte


# *********************************************************************************************************
# Tests de la fonction tir_aleatoire()
# *********************************************************************************************************
class TestTirAleatoire:
    pytestmark = echeance.ECHEANCE4
    pytestfunction = 'flottes.tir_aleatoire'

    @pytest.mark.parametrize("flotte, tirages, expected", [
        pytest.param("flotte_vide", ["B1"], "B1"),
        pytest.param("flotte1", ["B1", "E5"], "E5")
    ])
    def test_tir_aleatoire(self, datadir, flotte, tirages, expected):
        flotte = utils_tests.flotte_lecture(datadir["{flotte}.json".format(flotte=flotte)])
        with mock.patch('outils.case_aleatoire', side_effect=tirages):
            case = flottes.tir_aleatoire(flotte)
        assert expected == case


# *********************************************************************************************************
# Tests de la fonction envoi_flotte_via_serveur()
# *********************************************************************************************************
class TestEnvoiFlotteViaServeur:
    """
    Tests de la fonction :py:func:`flottes.envoi_flotte_via_serveur`
    """
    pytestmark = echeance.ECHEANCE7
    pytestfunction = 'flottes.envoi_flotte_via_serveur'

    @pytest.mark.parametrize("flotte_nom, expected", [
        pytest.param("flotte1",
                     "porte-avions|A1|B1|C1|D1|E1|croiseur|A3|A4|A5|A6|contre-torpilleurs|J8|J9|J10|sous-marin|F1|F2|F3|torpilleur|D2|E2",
                     id="flotte1"),
        pytest.param("flotte2",
                     "porte-avions|A1|A2|A3|A4|A5|croiseur|B1|B2|B3|B4|contre-torpilleurs|D1|D2|D3|sous-marin|E1|E2|E3|torpilleur|H3|H4",
                     id="flotte2")
    ])
    def test_envoi_flotte_via_serveur(self, datadir, flotte_nom, expected):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        assert flottes.envoi_flotte_via_serveur(flotte) == expected


# *********************************************************************************************************
# Tests de la fonction initialisation_flotte_par_commande_du_serveur()
# *********************************************************************************************************
class TestInitialisationFlotteParCommandeDuServeur:
    """
    Tests de la fonction :py:func:`flottes.initialisation_flotte_par_commande_du_serveur`
    """
    pytestmark = echeance.ECHEANCE7
    pytestfunction = 'flottes.initialisation_flotte_par_commande_du_serveur'

    @pytest.mark.parametrize("liste, expected_flotte_nom", [
        pytest.param(["porte-avions", "A1", "B1", "C1", "D1", "E1",
                      "croiseur", "A3", "A4", "A5", "A6",
                      "contre-torpilleurs", "J8", "J9", "J10",
                      "sous-marin", "F1", "F2", "F3",
                      "torpilleur", "D2", "E2"],
                     "flotte1",
                     id="flotte1"),
        pytest.param(["porte-avions", "A1", "A2", "A3", "A4", "A5",
                      "croiseur", "B1", "B2", "B3", "B4",
                      "contre-torpilleurs", "D1", "D2", "D3",
                      "sous-marin", "E1", "E2", "E3",
                      "torpilleur", "H3", "H4"],
                     "flotte2",
                     id="flotte2")
    ])
    def test_initialisation_flotte_par_commande_du_serveur(self, datadir, liste, expected_flotte_nom):
        expected = utils_tests.flotte_lecture(datadir["{expected_flotte_nom}.json".format(expected_flotte_nom=expected_flotte_nom)])
        flotte = flottes.initialisation_flotte_vide()
        flottes.initialisation_flotte_par_commande_du_serveur(flotte, liste)

        assert expected == flotte


class TestNombreBateauxCoules:
    """
    Tests de la fonction :py:func:`flottes.initialisation_flotte_par_commande_du_serveur`
    """
    pytestmark = echeance.ECHEANCE1
    pytestfunction = 'flottes.nombre_bateaux_coules'

    @pytest.mark.parametrize("flotte_nom, expected", [
        pytest.param("flotte_vide", 0, id="flotte_vide"),
        pytest.param("flotte1", 1, id="flotte1"),
        pytest.param("flotte2", 2, id="flotte2"),
        pytest.param("flotte3", 5, id="flotte3"),
    ])
    def test_nombre_bateaux_coules(self, datadir, flotte_nom, expected):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])

        assert expected == flottes.nombre_bateaux_coules(flotte)


class TestNombreTirsTouchantFlotte:
    """
    Tests de la fonction :py:func:`flottes.initialisation_flotte_par_commande_du_serveur`
    """
    pytestmark = echeance.ECHEANCE1
    pytestfunction = 'flottes.nombre_tirs_touchant_flotte'

    @pytest.mark.parametrize("flotte_nom, expected", [
        pytest.param("flotte_vide", 0, id="flotte_vide"),
        pytest.param("flotte1", 4, id="flotte1"),
        pytest.param("flotte2", 1, id="flotte2"),
    ])
    def test_nombre_tirs_touchant_flotte(self, datadir, flotte_nom, expected):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])

        assert expected == flottes.nombre_tirs_touchant_flotte(flotte)
