import json
import os
from collections import deque

import mock
import pytest

import echeance
import utils_tests

try:
    import jeu_console
except:
    pass


class TestBatailleManuel:
    """
    Tests de la fonction :py:func:`jeu_console.bataille_manuel`
    """
    pytestmark = echeance.ECHEANCE4
    pytestfunction = 'jeu_console.bataille_manuel'

    @pytest.mark.parametrize("ma_flotte_nom, sa_flotte_nom, joueur, saisies", [
        pytest.param("flotte1", "flotte2", "moi", ['stop'], id="cas1"),
        pytest.param("flotte1", "flotte2", "adversaire", ['stop'], id="cas2"),
        pytest.param("flotte1", "flotte2", "moi", ['A1'] * 5 + ['stop'], id="cas3"),
        pytest.param("flotte1", "flotte2", "adversaire", ['A1'] * 5 + ['stop'], id="cas4")
    ])
    def test_bataille_manuel_stop(self, datadir, ma_flotte_nom, sa_flotte_nom, joueur, saisies):
        ma_flotte = utils_tests.flotte_lecture(datadir["{ma_flotte_nom}.json".format(ma_flotte_nom=ma_flotte_nom)])
        sa_flotte = utils_tests.flotte_lecture(datadir["{sa_flotte_nom}.json".format(sa_flotte_nom=sa_flotte_nom)])

        with mock.patch('builtins.input', side_effect=saisies):
            res = jeu_console.bataille_manuel(ma_flotte, sa_flotte, joueur)
        assert "abandonne" == res

    @pytest.mark.parametrize("ma_flotte_nom, sa_flotte_nom, jeu, joueur, resultat", [
        pytest.param("flotte1", "flotte2", "je_joue_je_gagne", "moi", "gagne", id="je_joue_je_gagne"),
        pytest.param("flotte1", "flotte2", "il_joue_je_gagne", "adversaire", "gagne", id="il_joue_je_gagne"),
        pytest.param("flotte1", "flotte2", "il_joue_il_gagne", "adversaire", "perd", id="il_joue_il_gagne"),
        pytest.param("flotte1", "flotte2", "je_joue_il_gagne", "moi", "perd", id="je_joue_il_gagne")
    ])
    def test_bataille_manuel(self, datadir, ma_flotte_nom, sa_flotte_nom, jeu, joueur, resultat):
        ma_flotte = utils_tests.flotte_lecture(datadir["{ma_flotte_nom}.json".format(ma_flotte_nom=ma_flotte_nom)])
        sa_flotte = utils_tests.flotte_lecture(datadir["{sa_flotte_nom}.json".format(sa_flotte_nom=sa_flotte_nom)])

        [mes_coups, ses_coups] = json.load(datadir["{jeu}.json".format(jeu=jeu)].open("rb"))
        saisies = list()
        if joueur == "moi":
            z = zip(mes_coups, ses_coups)
        else:
            z = zip(ses_coups, mes_coups)
        for e in z:
            saisies.append(e[0])
            saisies.append(e[1])
        print(saisies)

        with mock.patch('builtins.input', side_effect=saisies):
            res = jeu_console.bataille_manuel(ma_flotte, sa_flotte, joueur)
        assert resultat == res


