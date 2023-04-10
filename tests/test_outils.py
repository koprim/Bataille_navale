"""
Script de tests unitaires de outils.py
"""

import pytest

import echeance

try:
    import outils
except:
    pass


# *********************************************************************************************************
# Tests de la fonction est_case_valide()
# *********************************************************************************************************
class TestEstCaseValide:
    pytestmark = echeance.ECHEANCE2
    pytestfunction = 'outils.est_case_valide'

    def test_est_case_valide(self):
        """
        Teste la valeur renvoyée par :py:func:`outils.est_case_valide`
        """
        assert outils.est_case_valide("A4") is True
        assert outils.est_case_valide("a3") is False
        assert outils.est_case_valide("L9") is False
        assert outils.est_case_valide("B12") is False


class TestEstCaseValideErreur:
    pytestmark = echeance.ECHEANCE4
    pytestfunction = 'outils.est_case_valide'

    def test_est_case_erreur(self):
        """
        Teste la valeur renvoyée par :py:func:`outils.est_case_valide`
        """

        assert outils.est_case_valide("stop") is False


# *********************************************************************************************************
# Tests de la fonction case_ln_vers_indices()
# *********************************************************************************************************
class TestCaseLnVersIndices():
    """
    Tests de la fonction :py:func:`outils.case_ln_vers_indices`
    """

    def test_case_ln_vers_indices_return(self):
        """
        Teste le type de la valeur de retour
        """
        r = outils.case_ln_vers_indices("A1")
        assert isinstance(r, list) is True
        assert len(r) == 2

    def test_case_ln_vers_indices_saisie_valide(self):
        """
        Teste la valeur renvoyée lorsque la saisie est valide
        """
        assert outils.case_ln_vers_indices("A1") == [0, 0]
        assert outils.case_ln_vers_indices("B10") == [1, 9]


# *********************************************************************************************************
# Tests de la fonction indices_vers_case_ln()
# *********************************************************************************************************
class TestIndicesVersCaseLn():
    """
    Tests de la fonction :py:func:`outils.indices_vers_case_ln`
    """
    pytestmark = echeance.ECHEANCE2
    pytestfunction = 'outils.indices_vers_case_ln'

    def test_indices_vers_case_ln_return(self):
        """
        Teste le type de la valeur de retour
        """
        r = outils.indices_vers_case_ln([0, 0])
        assert isinstance(r, str) is True

    def test_indices_vers_case_ln_saisie_valide(self):
        """
        Teste la valeur renvoyée lorsque la saisie est valide
        """
        assert outils.indices_vers_case_ln([0, 0]) == "A1"
        assert outils.indices_vers_case_ln([1, 9]) == "B10"


# *********************************************************************************************************
# Tests de la fonction case_aleatoire()
# *********************************************************************************************************
class TestCaseAleatoire:
    pytestmark = echeance.ECHEANCE3
    pytestfunction = 'outils.case_aleatoire'

    def test_case_aleatoire(self, cases_possibles):
        """
        Teste la valeur renvoyée par :py:func:`outils.case_aleatoire`
        """
        assert outils.case_aleatoire() in cases_possibles


class TestJoueurAleatoire:
    pytestmark = echeance.ECHEANCE3
    pytestfunction = 'outils.joueur_aleatoire'

    def test_joueur_aleatoire(self):
        """
        Teste la valeur renvoyée par :py:func:`outils.joueur_aleatoire`
        """
        assert outils.joueur_aleatoire() in ["moi", "adversaire"]


