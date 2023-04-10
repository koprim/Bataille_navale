# coding: UTF-8
"""
Script: ia.py

"""
import random
import outils
import flottes
import terminal
import jeu_console
import string


# Fonctions
def auto(flotte):
	"""
	idées à mettre en place :
	- Identifié la taille du bateau qui va être coulée
	- Au lieu de faire un tir aléatoire, essayé de choisir des cases plus stratégiques style angle et bord
	- MARCHE PAS POUR DES BATEAUX COLLEE
	- Comment va marcher la compétition qui doit faire la fonction tout ça tout ça

	"""
	list_cases = liste_cases()
	effets = flotte['effets']
	tirs = flotte['tirs']
	taille = len(effets)
	tir = "A0"

	while not (outils.est_case_valide(tir)) or (tir in tirs):
		indices_motif_coulee = [0]
		coulee = 0
		while coulee < taille:
			if 'coulee' in effets[coulee:]:
				indices_motif_coulee.append(effets[coulee:].index('coulee') + coulee)
				coulee = indices_motif_coulee[-1] + 1
			else:
				coulee = taille + 1
		try:
			if effets[-1] == "coulee":
				coulee = indices_motif_coulee[-1] + 1
			else:
				coulee = indices_motif_coulee[0]
		except:
			pass
		try:
			tirs[effets[coulee:].index('touche') + coulee]
		except:
			tir = tir_strategique(tirs)
			return tir

		if str(effets).find("touche") == -1 or taille == 0 or effets[-1] == "coulee":
			tir = tir_strategique(tirs)
			return tir

		if taille >= 1:
			if effets[-1] == "touche":
				case_touchee = tirs[effets[coulee:].index('touche') + coulee]
				cases = case_autour(case_touchee)
				if taille >= 2:
					if effets[-2] == 'touche':
						direction = direction_bateau_touche(tirs[-2], tirs[-1])
						case_longueur = case_direction(case_touchee, direction)
						for case in case_longueur:
							if case in tirs:
								if tir_effet(tirs, effets)[case] == 'eau' and list_cases.index(case) < list_cases.index(case_touchee):
									case_longueur = case_longueur[case_longueur.index(case):]
								elif tir_effet(tirs, effets)[case] == 'eau' and list_cases.index(case) > list_cases.index(case_touchee):
									case_longueur = case_longueur[:case_longueur.index(case)]
								elif tir_effet(tirs, effets)[case] == 'touche':
									if case in case_longueur:
										case_longueur.remove(case)
						tir = random.choice(case_longueur)
					else:  # SI IL Y A TOUCHE ET EAU EN AVANT DERNIER
						case_touchee = tirs[effets[coulee:].index('touche') + coulee]
						cases = case_autour(case_touchee)
						tir = random.choice(cases)
						for elm in case_autour(case_touchee):
							if elm in tirs and tir_effet(tirs, effets)[elm] == 'eau':
								cases.remove(elm)
								tir = random.choice(cases)
							elif elm in tirs and (tir_effet(tirs, effets)[elm] == 'touche' or tir_effet(tirs, effets)[elm] == 'coulee'):
								direction = direction_bateau_touche(case_touchee, elm)
								case_longueur = case_direction(case_touchee, direction)
								for case in case_longueur:
									if case in tirs:
										if tir_effet(tirs, effets)[case] == 'eau' and list_cases.index(
												case) < list_cases.index(
												case_touchee):
											case_longueur = case_longueur[case_longueur.index(case):]
										elif tir_effet(tirs, effets)[case] == 'eau' and list_cases.index(
												case) > list_cases.index(case_touchee):
											case_longueur = case_longueur[:case_longueur.index(case)]
										elif tir_effet(tirs, effets)[case] == 'touche':
											case_longueur.remove(case)
								if len(case_longueur) == 0:
									tir = random.choice(cases)
								else:
									tir = random.choice(case_longueur)

				else:
					tir = random.choice(cases)
			elif effets[-1] == "eau":  # effets[-1] == 'coulee'  ou  effets[-1] == 'eau' ou not tirs
				if effets[-2] == 'touche':
					case_touchee = tirs[effets[coulee:].index('touche') + coulee]
					cases = case_autour(case_touchee)
					for elm in case_autour(case_touchee):
						if elm in tirs and tir_effet(tirs, effets)[elm] == 'eau':
							cases.remove(elm)
							tir = random.choice(cases)
						elif elm in tirs and tir_effet(tirs, effets)[elm] == 'touche':
							direction = direction_bateau_touche(case_touchee, elm)
							case_longueur = case_direction(case_touchee, direction)
							for case in case_longueur:
								if case in tirs:
									if tir_effet(tirs, effets)[case] == 'eau' and list_cases.index(case) < list_cases.index(
											case_touchee):
										case_longueur = case_longueur[case_longueur.index(case):]
									elif tir_effet(tirs, effets)[case] == 'eau' and list_cases.index(
											case) > list_cases.index(case_touchee):
										case_longueur = case_longueur[:case_longueur.index(case)]
									elif tir_effet(tirs, effets)[case] == 'touche':
										case_longueur.remove(case)
							if len(case_longueur) == 0:
								tir = random.choice(cases)
							else:
								tir = random.choice(case_longueur)
				elif effets[-2] == "eau" or effets[-2] == 'coulee':
					case_touchee = tirs[effets[coulee:].index('touche') + coulee]
					cases = case_autour(case_touchee)
					tir = random.choice(cases)
					for elm in case_autour(case_touchee):
						if elm in tirs and tir_effet(tirs, effets)[elm] == 'eau':
							cases.remove(elm)
						elif elm in tirs and tir_effet(tirs, effets)[elm] == 'touche':
							direction = direction_bateau_touche(case_touchee, elm)
							case_longueur = case_direction(case_touchee, direction)
							for case in case_longueur:
								if case in tirs:
									if tir_effet(tirs, effets)[case] == 'eau' and list_cases.index(case) < list_cases.index(
											case_touchee):
										case_longueur = case_longueur[case_longueur.index(case):]
									elif tir_effet(tirs, effets)[case] == 'eau' and list_cases.index(
											case) > list_cases.index(case_touchee):
										case_longueur = case_longueur[:case_longueur.index(case)]
									elif tir_effet(tirs, effets)[case] == 'touche':
										case_longueur.remove(case)
							tir = random.choice(case_longueur)
				else:
					tir = tir_strategique(tirs)


	return tir