class TestBatailleAuto:
    """
    Tests de la fonction :py:func:`jeu_console.bataille_auto`
    """

    pytestmark = echeance.ECHEANCE7
    pytestfunction = 'jeu_console.bataille_auto'

    @pytest.mark.parametrize("ma_flotte_nom, sa_flotte_nom, joueur, saisies", [
        pytest.param("flotte1", "flotte2", "moi", ['stop'], id="cas1"),
        pytest.param("flotte1", "flotte2", "adversaire", ['stop'], id="cas2"),
        pytest.param("flotte1", "flotte2", "moi", ['A1'] * 5 + ['stop'], id="cas3"),
        pytest.param("flotte1", "flotte2", "adversaire", ['A1'] * 5 + ['stop'], id="cas4")
    ])
    def test_bataille_auto_stop(self, datadir, ma_flotte_nom, sa_flotte_nom, joueur, saisies):
        ma_flotte = utils_tests.flotte_lecture(datadir["{ma_flotte_nom}.json".format(ma_flotte_nom=ma_flotte_nom)])
        sa_flotte = utils_tests.flotte_lecture(datadir["{sa_flotte_nom}.json".format(sa_flotte_nom=sa_flotte_nom)])

        with mock.patch('builtins.input', side_effect=saisies):
            res = jeu_console.bataille_auto(ma_flotte, sa_flotte, joueur, "auto")
        assert 'abandonne' == res

    @pytest.mark.parametrize("ma_flotte_nom, sa_flotte_nom, jeu, joueur, resultat", [
        pytest.param("flotte1", "flotte2", "je_joue_je_gagne", "moi", "gagne", id="je_joue_je_gagne"),
        pytest.param("flotte1", "flotte2", "il_joue_je_gagne", "adversaire", "gagne", id="il_joue_je_gagne"),
        pytest.param("flotte1", "flotte2", "il_joue_il_gagne", "adversaire", "perd", id="il_joue_il_gagne"),
        pytest.param("flotte1", "flotte2", "je_joue_il_gagne", "moi", "perd", id="je_joue_il_gagne")
    ])
    def test_bataille_auto(self, datadir, ma_flotte_nom, sa_flotte_nom, jeu, joueur, resultat):
        ma_flotte = utils_tests.flotte_lecture(datadir["{ma_flotte_nom}.json".format(ma_flotte_nom=ma_flotte_nom)])
        sa_flotte = utils_tests.flotte_lecture(datadir["{sa_flotte_nom}.json".format(sa_flotte_nom=sa_flotte_nom)])

        [mes_coups, ses_coups] = json.load(datadir["{jeu}.json".format(jeu=jeu)].open("rb"))

        with mock.patch('builtins.input', side_effect=mes_coups), \
             mock.patch('flottes.tir_aleatoire', side_effect=ses_coups):
            res = jeu_console.bataille_auto(ma_flotte, sa_flotte, joueur, "auto")
        assert resultat == res


class _MockSocket:
    def __init__(self, commands=None):
        if commands is None:
            self.__commands = None
        else:
            self.__commands = deque(commands)
        self.__sent_messages = list()

    def recuperation_commande_serveur(self):
        cmd = self.__commands.popleft()
        return cmd

    def repond_au_serveur(self, reponse):
        self.__sent_messages.append(reponse)

    @property
    def sent_messages(self):
        return self.__sent_messages


