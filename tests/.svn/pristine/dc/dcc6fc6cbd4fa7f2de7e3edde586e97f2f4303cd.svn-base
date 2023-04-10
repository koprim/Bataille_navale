"""
Script de tests unitaires de terminal.py
"""

import itertools

import mock
import pytest

import echeance
import utils_tests

try:
    import terminal
except:
    pass


# *********************************************************************************************************
# Tests de la fonction :py:func:`terminal.affiche_flotte_textuelle`
# *********************************************************************************************************
class TestAfficheFlotteTextuelle:
    pytestmark = echeance.ECHEANCE1
    pytestfunction = 'terminal.affiche_flotte_textuelle'

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_affiche_flotte_textuelle(self, datadir, capsys, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        expected = datadir["{flotte_nom}.txt".format(flotte_nom=flotte_nom)].read()
        terminal.affiche_flotte_textuelle(flotte)
        out, err = capsys.readouterr()
        assert out == expected


# *********************************************************************************************************
# Tests de la fonction affiche_flotte_2d_couleurs()
# *********************************************************************************************************
class TestAfficheFlotte2dCouleurs():
    """
    Tests de la fonction :py:func:`terminal.affiche_flotte_2d_couleurs`
    """
    pytestmark = echeance.ECHEANCE4
    pytestfunction = 'terminal.affiche_flotte_2d_couleurs'

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_affiche_flotte_2d_couleurs(self, capsys, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        terminal.affiche_flotte_2d_couleurs(flotte)
        out, err = capsys.readouterr()
        colors = utils_tests.compte_couleurs(out)
        assert utils_tests.NOMBRE_CASES_BATEAUX * 2 == colors  # Des couleurs sont-elles présentes ?

        expected_content = utils_tests.flotte_read_flotte2d(datadir["{flotte_nom}.txt".format(flotte_nom=flotte_nom)])
        assert expected_content == utils_tests.suppression_couleurs(out)

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_affiche_flotte_2d_couleurs_tirs(self, capsys, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        terminal.affiche_flotte_2d_couleurs(flotte)
        out, err = capsys.readouterr()
        colors = utils_tests.compte_couleurs(out)
        assert utils_tests.NOMBRE_CASES_BATEAUX * 2 == colors  # Des couleurs sont-elles présentes ?

        expected_content = utils_tests.flotte_read_flotte2d(datadir["{flotte_nom}.txt".format(flotte_nom=flotte_nom)])
        out = utils_tests.suppression_couleurs(out)
        assert expected_content == out

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_affiche_flotte_2d_couleurs_cachee(self, capsys, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        terminal.affiche_flotte_2d_couleurs(flotte, cachee=True)
        out, err = capsys.readouterr()

        expected_content = utils_tests.flotte_read_flotte2d(datadir["flotte_vide.txt"])
        assert expected_content == utils_tests.suppression_couleurs(out)

    @pytest.mark.parametrize("flotte_nom, expected_colors", [
        pytest.param("flotte1", 8, id="flotte1"),
        pytest.param("flotte2", utils_tests.NOMBRE_CASES_BATEAUX * 2, id="flotte2")
    ])
    def test_affiche_flotte_2d_couleurs_tirs_cachee(self, capsys, datadir, flotte_nom, expected_colors):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        terminal.affiche_flotte_2d_couleurs(flotte, cachee=True)
        out, err = capsys.readouterr()
        colors = utils_tests.compte_couleurs(out)
        assert expected_colors == colors  # Des couleurs sont-elles présentes ?

        expected_content = utils_tests.flotte_read_flotte2d(datadir["{flotte_nom}.txt".format(flotte_nom=flotte_nom)])
        out = utils_tests.suppression_couleurs(out)
        assert expected_content == out


# *********************************************************************************************************
# Tests de la fonction affiche_flotte_2d()
# *********************************************************************************************************
class TestAfficheFlotte2d():
    """
    Tests de la fonction :py:func:`terminal.affiche_flotte_2d`
    """
    pytestmark = echeance.ECHEANCE2
    pytestfunction = 'flottes.affiche_flotte_2d'

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_affiche_flotte_2d(self, capsys, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        terminal.affiche_flotte_2d(flotte)
        out, err = capsys.readouterr()

        expected_content = utils_tests.flotte_read_flotte2d(datadir["{flotte_nom}.txt".format(flotte_nom=flotte_nom)])
        assert expected_content == out

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_affiche_flotte_2d_tirs(self, capsys, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        terminal.affiche_flotte_2d(flotte)
        out, err = capsys.readouterr()

        expected_content = utils_tests.flotte_read_flotte2d(datadir["{flotte_nom}.txt".format(flotte_nom=flotte_nom)])
        assert expected_content == out

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_affiche_flotte_2d_cachee(self, capsys, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        terminal.affiche_flotte_2d(flotte, cachee=True)
        out, err = capsys.readouterr()

        expected_content = utils_tests.flotte_read_flotte2d(datadir["flotte_vide.txt"])
        assert expected_content == out

    @pytest.mark.parametrize("flotte_nom, expected_colors", [
        pytest.param("flotte1", 8, id="flotte1"),
        pytest.param("flotte2", utils_tests.NOMBRE_CASES_BATEAUX * 2, id="flotte2")
    ])
    def test_affiche_flotte_2d_tirs_cachee(self, capsys, datadir, flotte_nom, expected_colors):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        terminal.affiche_flotte_2d(flotte, cachee=True)
        out, err = capsys.readouterr()

        expected_content = utils_tests.flotte_read_flotte2d(datadir["{flotte_nom}.txt".format(flotte_nom=flotte_nom)])
        assert expected_content == out


# *********************************************************************************************************
# Tests de la fonction affiche_flotte_inconnue_2d()
# *********************************************************************************************************
class TestAfficheFlotteInconnue2d:
    pytestmark = echeance.ECHEANCE6
    pytestfunction = 'terminal.affiche_flotte_inconnue_2d'

    @pytest.mark.parametrize("flotte_nom", ["flotte1", "flotte2"])
    def test_affiche_flotte_inconnue_2d(self, capsys, datadir, flotte_nom):
        flotte = utils_tests.flotte_lecture(datadir["{flotte_nom}.json".format(flotte_nom=flotte_nom)])
        terminal.affiche_flotte_inconnue_2d(flotte)
        out, err = capsys.readouterr()

        expected_content = utils_tests.flotte_read_flotte2d(datadir["{flotte_nom}.txt".format(flotte_nom=flotte_nom)])
        out = utils_tests.suppression_couleurs(out)
        assert expected_content == out


# *********************************************************************************************************
# Tests de la fonction saisie_pseudo()
# *********************************************************************************************************
class TestSaisiePseudo:
    pytestmark = echeance.ECHEANCE9
    pytestfunction = 'terminal.saisie_pseudo'

    def test_saisie_pseudo(self):
        with mock.patch("builtins.input", return_value="foobar"):
            res = terminal.saisie_pseudo()

        assert "foobar" == res

    def test_saisie_pseudo_vide(self):
        with mock.patch("builtins.input", side_effect=["", "", "foobar"]):
            res = terminal.saisie_pseudo()

        assert "foobar" == res


# *********************************************************************************************************
# Tests de la fonction saisie_adresse_reseau()
# *********************************************************************************************************
class TestSaisieAdresseReseau:
    pytestmark = echeance.ECHEANCE8
    pytestfunction = 'terminal.saisie_adresse_reseau'

    @pytest.mark.parametrize("saisies", [
        ["localhost:12800"],
        ["localhost", "localhost:12800"],
        ["localhost:test", "localhost:12800"],
        [":12800", "localhost:12800"],
    ])
    def test_saisie_adresse_reseau(self, saisies):
        with mock.patch("builtins.input", side_effect=saisies):
            res = terminal.saisie_adresse_reseau()

        assert ["localhost", 12800] == res


# *********************************************************************************************************
# Tests de la fonction saisie_mode_initialisation_flottes()
# *********************************************************************************************************
class TestSaisieModeInitialisationFlottes:
    """
    Tests de la fonction :py:func:`terminal.saisie_mode_initialisation_flottes`
    """
    pytestmark = echeance.ECHEANCE8
    pytestfunction = 'terminal.saisie_mode_initialisation_flottes'

    @pytest.mark.parametrize("saisies, expected", [
        ("1", "endur"),
        ("2", "manuel"),
        ("3", "manuel+aleatoire"),
        ("4", "aleatoires"),
        ("5", "restaurees")
    ])
    def test_saisie_mode_initialisation_flottes(self, capsys, saisies, expected):
        with mock.patch('builtins.input', side_effect=saisies):
            r = terminal.saisie_mode_initialisation_flottes()

        out, err = capsys.readouterr()

        assert """
Mode de choix de la flotte :
----------------------------
 1> flottes initialisées en dur
 2> flotte du joueur initialisée manuellement et flotte de l'adversaire vide
 3> flotte du joueur initialisée manuellement et flotte de l'adversaire aléatoirement
 4> flottes initialisées aléatoirement (defaut)
 5> flottes restaurées de la dernière partie sauvegardée

""" == out
        assert expected == r

    def test_saisie_mode_initialisation_flottes_erreur(self, capsys):
        saisies = ['k', '6', 'yeah', '1']

        with mock.patch('builtins.input', side_effect=saisies):
            r = terminal.saisie_mode_initialisation_flottes()

        out, err = capsys.readouterr()

        assert """
Mode de choix de la flotte :
----------------------------
 1> flottes initialisées en dur
 2> flotte du joueur initialisée manuellement et flotte de l'adversaire vide
 3> flotte du joueur initialisée manuellement et flotte de l'adversaire aléatoirement
 4> flottes initialisées aléatoirement (defaut)
 5> flottes restaurées de la dernière partie sauvegardée

""" * 4 == out
        assert "endur" == r


# *********************************************************************************************************
# Tests de la fonction saisie_mode_choix_jeu()
# *********************************************************************************************************
class TestSaisieModeChoixJeu:
    """
    Tests de la fonction :py:func:`terminal.saisie_mode_choix_jeu`
    """
    pytestmark = echeance.ECHEANCE9
    pytestfunction = 'terminal.saisie_mode_choix_jeu'

    @pytest.mark.parametrize("saisies, expected", [
        ("1", "manuel"),
        ("2", "auto"),
        ("3", "ia"),
        ("4", "reseau")
    ])
    def test_saisie_mode_choix_jeu(self, capsys, saisies, expected):
        with mock.patch('builtins.input', side_effect=saisies):
            r = terminal.saisie_mode_choix_jeu()
        out, err = capsys.readouterr()

        assert """
Mode de choix du jeu :
----------------------
 1> jeu entièrement manuel [utile pour le debug] (choix par defaut)
 2> jeu automatique contre l'ordinateur
 3> jeu automatique avancé contre l'ordinateur (tir avec IA)
 4> jeu en réseau

""" == out
        assert expected == r

    def test_saisie_mode_choix_jeu_erreur(self, capsys):
        saisies = ['k', '5', 'yeah', '1']

        with mock.patch('builtins.input', side_effect=saisies):
            r = terminal.saisie_mode_choix_jeu()

        out, err = capsys.readouterr()

        assert """
Mode de choix du jeu :
----------------------
 1> jeu entièrement manuel [utile pour le debug] (choix par defaut)
 2> jeu automatique contre l'ordinateur
 3> jeu automatique avancé contre l'ordinateur (tir avec IA)
 4> jeu en réseau

""" * 4 == out
        assert "manuel" == r


# *********************************************************************************************************
# Tests de la fonction saisie_cible_valide_ou_commande()
# *********************************************************************************************************
class TestSaisieCibleValideOuCommande:
    """
    Tests de la fonction :py:func:`terminal.saisie_cible_valide_ou_commande`
    """
    pytestmark = echeance.ECHEANCE4
    pytestfunction = 'terminal.saisie_cible_valide_ou_commande'

    @pytest.mark.parametrize("commandes, saisie", [
        pytest.param(["stop"], "A1", id="stop/A1"),
        pytest.param(["stop"], "stop", id="stop/stop"),
        pytest.param(["stop", "sauv"], "A1", id="stop+sauv/A1"),
        pytest.param(["stop", "sauv"], "stop", id="stop+sauv/stop"),
        pytest.param(["stop", "sauv"], "sauv", id="stop+sauv/sauv"),
    ])
    def test_saisie_cible_valide_ou_commande(self, saisie, commandes):
        with mock.patch('builtins.input', return_value=saisie):
            r = terminal.saisie_cible_valide_ou_commande(commandes)

        assert saisie == r

    # @pytest.mark.parametrize("commandes", [["stop"], ["stop", "sauv"]])
    # @pytest.mark.parametrize("saisies", [["Z1", "A1"], ["toto" "A1"]])
    @pytest.mark.parametrize("commandes, saisies", [
        pytest.param(["stop"], ["Z1", "A1"], id="stop/Z1-A1"),
        pytest.param(["stop", "sauv"], ["Z1", "A1"], id="stop+sauv/Z1-A1"),
        pytest.param(["stop"], ["toto", "A1"], id="stop/toto-A1"),
        pytest.param(["stop", "sauv"], ["toto", "A1"], id="stop+sauv/toto-A1"),
    ])
    def test_saisie_cible_valide_ou_commande_erreur(self, saisies, commandes):
        with mock.patch('builtins.input', side_effect=saisies):
            r = terminal.saisie_cible_valide_ou_commande(commandes)

        assert "A1" == r


# *********************************************************************************************************
# Tests de la fonction saisie_direction_valide()
# *********************************************************************************************************
class TestSaisieDirectionValide:
    """
    Tests de la fonction :py:func:`terminal.saisie_direction_valide`
    """
    pytestmark = echeance.ECHEANCE6
    pytestfunction = 'terminal.saisie_direction_valide'

    @pytest.mark.parametrize("saisies, expected", [
        ("h", "horizontal"),
        ("horizontal", "horizontal"),
        ("v", "vertical"),
        ("vertical", "vertical")
    ])
    def test_saisie_direction_valide(self, saisies, expected):
        with mock.patch('builtins.input', return_value=saisies):
            r = terminal.saisie_direction_valide()

        assert expected == r

    def test_saisie_mode_choix_jeu_erreur(self, mock):
        saisies = ['k', '5', 'yeah', 'h']

        with mock.patch('builtins.input', side_effect=saisies):
            r = terminal.saisie_direction_valide()

        assert "horizontal" == r


# *********************************************************************************************************
# Tests de la fonction choix_bateau_a_positionner()
# *********************************************************************************************************
class TestChoixBateauAPositionner:
    """
    Tests de la fonction :py:func:`terminal.choix_bateau_a_positionner`
    """
    pytestmark = echeance.ECHEANCE6
    pytestfunction = 'terminal.choix_bateau_a_positionner'

    @pytest.mark.parametrize("saisies, expected", [
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("stop", "stop")
    ])
    def test_choix_bateau_a_positionner(self, datadir, capsys, saisies, expected):
        flotte = utils_tests.flotte_lecture(datadir["flotte1.json"])
        with mock.patch('builtins.input', return_value=saisies):
            r = terminal.choix_bateau_a_positionner(flotte)
        out, err = capsys.readouterr()

        expected_out = """Choisir le bateau à (re)positionner parmi :
   1) contre-torpilleurs (3 cases), actuellement en J8, J9, J10
   2) croiseur (4 cases), actuellement en A3, A4, A5, A6
   3) porte-avions (5 cases), actuellement en A1, B1, C1, D1, E1
   4) sous-marin (3 cases), actuellement en F1, F2, F3
   5) torpilleur (2 cases), actuellement en D2, E2
Taper stop pour stopper le choix de la flotte
"""
        assert expected_out == out
        assert expected == r

    @pytest.mark.parametrize("saisies, expected", [
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4)
    ])
    def test_choix_bateau_a_positionner_vide(self, capsys, flotte_vide, saisies, expected):
        with mock.patch('builtins.input', return_value=saisies):
            r = terminal.choix_bateau_a_positionner(flotte_vide)
        out, err = capsys.readouterr()

        expected_out = """Choisir le bateau à (re)positionner parmi :
   1) contre-torpilleurs (3 cases), actuellement non positionné
   2) croiseur (4 cases), actuellement non positionné
   3) porte-avions (5 cases), actuellement non positionné
   4) sous-marin (3 cases), actuellement non positionné
   5) torpilleur (2 cases), actuellement non positionné
Taper stop pour stopper le choix de la flotte
"""
        assert expected_out == out
        assert expected == r

    def test_choix_bateau_a_positionner_vide_stop(self, capsys, flotte_vide):
        saisies = ['stop', '1']

        with mock.patch('builtins.input', side_effect=saisies):
            r = terminal.choix_bateau_a_positionner(flotte_vide)

        out, err = capsys.readouterr()
        expected_out = """Choisir le bateau à (re)positionner parmi :
   1) contre-torpilleurs (3 cases), actuellement non positionné
   2) croiseur (4 cases), actuellement non positionné
   3) porte-avions (5 cases), actuellement non positionné
   4) sous-marin (3 cases), actuellement non positionné
   5) torpilleur (2 cases), actuellement non positionné
Taper stop pour stopper le choix de la flotte
"""
        assert expected_out == out
        assert 1 == r

    def test_choix_bateau_a_positionner_erreur(self, capsys, flotte_vide):
        saisies = ['k', '1']

        with mock.patch('builtins.input', side_effect=saisies):
            r = terminal.choix_bateau_a_positionner(flotte_vide)

        out, err = capsys.readouterr()
        expected_out = """Choisir le bateau à (re)positionner parmi :
   1) contre-torpilleurs (3 cases), actuellement non positionné
   2) croiseur (4 cases), actuellement non positionné
   3) porte-avions (5 cases), actuellement non positionné
   4) sous-marin (3 cases), actuellement non positionné
   5) torpilleur (2 cases), actuellement non positionné
Taper stop pour stopper le choix de la flotte
"""
        assert expected_out == out
        assert 1 == r


# *********************************************************************************************************
# Tests de la fonction choix_flotte_manuel_console()
# *********************************************************************************************************
class TestChoixFlotteManuelConsole:
    """
    Tests de la fonction :py:func:`terminal.choix_flotte_manuel_console`
    """
    pytestmark = echeance.ECHEANCE8
    pytestfunction = 'terminal.choix_flotte_manuel_console'

    @pytest.mark.parametrize("direction, positions", [
        pytest.param("horizontal", ["A1", "B1", "C1", "D1", "E1"], id="horizontal"),
        pytest.param("vertical", ["A1", "A2", "A3", "A4", "A5"], id="vertical"),
    ])
    def test_choix_flotte_manuel_console_complete(self,  capsys, datadir, flotte_vide, direction, positions):
        saisies = [[str(i + 1), positions[i], direction] for i in range(5)]
        saisies = list(itertools.chain.from_iterable(saisies)) + ['stop']
        with mock.patch('builtins.input', side_effect=saisies):
            terminal.choix_flotte_manuel_console(flotte_vide)
        out, err = capsys.readouterr()

        actual_out = utils_tests.suppression_couleurs(out)
        expected_out = utils_tests.flotte_read_flotte2d(str(datadir['output_%s.txt' % direction]))
        assert expected_out == actual_out

    @pytest.mark.parametrize("flotte, direction, positions", [
        pytest.param("flotte1", "vertical", "B1", id="vertical"),
        pytest.param("flotte2", "horizontal", "A2", id="horizontal"),
    ])
    def test_choix_flotte_manuel_console_echec(self, capsys, datadir, flotte, direction, positions):
        flotte = utils_tests.flotte_lecture((datadir["{flotte}.json".format(flotte=flotte)]))

        saisies = ["4", positions, direction, "stop"]
        with mock.patch('builtins.input', side_effect=saisies):
            terminal.choix_flotte_manuel_console(flotte)
        out, err = capsys.readouterr()

        actual_out = utils_tests.suppression_couleurs(out)
        expected_out = utils_tests.flotte_read_flotte2d(str(datadir['output_%s.txt' % direction]))
        assert expected_out == actual_out
