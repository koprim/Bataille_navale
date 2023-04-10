import copy
import os

import pytest

import utils_tests

REPERTOIRE_TESTS = os.path.dirname(os.path.realpath(__file__))
REPERTOIRE_CODES = os.path.dirname(REPERTOIRE_TESTS)


@pytest.fixture
def change_repertoire_courant_datadir(datadir):
    """Déplace le répertoire courant pour être celui des codes sources"""
    dir = datadir["."]
    os.chdir(str(dir))
    yield dir
    os.chdir(REPERTOIRE_TESTS)  # replace la console dans le répertoire de tests après test


@pytest.fixture
def change_repertoire_courant_datadir_copy(datadir_copy):
    """Déplace le répertoire courant pour être celui des données"""
    dir = datadir_copy["."]
    os.chdir(str(dir))
    yield dir
    os.chdir(REPERTOIRE_TESTS)  # replace la console dans le répertoire de tests après test


@pytest.fixture
def change_repertoire_courant_tmpdir(tmpdir):
    """Déplace le répertoire courant pour être celui temporaire de test"""
    os.chdir(str(tmpdir))
    yield tmpdir
    os.chdir(REPERTOIRE_TESTS)  # replace la console dans le répertoire de tests après test


@pytest.fixture
def restaure_repertoire_tests():
    """Déplace le répertoire courant pour être celui des tests"""

    yield dir
    os.chdir(REPERTOIRE_TESTS)  # replace la console dans le répertoire de tests après test


@pytest.fixture
def cases_possibles():
    return utils_tests.CASES_POSSIBLES


@pytest.fixture
def flotte_random():
    return utils_tests.flotte_random()


@pytest.fixture
def flotte_vide(datadir):
    return copy.deepcopy(utils_tests.flotte_lecture(datadir["flotte_vide.json"]))