class TestInitialisationBatailleReseau:
    pytestmark = echeance.ECHEANCE7
    pytestfunction = 'jeu_console.initialisation_bataille_reseau'

    @pytest.mark.parametrize("commandes_serveur, expected_sent_messages", [
        pytest.param(["[pseudo]", "[start]barfoo"],
                     ['[pseudo]foobar', '[ack]'],
                     id="second"),
        pytest.param(["[pseudo]", "[attente]", "[attente]", "[start]barfoo"],
                     ['[pseudo]foobar', '[ack]', '[ack]', '[ack]'],
                     id="premier")
    ])
    def test_initialisation_bataille_reseau(self, datadir, commandes_serveur, expected_sent_messages):
        ma_flotte = utils_tests.flotte_lecture(datadir["flotte1.json"])
        sa_flotte = utils_tests.flotte_lecture(datadir["flotte_vide.json"])
        ip = None
        port = None

        socket = _MockSocket(commandes_serveur)
        with mock.patch('builtins.input', side_effect=["foobar"]), \
             mock.patch('reseau.connexion_serveur', return_value=socket), \
             mock.patch('reseau.recuperation_commande_serveur',
                        side_effect=lambda socket_actif: socket_actif.recuperation_commande_serveur()), \
             mock.patch('reseau.repond_au_serveur',
                        side_effect=lambda socket_actif, reponse: socket_actif.repond_au_serveur(reponse)):
            jeu_console.initialisation_bataille_reseau(ma_flotte, sa_flotte, ip, port)

        assert "foobar" == ma_flotte['pseudo']
        assert "barfoo" == sa_flotte['pseudo']
        assert expected_sent_messages == socket.sent_messages

    def test_initialisation_bataille_reseau_connexion_erreur(self, datadir):
        ma_flotte = utils_tests.flotte_lecture(datadir["flotte1.json"])
        sa_flotte = utils_tests.flotte_lecture(datadir["flotte_vide.json"])
        ip = None
        port = None

        with mock.patch('reseau.connexion_serveur', return_value=None):
            res = jeu_console.initialisation_bataille_reseau(ma_flotte, sa_flotte, ip, port)
        assert res is None

    @pytest.mark.parametrize("commandes_serveur, expected_sent_messages", [
        pytest.param(["[pseudo]", "[fin]"],
                     ['[pseudo]foobar'],
                     id="second"),
        pytest.param(["[pseudo]", "[attente]", "[attente]", "[fin]"],
                     ['[pseudo]foobar', '[ack]', '[ack]'],
                     id="premier"),
        pytest.param(["[pseudo]", "[attente]", "[attente]", "[timeout]"],
                     ['[pseudo]foobar', '[ack]', '[ack]'],
                     id="timeout")
    ])
    def test_initialisation_bataille_reseau_fin(self, datadir, commandes_serveur, expected_sent_messages):
        ma_flotte = utils_tests.flotte_lecture(datadir["flotte1.json"])
        sa_flotte = utils_tests.flotte_lecture(datadir["flotte_vide.json"])
        ip = None
        port = None

        socket = _MockSocket(commandes_serveur)
        with mock.patch('builtins.input', side_effect=["foobar"]), \
             mock.patch('reseau.connexion_serveur', return_value=socket), \
             mock.patch('reseau.recuperation_commande_serveur',
                        side_effect=lambda socket_actif: socket_actif.recuperation_commande_serveur()), \
             mock.patch('reseau.repond_au_serveur',
                        side_effect=lambda socket_actif, reponse: socket_actif.repond_au_serveur(reponse)):
            res = jeu_console.initialisation_bataille_reseau(ma_flotte, sa_flotte, ip, port)

        assert res is None
        assert expected_sent_messages == socket.sent_messages


class TestBatailleReseauEnvoyerTir:
    pytestmark = echeance.ECHEANCE8
    pytestfunction = 'jeu_console.bataille_reseau_envoyer_tir'

    @pytest.mark.parametrize("case, effet, expected_touche, expected_coule", [
        pytest.param("A1", "touche", 1, 0),
        pytest.param("A1", "coule", 1, 1),
        pytest.param("A1", "eau", 0, 0),
        pytest.param("A1", "gagne", 1, 1)
    ])
    def test_bataille_reseau_envoyer_tir(self, datadir, case, effet, expected_touche, expected_coule):
        ma_flotte = utils_tests.flotte_lecture(datadir["flotte1.json"])
        sa_flotte = utils_tests.flotte_lecture(datadir["flotte_vide.json"])

        commandes_serveur = ["[resultat]{case}|{effet}".format(case=case, effet=effet)]
        socket = _MockSocket(commandes_serveur)
        with mock.patch('builtins.input', side_effect=["A1"]), \
             mock.patch('reseau.connexion_serveur', return_value=socket), \
             mock.patch('reseau.recuperation_commande_serveur',
                        side_effect=lambda socket_actif: socket_actif.recuperation_commande_serveur()), \
             mock.patch('reseau.repond_au_serveur',
                        side_effect=lambda socket_actif, reponse: socket_actif.repond_au_serveur(reponse)):
            res = jeu_console.bataille_reseau_envoyer_tir(ma_flotte, sa_flotte, socket, 1)

        assert effet == res
        assert [case] == sa_flotte['tirs']
        assert [effet] == sa_flotte['effets']
        assert expected_touche == sa_flotte['nbreTouche']
        assert expected_coule == sa_flotte['nbreCoule']
        assert ['[tir]{case}'.format(case=case), '[ack]'] == socket.sent_messages

    def test_bataille_reseau_envoyer_tir_stop(self, datadir):
        ma_flotte = utils_tests.flotte_lecture(datadir["flotte1.json"])
        sa_flotte = utils_tests.flotte_lecture(datadir["flotte_vide.json"])

        socket = _MockSocket()
        with mock.patch('builtins.input', side_effect=["stop"]), \
             mock.patch('reseau.connexion_serveur', return_value=socket), \
             mock.patch('reseau.recuperation_commande_serveur',
                        side_effect=lambda socket_actif: socket_actif.recuperation_commande_serveur()), \
             mock.patch('reseau.repond_au_serveur',
                        side_effect=lambda socket_actif, reponse: socket_actif.repond_au_serveur(reponse)):
            res = jeu_console.bataille_reseau_envoyer_tir(ma_flotte, sa_flotte, socket, 1)

        assert "stop" == res
        assert [] == sa_flotte['tirs']
        assert [] == sa_flotte['effets']
        assert ["[fin]"] == socket.sent_messages