# *********************************************************************************************************
# Tests de la fonction affichage_statistiques_joueurs()
# *********************************************************************************************************
class TestAffichageStatistiquesJoueurs():
    """
    Tests de la fonction :py:func:`outils.affichage_statistiques_joueurs`
    """

    pytestmark = echeance.ECHEANCE5
    pytestfunction = 'outils.affichage_statistiques_joueurs'

    def test_affichage_statistiques_joueurs_inexistant(self, change_repertoire_courant_datadir):
        assert outils.affichage_statistiques_joueurs() == ""

    def test_affichage_statistiques_joueurs_existant1(self, change_repertoire_courant_datadir):
        assert outils.affichage_statistiques_joueurs() == """+-----------+----------------+-----------+----------+----------+
| Joueurs   | Parties jouées | Victoires | Défaites | Abandons |
+===========+================+===========+==========+==========+
| anonymous | 31             | 0         | 0        | 31       |
+-----------+----------------+-----------+----------+----------+
| ordi      | 17             | 0         | 1        | 16       |
+-----------+----------------+-----------+----------+----------+
| moi       | 2              | 0         | 0        | 2        |
+-----------+----------------+-----------+----------+----------+
"""

    def test_affichage_statistiques_joueurs_existant2(self, change_repertoire_courant_datadir):
        assert outils.affichage_statistiques_joueurs() == """+---------+----------------+-----------+----------+----------+
| Joueurs | Parties jouées | Victoires | Défaites | Abandons |
+=========+================+===========+==========+==========+
| ordi    | 17             | 0         | 1        | 16       |
+---------+----------------+-----------+----------+----------+
| moi     | 2              | 0         | 0        | 2        |
+---------+----------------+-----------+----------+----------+
| toto    | 1              | 1         | 0        | 0        |
+---------+----------------+-----------+----------+----------+
"""

    def test_affichage_statistiques_joueurs_vide(self, change_repertoire_courant_datadir):
        assert outils.affichage_statistiques_joueurs() == """+---------+----------------+-----------+----------+----------+
| Joueurs | Parties jouées | Victoires | Défaites | Abandons |
+=========+================+===========+==========+==========+
"""


# *********************************************************************************************************
# Tests de la fonction ajoute_statistiques_joueur()
# *********************************************************************************************************
class TestAjouteStatistiquesJoueur():
    """
    Tests de la fonction :py:func:`outils.ajoute_statistiques_joueur`
    """
    pytestmark = echeance.ECHEANCE5
    pytestfunction = 'outils.ajoute_statistiques_joueur'

    @pytest.mark.parametrize("resultat,contenu", [
        pytest.param("gagne", "toto;1;1;0\n", id="gagne"),
        pytest.param("perd", "toto;1;0;1\n", id="perd"),
        pytest.param("abandonne", "toto;1;0;0\n", id="abandonne")
    ])
    def test_ajoute_statistiques_joueur_inexistant(self, change_repertoire_courant_datadir_copy, resultat, contenu):
        outils.ajoute_statistiques_joueur("toto", resultat)

        f = change_repertoire_courant_datadir_copy.join("statistiques.txt")
        assert f.read() == contenu

    @pytest.mark.parametrize("resultat,contenu", [
        pytest.param("gagne", "toto;1;1;0\n", id="gagne"),
        pytest.param("perd", "toto;1;0;1\n", id="perd"),
        pytest.param("abandonne", "toto;1;0;0\n", id="abandonne")
    ])
    def test_ajoute_statistiques_joueur_nouveau(self, change_repertoire_courant_datadir_copy, resultat, contenu):
        outils.ajoute_statistiques_joueur("toto", resultat)

        f = change_repertoire_courant_datadir_copy.join("statistiques.txt")
        assert f.read() == "ordi;17;0;1\nmoi;2;0;0\n" + contenu

    @pytest.mark.parametrize("resultat,contenu", [
        pytest.param("gagne", "ordi;18;2;1\nmoi;2;0;0\n", id="gagne"),
        pytest.param("perd", "ordi;18;1;2\nmoi;2;0;0\n", id="perd"),
        pytest.param("abandonne", "ordi;18;1;1\nmoi;2;0;0\n", id="abandonne")
    ])
    def test_ajoute_statistiques_joueur_existant(self, change_repertoire_courant_datadir_copy, resultat, contenu):
        outils.ajoute_statistiques_joueur("ordi", resultat)

        f = change_repertoire_courant_datadir_copy.join("statistiques.txt")
        assert f.read() == contenu