def tir_effet(tirs, effets):
	dico = {}
	i = 0
	for case in tirs:
		dico[case] = effets[i]
		i += 1
	return dico


def direction_bateau_touche(case_1, case_2):
	car_1 = [case_1[0], case_1[1:]]
	car_2 = [case_2[0], case_2[1:]]
	if car_1[0] == car_2[0]:
		return "horizontal"
	else:
		return "vertical"


def liste_cases():
	list_cases = []
	for lettre in string.ascii_uppercase[:10]:
		for chiffre in range(1, 11):
			list_cases.append(lettre + str(chiffre))
	return list_cases


def case_suivante(case, direction, i):
	car = [case[0], case[1:]]
	if direction == "horizontal":
		case = car[0] + str(int(car[1]) + i)
	elif direction == 'vertical':
		case = string.ascii_uppercase[string.ascii_uppercase[:10].index(car[0]) + i] + car[1]
	return case


def case_direction(case, direction):
	liste_cases = []
	for i in range(5, 1, -1):
		if outils.est_case_valide(case_suivante(case, direction, -i)):
			liste_cases.append(case_suivante(case, direction, -i))
	for i in range(1, 5):
		if outils.est_case_valide(case_suivante(case, direction, i)):
			liste_cases.append(case_suivante(case, direction, i))
	return liste_cases


def case_autour(case):
	"""
	Ajoute dans une liste les cases autour dans les 2 axes de celle en paramètre
	:param case:
	:return: liste
	"""
	liste = []
	case_g = case_suivante(case, 'horizontal', -1)
	if outils.est_case_valide(case_g):
		liste.append(case_g)
	case_d = case_suivante(case, 'horizontal', 1)
	if outils.est_case_valide(case_d):
		liste.append(case_d)
	case_h = case_suivante(case, 'vertical', -1)
	if outils.est_case_valide(case_h):
		liste.append(case_h)
	case_b = case_suivante(case, 'vertical', 1)
	if outils.est_case_valide(case_b):
		liste.append(case_b)
	return liste


def parties_concours_ia(nb_parties, ip, port):
	mon_pseudo = terminal.saisie_pseudo()
	for i in range(nb_parties):
		ma_flotte = flottes.initialisation_flotte_vide()
		flottes.choix_flotte_aleatoire(ma_flotte)
		res = jeu_console.bataille_reseau(ma_flotte, ip, port)
		outils.ajoute_statistiques_joueur(mon_pseudo, res)
		outils.affichage_statistiques_joueurs()
	return


def tir_strategique(tirs):
	list_cases = liste_cases()
	i = 0
	tir = list_cases[2 * i]
	while tir in tirs:
		i += 1
		if ((i / 5) % 2) == 0:
			tir = list_cases[2 * i + 1]
		else:
			tir = list_cases[2 * i]
	return tir


# Programme principal
def main():
	flotte = {
		'bateaux': {
			'porte-avions': ["A1", "B1", "C1", "D1", "E1"],
			'croiseur': ["A2", "B2", "C2", "D2"],
			'contre-torpilleurs': ["J8", "J9", "J10"],
			'sous-marin': ["F1", "F2", "F3"],
			'torpilleur': ["D2", "E2"]},
		'tirs': ["A1", "A2", "A3"],
		'effets': ["touche", "touche", "coulee"],
		'pseudo': 'moi'}
	print(auto(flotte))

	#jeu_console.partie()

if __name__ == '__main__':
	main()