class TestBatailleReseauTirRecu:
    pytestmark = echeance.ECHEANCE8
    pytestfunction = 'jeu_console.bataille_reseau_tir_recu'

    @pytest.mark.parametrize(
        "flotte, case, expected_case_effet, expected_tirs, expected_effets, expected_touche, expected_coule", [
            pytest.param("flotte-touche", "A1", "touche", ['A1'], ['touche'], 1, 0, id="touche"),
            pytest.param("flotte-coule", "A1", "coule", ['B1', 'C1', 'D1', 'E1', 'A1'], ['touche'] * 4 + ['coule'], 1,
                         1, id="coule"),
            pytest.param("flotte-eau", "A2", "eau", ['A2'], ['eau'], 0, 0, id="eau"),
            pytest.param("flotte-gagne", "A1", "gagne",
                         ["B1", "C1", "D1", "E1", "G1", "G2", "G3", "G4",
                          "H1", "H2", "H3", "I1", "I2", "I3", "J1", "J2", "A1"],
                         ['gagne'], 1, 1, id="gagne")
        ])
    def test_bataille_reseau_tir_recu(self, datadir, flotte, case, expected_case_effet, expected_tirs, expected_effets,
                                      expected_touche, expected_coule):
        ma_flotte = utils_tests.flotte_lecture(datadir["{flotte}.json".format(flotte=flotte)])
        sa_flotte = utils_tests.flotte_lecture(datadir["flotte_vide.json"])

        commandes_serveur = ["[resultat]"]
        socket = _MockSocket(commandes_serveur)
        with mock.patch('builtins.input', side_effect=["stop"]), \
             mock.patch('reseau.connexion_serveur', return_value=socket), \
             mock.patch('reseau.recuperation_commande_serveur',
                        side_effect=lambda socket_actif: socket_actif.recuperation_commande_serveur()), \
             mock.patch('reseau.repond_au_serveur',
                        side_effect=lambda socket_actif, reponse: socket_actif.repond_au_serveur(reponse)):
            res = jeu_console.bataille_reseau_tir_recu(ma_flotte, sa_flotte, case, socket, 1)

        assert expected_case_effet == res
        assert expected_tirs == ma_flotte['tirs']
        assert expected_effets == ma_flotte['effets']
        assert ['[resultat]{case}|{expected_case_effet}'.format(case=case, expected_case_effet=expected_case_effet)] == socket.sent_messages


