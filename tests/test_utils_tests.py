"""
Script de tests unitaires de flottes_tests_utils.py proposant des méthodes utilisées par les tests unitaires.
"""

import pytest

import couleurs
import utils_tests


class TestCalculDirection:
    @pytest.mark.parametrize("positions, expected", [
        pytest.param(["A1", "A2"], "horizontal", id="test1"),
        pytest.param(["A1", "B1"], "vertical", id="test2"),
        pytest.param(['D7', 'D8', 'D9', 'D10'], "horizontal", id="test3")
    ])
    def test_calcul_direction(self, positions, expected):
        assert utils_tests.calcul_direction(positions) == expected

    @pytest.mark.parametrize("positions", [
        pytest.param(["A1", "B2"]),
        pytest.param(["A1", "A3"]),
    ])
    def test_calcul_direction_erreur(self, positions):
        with pytest.raises(Exception) as e:
            utils_tests.calcul_direction(positions)


class TestSuppressionCouleurs:
    @pytest.mark.parametrize("content, expected", [
        pytest.param(couleurs.COULEURS["rouge"] + "rouge\n" + couleurs.COULEURS["blanc"] + "blanc", 2, id="rouge-blanc"),
        pytest.param(couleurs.COULEURS['rouge'] + " X" + couleurs.COULEURS['blanc'] + " " + couleurs.COULEURS['rouge'] + " X" + couleurs.COULEURS['blanc'], 4, id="rouge-X-blanc- -rouge-X-blanc")
    ])
    @pytest.mark.skipif(not couleurs.AVEC_COLORAMA,
                        reason="requires colorama")
    def test_suppression_couleurs_colorama(self, content, expected):
        assert couleurs.AVEC_COLORAMA
        assert expected == utils_tests.compte_couleurs(content)

    @pytest.mark.parametrize("content, expected", [
        pytest.param(couleurs.COULEURS["rouge"] + "rouge\n" + couleurs.COULEURS["blanc"] + "blanc", 2, id="rouge-blanc"),
        pytest.param(couleurs.COULEURS['rouge'] + " X" + couleurs.COULEURS['blanc'] + " " + couleurs.COULEURS['rouge'] + " X" + couleurs.COULEURS['blanc'], 4, id="rouge-X-blanc- -rouge-X-blanc")
    ])
    @pytest.mark.skipif(couleurs.AVEC_COLORAMA,
                        reason="does not require colorama")
    def test_suppression_couleurs_not_colorama(self, content, expected):
        assert not couleurs.AVEC_COLORAMA
        assert expected == utils_tests.compte_couleurs(content)


@pytest.mark.parametrize("content, expected", [
    pytest.param(couleurs.COULEURS["rouge"] + "rouge\n" + couleurs.COULEURS["blanc"] + "blanc", "rouge\nblanc")
])
def test_suppression_couleurs(content, expected):
    assert expected == utils_tests.suppression_couleurs(content)


@pytest.mark.parametrize("file, expected", [
    pytest.param("file1.txt", "\033[31mrouge\n\033[37mblanc", id="rouge-blanc"),
])
def test_flotte_read_flotte2d(datadir, file, expected):
    actual = utils_tests.flotte_read_flotte2d(str(datadir[file]))
    assert expected == actual


@pytest.mark.parametrize("file, expected", [
    ("file1.txt", """rouge
blanc"""),
])
def test_flotte_read_flotte2d_suppression_couleurs(datadir, file, expected):
    actual = utils_tests.flotte_read_flotte2d(str(datadir[file]), True)
    assert expected == actual