class TestBatailleReseau:
    pytestmark = echeance.ECHEANCE8
    pytestfunction = 'jeu_console.bataille_reseau'

    def test_bataille_reseau_erreur_init(self, datadir):
        ma_flotte = utils_tests.flotte_lecture(datadir["flotte1.json"])
        sa_flotte = utils_tests.flotte_lecture(datadir["flotte_vide.json"])
        ip = None
        port = None

        with mock.patch('builtins.input', side_effect=["foobar"]), \
             mock.patch('reseau.connexion_serveur', return_value=None):
            res = jeu_console.bataille_reseau(ma_flotte, ip, port)

        assert res is None

    @pytest.mark.parametrize("partie, resultat", [
        pytest.param("partie1", "gagne"),
        pytest.param("partie2", "perd"),
        pytest.param("partie3", "gagne"),
        pytest.param("partie4", "perd"),
        pytest.param("partie5", "abandonne"),
        pytest.param("partie6", "abandonne"),
    ])
    def test_bataille_reseau(self, datadir, partie, resultat):
        ip = None
        port = None
        ma_flotte = utils_tests.flotte_lecture(datadir["flotte1.json"])
        partie_content = utils_tests.flotte_lecture(datadir["{partie}.json".format(partie=partie)])
        commandes_serveur = partie_content["commandes_serveur"]
        saisies = partie_content["saisies"]
        sent_messages = partie_content["messages_envoyes"]
        socket = _MockSocket(commandes_serveur)
        with mock.patch('builtins.input', side_effect=saisies), \
             mock.patch('reseau.connexion_serveur', return_value=socket), \
             mock.patch('reseau.recuperation_commande_serveur',
                        side_effect=lambda socket_actif: socket_actif.recuperation_commande_serveur()), \
             mock.patch('reseau.repond_au_serveur',
                        side_effect=lambda socket_actif, reponse: socket_actif.repond_au_serveur(reponse)):
            res = jeu_console.bataille_reseau(ma_flotte, ip, port)

        assert resultat == res
        assert sent_messages == socket.sent_messages


class TestChoixFlotte:
    pytestmark = echeance.ECHEANCE9
    pytestfunction = 'jeu_console.choix_flotte'

    def test_choix_flotte_endur(self, datadir):
        with mock.patch('builtins.input', side_effect=["1"]):
            res = jeu_console.choix_flotte()
        flotte1 = utils_tests.flotte_lecture(datadir["flotte1.json"])
        flotte2 = utils_tests.flotte_lecture(datadir["flotte2.json"])

        # Fix pseudo
        flotte1["pseudo"] = "moi"
        flotte2["pseudo"] = "adversaire"
        assert flotte1 == res[0]
        assert flotte2 == res[1]

    @pytest.mark.parametrize("saisie_nom, expected_flotte_nom", [
        pytest.param("saisie_flotte1", "flotte1_saisie")
    ])
    def test_choix_flotte_manuel(self, datadir, saisie_nom, expected_flotte_nom):
        saisie = json.load(datadir["{saisie_nom}.json".format(saisie_nom=saisie_nom)].open("rb"))
        expected_flotte = utils_tests.flotte_lecture(datadir["{expected_flotte_nom}.json".format(expected_flotte_nom=expected_flotte_nom)])
        with mock.patch('builtins.input', side_effect=["2"] + saisie):
            res = jeu_console.choix_flotte()
        assert expected_flotte == res[0]

        flotte_vide = utils_tests.flotte_lecture(datadir["flotte_vide.json"])
        assert flotte_vide == res[1]

    @pytest.mark.parametrize("saisie_nom, expected_flotte_nom", [
        pytest.param("saisie_flotte1", "flotte1_saisie")
    ])
    def test_choix_flotte_manuel_aleatoire(self, datadir, saisie_nom, expected_flotte_nom):
        saisie = json.load(datadir["{saisie_nom}.json".format(saisie_nom=saisie_nom)].open("rb"))
        expected_flotte = utils_tests.flotte_lecture(datadir["{expected_flotte_nom}.json".format(expected_flotte_nom=expected_flotte_nom)])
        with mock.patch('builtins.input', side_effect=["3"] + saisie):
            res = jeu_console.choix_flotte()
        assert expected_flotte == res[0]

        sa_flotte = res[1]
        for bat, nbcases in utils_tests.LONGUEURS_BATEAUX.items():
            assert nbcases == len(sa_flotte['bateaux'][bat])

    def test_choix_flotte_aleatoire(self):
        with mock.patch('builtins.input', side_effect=["4"]):
            res = jeu_console.choix_flotte()

        ma_flotte = res[1]
        for bat, nbcases in utils_tests.LONGUEURS_BATEAUX.items():
            assert nbcases == len(ma_flotte['bateaux'][bat])

        sa_flotte = res[1]
        for bat, nbcases in utils_tests.LONGUEURS_BATEAUX.items():
            assert nbcases == len(sa_flotte['bateaux'][bat])

    @pytest.mark.parametrize("cas", ["cas1"])
    def test_choix_flotte_restauree(self, datadir, cas, restaure_repertoire_tests):
        expected_ma_flotte = utils_tests.flotte_lecture(datadir["{cas}/ma_flotte.json".format(cas=cas)])
        expected_sa_flotte = utils_tests.flotte_lecture(datadir["{cas}/sa_flotte.json".format(cas=cas)])

        dir = datadir["cas1"]
        os.chdir(str(dir))

        with mock.patch('builtins.input', side_effect=["5"]):
            res = jeu_console.choix_flotte()

        assert expected_ma_flotte == res[0]
        assert expected_sa_flotte == res[1]

    def test_choix_flotte_restauree_echec(self, datadir):
        with mock.patch('builtins.input', side_effect=["5", "1"]):
            res = jeu_console.choix_flotte()

        flotte1 = utils_tests.flotte_lecture(datadir["flotte1.json"])
        flotte2 = utils_tests.flotte_lecture(datadir["flotte2.json"])

        # Fix pseudo
        flotte1["pseudo"] = "moi"
        flotte2["pseudo"] = "adversaire"
        assert flotte1 == res[0]
        assert flotte2 == res[1]



def _bataille_reseau_side_effect(*args, **kwargs):
    """
    This is the mock side_effect for bataille_reseau mock to change flotte pseudo
    """
    args[0]["pseudo"] = "foobar"
    return mock.DEFAULT


class TestPartie:
    pytestmark = echeance.ECHEANCE9
    pytestfunction = 'jeu_console.partie'

    @pytest.mark.parametrize("resultat", ["gagne", "perd"])
    @pytest.mark.parametrize("joueur", ["moi", "adversaire"])
    @pytest.mark.parametrize("mode_choix_flotte", [
        "endur",
        "manuel",
        "manuel-aleatoire",
        "aleatoires",
        "restaurees"
    ])
    def test_partie_bataille_manuel(self, datadir, change_repertoire_courant_tmpdir, mode_choix_flotte, joueur, resultat):
        partie = json.load(datadir["{mode_choix_flotte}.json".format(mode_choix_flotte=mode_choix_flotte)].open("rb"))
        saisie = partie["saisie"]

        flotte1 = utils_tests.flotte_lecture(datadir["flotte1.json"])
        flotte2 = utils_tests.flotte_lecture(datadir["flotte2.json"])
        flotte_vide = utils_tests.flotte_lecture(datadir["flotte_vide.json"])

        with mock.patch('builtins.input', side_effect=saisie), \
             mock.patch(
                 "flottes.initialisation_flotte_par_dictionnaire_fixe",
                 side_effect=[flotte1, flotte2]) as mock_initialisation_flotte_par_dictionnaire_fixe, \
                mock.patch(
                    "flottes.initialisation_flotte_vide",
                    return_value=flotte_vide) as mock_initialisation_flotte_vide, \
                mock.patch("terminal.choix_flotte_manuel_console") as mock_choix_flotte_manuel_console, \
                mock.patch("flottes.choix_flotte_aleatoire") as mock_choix_flotte_aleatoire, \
                mock.patch("flottes.restauration_partie") as mock_restauration_partie, \
                mock.patch("outils.affichage_statistiques_joueurs") as mock_affichage_statistiques_joueurs, \
                mock.patch("outils.joueur_aleatoire", return_value=joueur) as mock_joueur_aleatoire, \
                mock.patch("outils.ajoute_statistiques_joueur") as mock_ajoute_statistiques_joueur, \
                mock.patch("jeu_console.bataille_manuel", return_value=resultat) as mock_bataille_manuel:
            jeu_console.partie()

        # Vérification de l'appel à outils.affichage_statistiques_joueurs()
        mock_affichage_statistiques_joueurs.assert_called_once
        mock_bataille_manuel.assert_called_once
        mock_ajoute_statistiques_joueur.assert_called_once
        mock_joueur_aleatoire.assert_called_once
        assert partie["initialisation_flotte_par_dictionnaire_fixe"] == \
               mock_initialisation_flotte_par_dictionnaire_fixe.call_count
        assert partie["initialisation_flotte_vide"] == \
               mock_initialisation_flotte_vide.call_count
        assert partie["choix_flotte_manuel_console"] == \
               mock_choix_flotte_manuel_console.call_count
        assert partie["choix_flotte_aleatoire"] == \
               mock_choix_flotte_aleatoire.call_count
        assert partie["restauration_partie"] == \
               mock_restauration_partie.call_count
        mock_ajoute_statistiques_joueur.assert_called_once_with('foobar', resultat)

    @pytest.mark.parametrize("resultat", ["gagne", "perd"])
    @pytest.mark.parametrize("joueur", ["moi", "adversaire"])
    @pytest.mark.parametrize("mode_choix_flotte", [
        "endur",
        "manuel",
        "manuel-aleatoire",
        "aleatoires",
        "restaurees"
    ])
    def test_partie_bataille_auto(self, datadir, change_repertoire_courant_tmpdir, mode_choix_flotte, joueur, resultat):
        partie = json.load(datadir["{mode_choix_flotte}.json".format(mode_choix_flotte=mode_choix_flotte)].open("rb"))
        saisie = partie["saisie"]
        saisie.reverse()

        flotte1 = utils_tests.flotte_lecture(datadir["flotte1.json"])
        flotte2 = utils_tests.flotte_lecture(datadir["flotte2.json"])
        flotte_vide = utils_tests.flotte_lecture(datadir["flotte_vide.json"])

        with mock.patch('builtins.input', side_effect=lambda x: saisie.pop()), \
             mock.patch(
                 "flottes.initialisation_flotte_par_dictionnaire_fixe",
                 side_effect=[flotte1, flotte2]) as mock_initialisation_flotte_par_dictionnaire_fixe, \
                mock.patch(
                    "flottes.initialisation_flotte_vide",
                    return_value=flotte_vide) as mock_initialisation_flotte_vide, \
                mock.patch("terminal.choix_flotte_manuel_console") as mock_choix_flotte_manuel_console, \
                mock.patch("flottes.choix_flotte_aleatoire") as mock_choix_flotte_aleatoire, \
                mock.patch("flottes.restauration_partie") as mock_restauration_partie, \
                mock.patch("outils.affichage_statistiques_joueurs") as mock_affichage_statistiques_joueurs, \
                mock.patch("outils.joueur_aleatoire", return_value=joueur) as mock_joueur_aleatoire, \
                mock.patch("outils.ajoute_statistiques_joueur") as mock_ajoute_statistiques_joueur, \
                mock.patch("jeu_console.bataille_auto", return_value=resultat) as mock_bataille_auto:
            jeu_console.partie()

        # Vérification de l'appel à outils.affichage_statistiques_joueurs()
        mock_affichage_statistiques_joueurs.assert_called_once
        mock_bataille_auto.assert_called_once
        mock_ajoute_statistiques_joueur.assert_called_once
        mock_joueur_aleatoire.assert_called_once
        assert partie["initialisation_flotte_par_dictionnaire_fixe"] == \
               mock_initialisation_flotte_par_dictionnaire_fixe.call_count
        assert partie["initialisation_flotte_vide"] == \
               mock_initialisation_flotte_vide.call_count
        assert partie["choix_flotte_manuel_console"] == \
               mock_choix_flotte_manuel_console.call_count
        assert partie["choix_flotte_aleatoire"] == \
               mock_choix_flotte_aleatoire.call_count
        assert partie["restauration_partie"] == \
               mock_restauration_partie.call_count
        mock_ajoute_statistiques_joueur.assert_called_once_with('foobar', resultat)

    @pytest.mark.parametrize("resultat", ["gagne", "perd"])
    @pytest.mark.parametrize("joueur", ["moi", "adversaire"])
    @pytest.mark.parametrize("mode_choix_flotte", [
        # "endur",
        # "manuel",
        # "manuel-aleatoire",
        "aleatoires",
        # "restaurees"
    ])
    def test_partie_bataille_reseau(self, datadir, change_repertoire_courant_tmpdir, mode_choix_flotte, joueur, resultat):
        partie = json.load(datadir["{mode_choix_flotte}.json".format(mode_choix_flotte=mode_choix_flotte)].open("rb"))
        saisie = partie["saisie"]
        saisie.reverse()

        flotte1 = utils_tests.flotte_lecture(datadir["flotte1.json"])
        flotte1["pseudo"] = 'foobar'
        flotte2 = utils_tests.flotte_lecture(datadir["flotte2.json"])
        flotte_vide = utils_tests.flotte_lecture(datadir["flotte_vide.json"])

        with mock.patch('builtins.input', side_effect=lambda x: saisie.pop()), \
             mock.patch(
                 "flottes.initialisation_flotte_par_dictionnaire_fixe",
                 side_effect=[flotte1, flotte2]) as mock_initialisation_flotte_par_dictionnaire_fixe, \
                mock.patch(
                    "flottes.initialisation_flotte_vide",
                    return_value=flotte_vide) as mock_initialisation_flotte_vide, \
                mock.patch("terminal.choix_flotte_manuel_console") as mock_choix_flotte_manuel_console, \
                mock.patch("flottes.choix_flotte_aleatoire") as mock_choix_flotte_aleatoire, \
                mock.patch("flottes.restauration_partie") as mock_restauration_partie, \
                mock.patch("outils.affichage_statistiques_joueurs") as mock_affichage_statistiques_joueurs, \
                mock.patch("outils.joueur_aleatoire", return_value=joueur) as mock_joueur_aleatoire, \
                mock.patch("outils.ajoute_statistiques_joueur") as mock_ajoute_statistiques_joueur, \
                mock.patch("jeu_console.bataille_reseau") as mock_bataille_reseau:
            mock_bataille_reseau.side_effect=_bataille_reseau_side_effect
            mock_bataille_reseau.return_value = resultat
            jeu_console.partie()

        # Vérification de l'appel à outils.affichage_statistiques_joueurs()
        mock_affichage_statistiques_joueurs.assert_called_once
        mock_bataille_reseau.assert_called_once
        mock_ajoute_statistiques_joueur.assert_called_once
        mock_joueur_aleatoire.assert_called_once
        assert partie["initialisation_flotte_par_dictionnaire_fixe"] == \
               mock_initialisation_flotte_par_dictionnaire_fixe.call_count
        assert partie["initialisation_flotte_vide"] == \
               mock_initialisation_flotte_vide.call_count
        assert partie["choix_flotte_manuel_console"] == \
               mock_choix_flotte_manuel_console.call_count
        assert partie["choix_flotte_aleatoire"] == \
               mock_choix_flotte_aleatoire.call_count
        assert partie["restauration_partie"] == \
               mock_restauration_partie.call_count
        mock_ajoute_statistiques_joueur.assert_called_once_with('foobar', resultat)

    # @pytest.mark.bataille_reel
    # def test_partie_bataille_reseau_reel(self, datadir, change_repertoire_courant_tmpdir):
    #     saisies = json.load(datadir["saisies.json"].open("rb"))
    #     saisies.reverse()
    #
    #     with mock.patch('builtins.input', side_effect=lambda x: saisies.pop()):
    #         jeu_console.partie()