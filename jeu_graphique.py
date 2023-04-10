import operator
import outils
import flottes
import pygame
import ia

surfaceW = 1280  # Dimension de la fenêtre / Largeur
surfaceH = 720  # Dimension de la fenêtre / Longueur


def verif_bateau(bateau, positions):
	tailles = {
		'porte-avions': 5,
		'croiseur': 4,
		'contre-torpilleurs': 3,
		'sous-marin': 3,
		'torpilleur': 2,
	}
	if len(positions) == tailles[bateau]:
		h = True
		v = True
		indices = [outils.case_ln_vers_indices(elmt) for elmt in positions]
		tri = sorted(indices, key=operator.itemgetter(0, 1))
		for i in range(tailles[bateau]):
			if tri[i][0] != tri[0][0] + i or tri[i][1] != tri[0][1]:
				h = False
				break
		for i in range(tailles[bateau]):
			if tri[i][1] != tri[0][1] + i or tri[i][0] != tri[0][0]:
				v = False
				break
		return h or v
	else:
		return False


def verif_positions(positions):
	# couleur = {
	# 		'porte-avions': "bleu",
	# 		'croiseur': "rouge",
	# 		'contre-torpilleurs': "verte",
	# 		'sous-marin': "orange",
	# 		'torpilleur': "violette",
	# }
	tailles = {
		'bleu': 5,
		'rouge': 4,
		'verte': 3,
		'orange': 3,
		'violette': 2,
	}
	validations = []
	for couleur in positions:
		if couleur in ['bleu', 'rouge', 'verte', 'orange', 'violette']:
			if len(positions[couleur]) == tailles[couleur]:
				h = True
				v = True
				indices = [outils.case_ln_vers_indices(elmt) for elmt in positions[couleur]]
				tri = sorted(indices, key=operator.itemgetter(0, 1))
				for i in range(tailles[couleur]):
					if tri[i][0] != tri[0][0] + i or tri[i][1] != tri[0][1]:
						h = False
						break
				for i in range(tailles[couleur]):
					if tri[i][1] != tri[0][1] + i or tri[i][0] != tri[0][0]:
						v = False
						break
				validations.append(h or v)
			else:
				return False
	return False not in validations


def orientation(liste_cases):
	if liste_cases[0][0] == liste_cases[1][0]:
		return "horizontal"
	else:
		return "vertical"


class Menu:
	""" Création et gestion des boutons d'un menu """

	def __init__(self, application, *groupes):
		self._fenetre = application.fenetre
		self.background = pygame.image.load("images/gui/menu/background2.png")
		self.rectBackground = self.background.get_rect()
		self.rectBackground.center = (surfaceW / 2, surfaceH / 2)
		self.titre = pygame.image.load("images/gui/menu/titre.png")
		self.rectTitre = self.titre.get_rect()
		self.rectTitre.center = (surfaceW / 2, 150)
		# noms des menus et commandes associées
		items = (
			('un_joueur', application.positionnement),
			('multijoueur', application.positionnement),
			('options', application.options),
			('quitter', application.quitter),
		)
		x = surfaceW / 2
		y = 300
		self._boutons = []
		for nom, cmd in items:
			mb = MenuBouton(
				nom,
				"",
				x,
				y,
				cmd
			)
			self._boutons.append(mb)
			y += 30
			for groupe in groupes:
				groupe.add(mb)

	def update(self, application, events):
		self._fenetre.blit(self.background, self.rectBackground)
		self._fenetre.blit(self.titre, self.rectTitre)
		self.image = pygame.Surface((200, 20))
		clicGauche, *_ = pygame.mouse.get_pressed()
		posPointeur = pygame.mouse.get_pos()
		for bouton in self._boutons:
			# Si le pointeur souris est au-dessus d'un bouton
			if bouton.rect.collidepoint(*posPointeur):
				# Changement du curseur par un quelconque
				pygame.mouse.set_cursor(*pygame.cursors.tri_left)
				# Changement de la couleur du bouton
				bouton.dessiner("survol")
				# Si le clic gauche a été pressé
				if clicGauche:
					# Appel de la fonction du bouton
					if bouton.nom == "un_joueur":
						application.mode = "solo"
						flottes.choix_flotte_aleatoire_silence(application.flotte2)
						application.n_joueur = 1
					elif bouton.nom == "multijoueur":
						application.mode = "multi"
						application.n_joueur = 2
					bouton.executerCommande(application.sons)
				break
			else:
				# Le pointeur n'est pas au-dessus du bouton
				bouton.dessiner("normal")
		else:
			# Le pointeur n'est pas au-dessus d'un des boutons
			# initialisation au pointeur par défaut
			pygame.mouse.set_cursor(*pygame.cursors.arrow)

	def detruire(self):
		pygame.mouse.set_cursor(*pygame.cursors.arrow)  # initialisation du pointeur


class MenuBouton(pygame.sprite.Sprite):
	""" Création d'un simple bouton rectangulaire """

	def __init__(self, nom, etat, x, y, commande):
		super().__init__()
		self.nom = nom
		self._commande = commande
		self.image = pygame.Surface((200, 20))
		self.son_clic = pygame.mixer.Sound('sons/effets/click.ogg')

		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		self.image_normal = pygame.image.load(f"images/gui/menu/{nom}.png")
		self.image_survol = pygame.image.load(f"images/gui/menu/{nom}_hovered.png")
		self.rect_image = self.image_normal.get_rect()

		self.dessiner(etat)

	def dessiner(self, etat):
		if etat == "survol":
			self.image.blit(self.image_survol, self.rect_image)
		else:
			self.image.blit(self.image_normal, self.rect_image)

	def executerCommande(self, son_active):
		# On joue l'effet sonore du bouton
		if son_active:
			self.son_clic.play()
		# Appel de la commande du bouton
		self._commande()


class Jeu:
	""" Simulacre de l'interface du jeu """

	def __init__(self, application, *groupes):
		self.tour = application.tour
		if self.tour == "J1":
			self.flotte1 = application.flotte1
			self.flotte2 = application.flotte2
		elif self.tour == "J2":
			self.flotte1 = application.flotte2
			self.flotte2 = application.flotte1
		self.case = "##"
		self.son_clic = pygame.mixer.Sound('sons/effets/click.ogg')
		self.font = pygame.font.SysFont("comicsansms", 17, bold=True)
		self._fenetre = application.fenetre
		self.map = pygame.image.load("images/gui/jeu/map_background.png")
		self.rectMap = self.map.get_rect()
		self.rectMap.center = (400, surfaceH / 2)
		self.choix_case = pygame.image.load("images/gui/jeu/choix_case.png")
		self.rectChoix_case = self.choix_case.get_rect()
		self.rectChoix_case.center = (1000, 550)
		self.ma_flotte = pygame.image.load(f"images/gui/jeu/ma_flotte_{self.tour}.png")
		self.rectMa_flotte = self.ma_flotte.get_rect()
		self.rectMa_flotte.center = (1000, 220)
		self.gauche_presse = True
		self.droit_presse = True
		self.valide = False
		self._bateaux = []
		self.positions_des_bateaux = flottes.positions_bateaux(self.flotte1)
		x_offset = 886
		y_offset = 128
		for bateau in self.flotte1["bateaux"]:
			liste_cases = self.flotte1["bateaux"][bateau]
			if orientation(liste_cases) == "horizontal":
				orient = "hori"
			elif orientation(liste_cases) == "vertical":
				orient = "verti"
			for case in liste_cases:
				if case == outils.case_min(liste_cases):
					forme = orient + "_extr1"
				elif case == outils.case_max(liste_cases):
					forme = orient + "_extr2"
				else:
					forme = orient + "_centre"
				indices = outils.case_ln_vers_indices(case)
				nom = self.positions_des_bateaux[case]
				x = indices[1] * 25 + x_offset
				y = indices[0] * 25 + y_offset
				cmd = application.nothing
				bat = Bateau(
					nom,
					case,
					forme,
					"",
					x,
					y,
					cmd
				)
				self._bateaux.append(bat)
				for groupe in groupes:
					groupe.add(bat)

		# Creation des tirs sur la flotte adverse
		self._tirs = []
		x_offset = 190
		y_offset = 150
		for n in range(1, 11):
			for L in 'ABCDEFGHIJ':
				case = L + str(n)
				indices = outils.case_ln_vers_indices(case)
				x = x_offset + indices[1] * 46.5
				y = y_offset + indices[0] * 46.5
				cmd = application.nothing
				tir = Tir(
					case,
					"",
					x,
					y,
					cmd
				)
				self._tirs.append(tir)
				for groupe in groupes:
					groupe.add(tir)

		# Creation des tirs sur ma flotte
		self.cobweb = pygame.image.load("images/cobweb.png").convert_alpha()
		self.destroy = pygame.image.load("images/destroy.png").convert_alpha()
		self.tnt = pygame.image.load("images/tnt_side_petit.png")
		self.diamond = pygame.image.load("images/diamond_block.png")
		self._tirs_sur_moi = []
		x_offset = 886
		y_offset = 128
		for case in self.flotte1["tirs"]:
			indices = outils.case_ln_vers_indices(case)
			x = x_offset + indices[1] * 25
			y = y_offset + indices[0] * 25
			cmd = application.nothing
			tir = Tir(
				case,
				"",
				x,
				y,
				cmd
			)
			effet = self.flotte1["effets"][self.flotte1["tirs"].index(case)]
			if effet == "eau":
				tir.image_normal = self.cobweb
			elif effet == "gagne":
				tir.image_normal = self.diamond
			elif effet == "touche":
				tir.image_normal = self.destroy
			elif effet == "coule":
				tir.image_normal = self.tnt
			self._tirs_sur_moi.append(tir)
			for groupe in groupes:
				groupe.add(tir)

		items = (
			('valider', application.changement if application.mode == "multi" else application.jeu),
			('quitter', application.menu),
		)
		x = 1000
		y = 550
		self._boutons = []
		for nom, cmd in items:
			mb = MenuBouton(
				nom,
				"",
				x,
				y,
				cmd
			)
			self._boutons.append(mb)
			y += 30
			for groupe in groupes:
				groupe.add(mb)

		# Creation de la barre de vie
		self._coeurs = []
		x = 840
		y = 76
		for n in range(5):
			co = Coeur(
				x,
				y,
			)
			x += 28
			self._coeurs.append(co)
			for groupe in groupes:
				groupe.add(co)

		application.fond = (0, 0, 200)
		self.background = pygame.image.load("images/water_background/water-0.png")
		self.rectBackground = self.background.get_rect()
		self.rectBackground.center = (surfaceW / 2, surfaceH / 2)
		self.i_water = 0
		# Création d'un event
		self._NEXTFRAME = pygame.USEREVENT + 1
		pygame.time.set_timer(self._NEXTFRAME, 500)

	def update(self, application, events):
		vie = 5 - flottes.nombre_bateaux_coules(self.flotte1)
		self._fenetre.blit(self.background, self.rectBackground)
		self._fenetre.blit(self.map, self.rectMap)
		self._fenetre.blit(self.ma_flotte, self.rectMa_flotte)
		self._fenetre.blit(self.choix_case, self.rectChoix_case)
		if not self.valide:
			texte = self.font.render(self.case, True, (0, 0, 0))
			texte_rect = texte.get_rect(center=(1120, 508))
			self._fenetre.blit(texte, texte_rect)
		clicGauche = pygame.mouse.get_pressed()[0]
		clicDroit = pygame.mouse.get_pressed()[2]
		posPointeur = pygame.mouse.get_pos()
		for tir in self._tirs:
			if tir.case in self.flotte2["tirs"]:
				if not tir.modif:
					effet = flottes.analyse_tir_sans_modif(self.flotte2, tir.case)
					if effet == "touche":
						tir.image_normal = pygame.image.load("images/destroy_map.png")
					elif effet == "coule":
						tir.image_normal = pygame.image.load("images/tnt_side.png")
					elif effet == "eau":
						tir.image_normal = pygame.image.load("images/cobweb_map.png")
					elif effet == "gagne":
						tir.image_normal = pygame.image.load("images/diamond_block.png")
					tir.modif = True
			if tir.rect.collidepoint(*posPointeur):
				# Changement de la couleur du bouton
				tir.dessiner("survol")
				# Si le clic gauche a été pressé
				if clicGauche:
					if not self.gauche_presse:
						self.gauche_presse = True
						self.case = tir.case
						if application.sons:
							tir.jouerSon()
					# Appel de la fonction du bouton
					# tir.executerCommande()
				else:
					self.gauche_presse = False
				break
			else:
				# Le pointeur n'est pas au-dessus du bouton
				tir.dessiner("normal")
		for bateau in self._bateaux:
			# Si le pointeur souris est au-dessus d'un bateau
			if bateau.rect.collidepoint(*posPointeur):
				# Changement de la couleur du bateau
				bateau.dessiner("survol")
				# Si le clic gauche a été pressé
				if clicGauche:
					if not self.gauche_presse:
						self.gauche_presse = True
						# bateau.executerCommande()
				else:
					self.gauche_presse = False
				break
			else:
				# Le pointeur n'est pas au-dessus du bateau
				bateau.dessiner("normal")
		for bouton in self._boutons:
			# Si le pointeur souris est au-dessus d'un bouton
			if bouton.rect.collidepoint(*posPointeur):
				# Changement du curseur par un quelconque
				pygame.mouse.set_cursor(*pygame.cursors.tri_left)
				# Changement de la couleur du bouton
				bouton.dessiner("survol")
				# Si le clic gauche a été pressé
				if clicGauche:
					if not self.gauche_presse:
						self.gauche_presse = True
						if bouton.nom == "valider":
							if self.case != "##" and self.case not in self.flotte2["tirs"] or self.valide:
								if self.valide:
									if "gagne" in self.flotte1["effets"]:
										application.gagnant = self.tour
										bouton._commande = application.vainqueur
										application.gagnant = "J1" if self.tour == "J2" else "J2"
										bouton._commande = application.vainqueur
									elif "gagne" in self.flotte2["effets"]:
										application.gagnant = self.tour
										bouton._commande = application.vainqueur
									bouton.executerCommande(application.sons)
								else:
									if application.sons:
										self.jouerSon("clic")
									self.flotte2["tirs"].append(self.case)
									effet = flottes.analyse_tir_sans_modif(self.flotte2, self.case)
									if application.sons:
										self.jouerSon("clic")
										son = pygame.mixer.Sound(f'sons/effets/{effet}.ogg')
										son.play()
									self.flotte2["effets"].append(effet)
									self.choix_case = pygame.image.load(f"images/gui/jeu/resultat_{effet}.png")
									self._boutons[0].image_normal = pygame.image.load("images/gui/menu/ok_point.png")
									self._boutons[0].image_survol = pygame.image.load("images/gui/menu/ok_point_hovered.png")
									if application.mode == "solo":
										tir_adversaire = flottes.tir_aleatoire(self.flotte1)  # IA modifier ici : flottes.tir_aleatoire(self.flotte1) ou ia.auto(self.flotte1)
										self.flotte1["tirs"].append(tir_adversaire)
										self.flotte1["effets"].append(flottes.analyse_tir_sans_modif(self.flotte1, tir_adversaire))
									elif application.mode == "multi":
										pass
									self.valide = True
							else:
								if application.sons:
									self.jouerSon("clic")
						elif bouton.nom == "quitter":
							application.flotte1 = flottes.initialisation_flotte_vide()
							application.flotte2 = flottes.initialisation_flotte_vide()
							bouton.executerCommande(application.sons)
						else:
							bouton.executerCommande(application.sons)
				else:
					self.gauche_presse = False
				break
			else:
				# Le pointeur n'est pas au-dessus du bouton
				bouton.dessiner("normal")
		else:
			# Le pointeur n'est pas au-dessus d'un des boutons
			# initialisation au pointeur par défaut
			pygame.mouse.set_cursor(*pygame.cursors.arrow)
		for tir in self._tirs_sur_moi:
			if tir.rect.collidepoint(*posPointeur):
				# Changement de la couleur du bouton
				tir.dessiner("survol")
				# Si le clic gauche a été pressé
				if clicGauche:
					if not self.gauche_presse:
						tir.jouerSon()
					# Appel de la fonction du bouton
					# tir.executerCommande()
				else:
					self.gauche_presse = False
				break
			else:
				# Le pointeur n'est pas au-dessus du bouton
				tir.dessiner("normal")
		for coeur in self._coeurs:
			if vie > 0:
				coeur.dessiner("plein")
				vie -= 1
			else:
				coeur.dessiner("vide")
		# for event in events:
		# 	if event.type == self._NEXTFRAME:
		# 		self.animation_fond()
		# 		break

	def animation_fond(self):
		self.i_water = (self.i_water + 1) % 16
		self.background = pygame.image.load(f"images/water_background/water-{self.i_water}.png")

	def jouerSon(self, nom_som):
		if nom_som == "clic":
			# On joue l'effet sonore du bouton
			self.son_clic.play()


class Coeur(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.Surface([30, 30], pygame.SRCALPHA, 32)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.image_plein = pygame.image.load("images/gui/jeu/coeur_plein.png")
		self.image_vide = pygame.image.load("images/gui/jeu/coeur_vide.png")
		self.rect_image = self.image_plein.get_rect()

	def dessiner(self, etat):
		if etat == "plein":
			self.image.blit(self.image_plein, self.rect_image)
		elif etat == "vide":
			self.image.blit(self.image_vide, self.rect_image)


class Tir(pygame.sprite.Sprite):
	def __init__(self, case, effet, x, y, commande):
		super().__init__()
		self.effet = effet
		self.case = case
		self.modif = False
		self._commande = commande
		self.son_clic = pygame.mixer.Sound('sons/effets/stone.ogg')
		self.image = pygame.Surface([30, 30], pygame.SRCALPHA, 32)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.image_normal = pygame.image.load("images/blue_concrete.png").convert_alpha()
		self.rect_image = self.image_normal.get_rect()
		self.font = pygame.font.SysFont("comicsansms", 12)
		self.font2 = pygame.font.SysFont("comicsansms", 13)

	def dessiner(self, effet):
		self.image.blit(self.image_normal, self.rect_image)
		if effet == "survol":
			texte = self.font.render(self.case, True, (255, 255, 255))
			texte_rect = texte.get_rect(center=(30 / 2, 30 / 2))
			self.image.blit(texte, texte_rect)

	def executerCommande(self, couleur, son_active):
		# self.image_normal = pygame.image.load(f"images/gui/jeu/laine_{couleur}.png").convert_alpha
		pass

	def jouerSon(self):
		# On joue l'effet sonore du bouton
		self.son_clic.play()


class Bateau(pygame.sprite.Sprite):
	""" Création d'un simple bouton rectangulaire """

	def __init__(self, nom, case, forme, etat, x, y, commande):
		super().__init__()
		self.nom = nom
		self.case = case
		self._commande = commande
		self.son_clic = pygame.mixer.Sound('sons/effets/click.ogg')
		self.image = pygame.Surface((25, 25))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		if forme == "hori_extr1":
			self.image_normal = pygame.image.load("images/bateau_hori_extr1.png")
		elif forme == "hori_extr2":
			self.image_normal = pygame.image.load("images/bateau_hori_extr2.png")
		elif forme == "hori_centre":
			self.image_normal = pygame.image.load("images/bateau_hori_centre.png")
		elif forme == "verti_extr1":
			self.image_normal = pygame.image.load("images/bateau_verti_extr1.png")
		elif forme == "verti_extr2":
			self.image_normal = pygame.image.load("images/bateau_verti_extr2.png")
		elif forme == "verti_centre":
			self.image_normal = pygame.image.load("images/bateau_verti_centre.png")
		self.rect_image = self.image_normal.get_rect()
		self.font = pygame.font.SysFont("comicsansms", 12)

		self.dessiner(etat)

	def dessiner(self, etat):
		self.image.blit(self.image_normal, self.rect_image)
		if etat == "survol":
			texte = self.font.render(self.case, True, (255, 255, 255))
			texte_rect = texte.get_rect(center=(25 / 2, 25 / 2))
			self.image.blit(texte, texte_rect)

	def executerCommande(self, son_active):
		# On joue l'effet sonore du bouton
		if son_active:
			self.son_clic.play()
		# Appel de la commande du bouton
		self._commande()


class Positionnement:
	""" Simulacre de l'interface des options """

	def __init__(self, application, *groupes):
		self._fenetre = application.fenetre
		self.gauche_presse = True
		self.droit_presse = True
		self.milieu_presse = False
		application.fond = (128, 128, 128)
		if application.n_joueur == 2:
			self.grille = pygame.image.load("images/gui/jeu/grille_J2.png")
		else:
			self.grille = pygame.image.load("images/gui/jeu/grille_J1.png")
		self.rectGrille = self.grille.get_rect()
		self.rectGrille.center = (500, surfaceH / 2)
		self.info = pygame.image.load("images/gui/jeu/info_positionnement.png")
		self.rectInfo = self.info.get_rect()
		self.rectInfo.center = (640, 50)
		self.astuce = pygame.image.load("images/gui/jeu/astuce.png")
		self.rectAstuce = self.astuce.get_rect()
		self.rectAstuce.center = (500, 610)

		# Images des laines :
		x = 917
		y = 185
		ecart = 37
		self.bleu = pygame.image.load("images/gui/jeu/laine_bleu.png")
		self.rectBleu = self.bleu.get_rect()
		self.rectBleu.center = (x, y)
		self.rouge = pygame.image.load("images/gui/jeu/laine_rouge.png")
		self.rectRouge = self.rouge.get_rect()
		self.rectRouge.center = (x, y + 1 * ecart)
		self.verte = pygame.image.load("images/gui/jeu/laine_verte.png")
		self.rectVerte = self.verte.get_rect()
		self.rectVerte.center = (x, y + 2 * ecart)
		self.orange = pygame.image.load("images/gui/jeu/laine_orange.png")
		self.rectOrange = self.orange.get_rect()
		self.rectOrange.center = (x, y + 3 * ecart)
		self.violette = pygame.image.load("images/gui/jeu/laine_violette.png")
		self.rectViolette = self.violette.get_rect()
		self.rectViolette.center = (x, y + 4 * ecart)
		
		self.multiplieur = pygame.image.load("images/gui/jeu/multiplieur.png")
		self.rectMultiplieur = self.multiplieur.get_rect()
		self.rectMultiplieur.center = (880, 260)
		self.couleur = "invisible"
		self.son_content = pygame.mixer.Sound('sons/effets/content.ogg')
		self.son_pas_content = pygame.mixer.Sound('sons/effets/pas_content.ogg')
		# Positions des laines
		self.taille = {
			'invisible': 999,
			'effacer': 999,
			'bleu': 5,
			'rouge': 4,
			'verte': 3,
			'orange': 3,
			'violette': 2,
		}
		self.positions = {
			'invisible': [],
			'effacer': [],
			'bleu': [],
			'rouge': [],
			'verte': [],
			'orange': [],
			'violette': [],
		}
		self.correspondance = {
			'porte-avions': "bleu",
			'croiseur': "rouge",
			'contre-torpilleurs': "verte",
			'sous-marin': "orange",
			'torpilleur': "violette"
		}
		# Creation des boutons posi
		items = (
			('porte-avions', "bleu"),
			('croiseur', "rouge"),
			('contre-torpilleurs', "verte"),
			('sous-marin', "orange"),
			('torpilleur', "violette")
		)
		x = 1055
		y = 186
		self._boutons = []
		for nom, couleur in items:
			mb = PosiBouton(
				nom,
				couleur,
				"",
				x,
				y,
			)
			self._boutons.append(mb)
			y += 37
			for groupe in groupes:
				groupe.add(mb)
		# Boutons Menu
		items2 = (
			('aleatoire', application.nothing),
			('effacer', application.positionnement),
			('valider', application.nothing),
			('quitter', application.menu)
		)
		x = 1055
		y = 450
		for nom, cmd in items2:
			b = MenuBouton(
				nom,
				"",
				x,
				y,
				cmd
			)
			self._boutons.append(b)
			y += 30
			for groupe in groupes:
				groupe.add(b)

		# Creation des laines
		self._laines = []
		x_offset = 290
		y_offset = 155
		for L in 'ABCDEFGHIJ':
			for n in range(1, 11):
				case = L + str(n)
				indices = outils.case_ln_vers_indices(case)
				x = x_offset + indices[1] * 46.5
				y = y_offset + indices[0] * 46.5
				cmd = application.nothing
				lai = Laine(
					self,
					case,
					"",
					x,
					y,
					cmd
				)
				self._laines.append(lai)
				for groupe in groupes:
					groupe.add(lai)

		# Creation de la barre de vie
		self._validations = []
		x = 1170
		y = 185
		for bateau in ["porte-avions", "croiseur", "contre-torpilleurs", "sous-marin", "torpilleur"]:
			vali = Validation(
				bateau,
				x,
				y,
			)
			y += 37
			self._validations.append(vali)
			for groupe in groupes:
				groupe.add(vali)
		self.couleur = "bleu"

	def update(self, application, events):
		self._fenetre.blit(self.grille, self.rectGrille)
		self._fenetre.blit(self.info, self.rectInfo)
		self._fenetre.blit(self.astuce, self.rectAstuce)
		self._fenetre.blit(self.multiplieur, self.rectMultiplieur)
		self._fenetre.blit(self.bleu, self.rectBleu)
		self._fenetre.blit(self.rouge, self.rectRouge)
		self._fenetre.blit(self.verte, self.rectVerte)
		self._fenetre.blit(self.orange, self.rectOrange)
		self._fenetre.blit(self.violette, self.rectViolette)
		clicGauche = pygame.mouse.get_pressed()[0]
		clicMilieu = pygame.mouse.get_pressed()[1]
		clicDroit = pygame.mouse.get_pressed()[2]
		posPointeur = pygame.mouse.get_pos()
		for laine in self._laines:
			if laine.rect.collidepoint(*posPointeur):
				# Changement de la couleur du bouton
				laine.dessiner("survol")
				# Si le clic gauche a été pressé
				if clicGauche:
					if not self.gauche_presse:
						self.gauche_presse = True
						laine.jouerSon()
					if len(self.positions[self.couleur]) < self.taille[self.couleur]:
						# Appel de la fonction du bouton
						laine.executerCommande(self.couleur, application.sons)
						if laine.case not in self.positions[self.couleur]:
							for couleur in self.positions:
								if laine.case in self.positions[couleur]:
									laine.couleur = "effacer"
									self.positions[couleur].remove(laine.case)
							laine.couleur = self.couleur
							self.positions[self.couleur].append(laine.case)
				else:
					self.gauche_presse = False
				if clicDroit:
					if not self.droit_presse:
						self.droit_presse = True
						laine.jouerSon()
					for couleur in self.positions:
						if laine.case in self.positions[couleur]:
							laine.couleur = "effacer"
							self.positions[couleur].remove(laine.case)
					laine.executerCommande("effacer", application.sons)
				else:
					self.droit_presse = False
				if clicMilieu:
					if not self.milieu_presse:
						print("lol")
						self.milieu_presse = True
						self.couleur = laine.couleur
				else:
					self.milieu_presse = False
				break
			else:
				# Le pointeur n'est pas au-dessus du bouton
				laine.dessiner("normal")
		for valid in self._validations:
			if verif_bateau(valid.bateau, self.positions[self.correspondance[valid.bateau]]):
				valid.dessiner("valide")
			else:
				valid.dessiner("pas_valide")
		for bouton in self._boutons:
			if isinstance(bouton, PosiBouton):
				# Si le pointeur souris est au-dessus d'un bouton
				if bouton.rect.collidepoint(*posPointeur):
					# Changement du curseur par un quelconque
					pygame.mouse.set_cursor(*pygame.cursors.tri_left)
					# Changement de la couleur du bouton
					bouton.dessiner("survol")
					# Si le clic gauche a été pressé
					if clicGauche:
						if not self.gauche_presse:
							self.gauche_presse = True
							if bouton.couleur in ["rouge", "bleu", "verte", "violette", "orange"]:
								# Changement de la couleur en fonction de celle du bouton
								self.couleur = bouton.couleur
							# Appel de la fonction du bouton
							elif bouton.couleur == "debogue":
								self.debogue()
							bouton.executerCommande(application.sons)
					else:
						self.gauche_presse = False
					break
				else:
					# Le pointeur n'est pas au-dessus du bouton
					bouton.dessiner("normal")
			elif isinstance(bouton, MenuBouton):
				# Si le pointeur souris est au-dessus d'un bouton
				if bouton.rect.collidepoint(*posPointeur):
					# Changement du curseur par un quelconque
					pygame.mouse.set_cursor(*pygame.cursors.tri_left)
					# Changement de la couleur du bouton
					bouton.dessiner("survol")
					# Si le clic gauche a été pressé
					if clicGauche:
						if clicGauche:
							if not self.gauche_presse:
								self.gauche_presse = True
								if bouton.nom == "aleatoire":
									for laine in self._laines:
										laine.executerCommande("effacer", application.sons)
									flotte = flottes.initialisation_flotte_vide()
									flottes.choix_flotte_aleatoire_silence(flotte)
									self.positions["bleu"] = flotte["bateaux"]["porte-avions"]
									self.positions["rouge"] = flotte["bateaux"]["croiseur"]
									self.positions["orange"] = flotte["bateaux"]["sous-marin"]
									self.positions["verte"] = flotte["bateaux"]["contre-torpilleurs"]
									self.positions["violette"] = flotte["bateaux"]["torpilleur"]
									for coul in self.positions:
										for case in self.positions[coul]:
											for laine in self._laines:
												if laine.case == case:
													laine.executerCommande(coul, application.sons)
								if bouton.nom == "valider":
									if verif_positions(self.positions):
										if application.sons:
											self.son_content.play()
										if application.n_joueur == 2:
											application.flotte2["bateaux"]["porte-avions"] = self.positions["bleu"]
											application.flotte2["bateaux"]["croiseur"] = self.positions["rouge"]
											application.flotte2["bateaux"]["sous-marin"] = self.positions["orange"]
											application.flotte2["bateaux"]["contre-torpilleurs"] = self.positions["verte"]
											application.flotte2["bateaux"]["torpilleur"] = self.positions["violette"]
											application.n_joueur -= 1
											application.positionnement()
										elif application.n_joueur == 1:
											application.flotte1["bateaux"]["porte-avions"] = self.positions["bleu"]
											application.flotte1["bateaux"]["croiseur"] = self.positions["rouge"]
											application.flotte1["bateaux"]["sous-marin"] = self.positions["orange"]
											application.flotte1["bateaux"]["contre-torpilleurs"] = self.positions["verte"]
											application.flotte1["bateaux"]["torpilleur"] = self.positions["violette"]
											application.jeu()
									else:
										if application.sons:
											self.son_pas_content.play()
								# Appel de la fonction du bouton
								bouton.executerCommande(application.sons)
					else:
						self.gauche_presse = False
					break
				else:
					# Le pointeur n'est pas au-dessus du bouton
					bouton.dessiner("normal")
		else:
			# Le pointeur n'est pas au-dessus d'un des boutons
			# initialisation au pointeur par défaut
			pygame.mouse.set_cursor(*pygame.cursors.arrow)

	def debogue(self):
		print(verif_positions(self.positions))


class Validation(pygame.sprite.Sprite):
	def __init__(self, bateau, x, y):
		super().__init__()
		self.bateau = bateau
		self.image = pygame.Surface([21, 21], pygame.SRCALPHA, 32)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.image_valide = pygame.image.load("images/gui/jeu/valide.png").convert_alpha()
		self.image_pas_valide = pygame.image.load("images/gui/jeu/pas_valide.png").convert_alpha()
		self.rect_image = self.image_valide.get_rect()

	def dessiner(self, etat):
		if etat == "valide":
			self.image.blit(self.image_valide, self.rect_image)
		elif etat == "pas_valide":
			self.image.blit(self.image_pas_valide, self.rect_image)


class PosiBouton(pygame.sprite.Sprite):
	""" Création d'un simple bouton rectangulaire """

	def __init__(self, nom, couleur, etat, x, y):
		super().__init__()
		self.couleur = couleur
		self.image = pygame.Surface((200, 20))
		self.son_clic = pygame.mixer.Sound('sons/effets/click.ogg')

		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		self.image_normal = pygame.image.load(f"images/gui/menu/{nom}.png")
		self.image_survol = pygame.image.load(f"images/gui/menu/{nom}_hovered.png")
		self.rect_image = self.image_normal.get_rect()

		self.dessiner(etat)

	def dessiner(self, etat):
		if etat == "survol":
			self.image.blit(self.image_survol, self.rect_image)
		else:
			self.image.blit(self.image_normal, self.rect_image)

	def executerCommande(self, son_active):
		# On joue l'effet sonore du bouton
		if son_active:
			self.son_clic.play()


class Laine(pygame.sprite.Sprite):

	def __init__(self, positionnement, case, etat, x, y, commande):
		super().__init__()
		self.couleur = positionnement.couleur
		self.case = case
		self._commande = commande
		self.son_clic = pygame.mixer.Sound('sons/effets/laine.ogg')
		self.image = pygame.Surface([28, 30], pygame.SRCALPHA, 32)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.image_normal = pygame.image.load(f"images/gui/jeu/laine_{self.couleur}.png").convert_alpha()
		self.rect_image = self.image_normal.get_rect()
		self.font = pygame.font.SysFont("comicsansms", 12)

		self.dessiner(etat)

	def dessiner(self, etat):
		self.image.blit(self.image_normal, self.rect_image)
		# if etat == "survol":
		# 	texte = self.font.render(self.case, True, (255, 255, 255))
		# 	texte_rect = texte.get_rect(center=(28 // 2, 30 // 2))
		# 	self.image.blit(texte, texte_rect)

	def executerCommande(self, couleur, son_active):
		self.image_normal = pygame.image.load(f"images/gui/jeu/laine_{couleur}.png").convert_alpha()

	def jouerSon(self):
		# On joue l'effet sonore du bouton
		self.son_clic.play()


class Changement:
	def __init__(self, application, *groupes):
		self._fenetre = application.fenetre
		self.tour = application.tour
		self.gauche_presse = True
		self.droit_presse = True
		application.fond = (128, 128, 128)
		if self.tour == "J1":
			self.grille = pygame.image.load("images/gui/jeu/changement1.png")
		elif self.tour == "J2":
			self.grille = pygame.image.load("images/gui/jeu/changement2.png")
		self.rectGrille = self.grille.get_rect()
		self.rectGrille.center = (surfaceW / 2, surfaceH / 2)
		# Boutons Menu
		self._boutons = []
		b = OkBouton('ok', "", 640, 480, application.jeu)
		self._boutons.append(b)
		for groupe in groupes:
			groupe.add(b)
		# items2 = (
		# 	('pas_ok', application.jeu),
		# 	('ok', application.jeu),
		# )
		# x = 300
		# y = 530
		# for nom, cmd in items2:
		# 	b = OkBouton(
		# 		nom,
		# 		"",
		# 		x,
		# 		y,
		# 		cmd
		# 	)
		# 	self._boutons.append(b)
		# 	x += 650
		# 	for groupe in groupes:
		# 		groupe.add(b)

	def update(self, application, events):
		self._fenetre.blit(self.grille, self.rectGrille)
		clicGauche = pygame.mouse.get_pressed()[0]
		clicDroit = pygame.mouse.get_pressed()[2]
		posPointeur = pygame.mouse.get_pos()
		for bouton in self._boutons:
			# Si le pointeur souris est au-dessus d'un bouton
			if bouton.rect.collidepoint(*posPointeur):
				# Changement du curseur par un quelconque
				pygame.mouse.set_cursor(*pygame.cursors.tri_left)
				# Changement de la couleur du bouton
				bouton.dessiner("survol")
				# Si le clic gauche a été pressé
				if clicGauche:
					if not self.gauche_presse:
						self.gauche_presse = True
						if bouton.nom == "ok":
							if self.tour == "J1":
								application.tour = "J2"
							elif self.tour == "J2":
								application.tour = "J1"
						elif bouton.nom == "pas_ok":
							if self.tour == "J1":
								application.flotte2["tirs"].pop(-1)
								application.flotte2["effets"].pop(-1)
							elif self.tour == "J2":
								application.flotte1["tirs"].pop(-1)
								application.flotte1["effets"].pop(-1)
						bouton.executerCommande(application.sons)
				else:
					self.gauche_presse = False
				break
			else:
				# Le pointeur n'est pas au-dessus du bouton
				bouton.dessiner("normal")
		else:
			# Le pointeur n'est pas au-dessus d'un des boutons
			# initialisation au pointeur par défaut
			pygame.mouse.set_cursor(*pygame.cursors.arrow)


class OkBouton(pygame.sprite.Sprite):
	""" Création d'un simple bouton rectangulaire """

	def __init__(self, nom, etat, x, y, commande, option=False):
		super().__init__()
		self.nom = nom
		self._commande = commande
		self.option = option
		self.image = pygame.Surface((50, 52))
		self.son_clic = pygame.mixer.Sound('sons/effets/click.ogg')

		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		self.image_normal = pygame.image.load(f"images/gui/jeu/{nom}.png").convert_alpha()
		self.image_survol = pygame.image.load(f"images/gui/jeu/{nom}_hovered.png").convert_alpha()
		self.rect_image = self.image_normal.get_rect()

		self.dessiner(etat)

	def dessiner(self, etat):
		if etat == "survol":
			self.image.blit(self.image_survol, self.rect_image)
		else:
			self.image.blit(self.image_normal, self.rect_image)

	def executerCommande(self, son_active):
		# On joue l'effet sonore du bouton
		if son_active:
			self.son_clic.play()
		# Appel de la commande du bouton
		self._commande()


class Options:
	""" Simulacre de l'interface des options """

	def __init__(self, application, *groupes):
		self._fenetre = application.fenetre
		application.fond = (128, 128, 128)
		self.options = pygame.image.load("images/gui/jeu/options.png")
		self.rectOptions = self.options.get_rect()
		self.rectOptions.center = (surfaceW / 2, surfaceH / 2)
		self.image_ok = pygame.image.load("images/gui/jeu/ok.png").convert_alpha()
		self.image_ok_hovered = pygame.image.load("images/gui/jeu/ok_hovered.png").convert_alpha()
		self.image_pas_ok = pygame.image.load("images/gui/jeu/pas_ok.png").convert_alpha()
		self.image_pas_ok_hovered = pygame.image.load("images/gui/jeu/pas_ok_hovered.png").convert_alpha()
		self._boutons = []
		items2 = (
			('ok' if application.musique else 'pas_ok', application.nothing, "musique"),
			('ok' if application.sons else 'pas_ok', application.nothing, "sons")
		)
		x = 800
		y = 305
		for nom, cmd, option in items2:
			b = OkBouton(
				nom,
				"",
				x,
				y,
				cmd,
				option
			)
			self._boutons.append(b)
			y += 130
			for groupe in groupes:
				groupe.add(b)
		self._boutons_menu = []
		b = MenuBouton('quitter', "", 640, 600, application.menu)
		self._boutons_menu.append(b)
		for groupe in groupes:
			groupe.add(b)

	def update(self, application, events):
		self._fenetre.blit(self.options, self.rectOptions)
		clicGauche = pygame.mouse.get_pressed()[0]
		clicDroit = pygame.mouse.get_pressed()[2]
		posPointeur = pygame.mouse.get_pos()
		for bouton in self._boutons:
			# Si le pointeur souris est au-dessus d'un bouton
			if bouton.rect.collidepoint(*posPointeur):
				# Changement du curseur par un quelconque
				pygame.mouse.set_cursor(*pygame.cursors.tri_left)
				# Changement de la couleur du bouton
				bouton.dessiner("survol")
				# Si le clic gauche a été pressé
				if clicGauche:
					if not self.gauche_presse:
						self.gauche_presse = True
						if bouton.nom == "ok":
							if bouton.option == "musique":
								application.musique = False
								pygame.mixer.music.stop()
							elif bouton.option == "sons":
								application.sons = False
							bouton.nom = "pas_ok"
							bouton.image_normal = self.image_pas_ok
							bouton.image_survol = self.image_pas_ok_hovered
						elif bouton.nom == "pas_ok":
							if bouton.option == "musique":
								application.musique = True
								pygame.mixer.music.play(-1)
							elif bouton.option == "sons":
								application.sons = True
							bouton.nom = "ok"
							bouton.image_normal = self.image_ok
							bouton.image_survol = self.image_ok_hovered
						bouton.executerCommande(application.sons)
				else:
					self.gauche_presse = False
				break
			else:
				# Le pointeur n'est pas au-dessus du bouton
				bouton.dessiner("normal")
		for bouton in self._boutons_menu:
			# Si le pointeur souris est au-dessus d'un bouton
			if bouton.rect.collidepoint(*posPointeur):
				# Changement du curseur par un quelconque
				pygame.mouse.set_cursor(*pygame.cursors.tri_left)
				# Changement de la couleur du bouton
				bouton.dessiner("survol")
				# Si le clic gauche a été pressé
				if clicGauche:
					# Appel de la fonction du bouton
					bouton.executerCommande(application.sons)
				break
			else:
				# Le pointeur n'est pas au-dessus du bouton
				bouton.dessiner("normal")
		else:
			# Le pointeur n'est pas au-dessus d'un des boutons
			# initialisation au pointeur par défaut
			pygame.mouse.set_cursor(*pygame.cursors.arrow)


class Vainqueur:
	def __init__(self, application, *groupes):
		application.flotte1 = flottes.initialisation_flotte_vide()
		application.flotte2 = flottes.initialisation_flotte_vide()
		self._fenetre = application.fenetre
		self.gagnant = application.gagnant
		self.gauche_presse = True
		self.droit_presse = True
		application.fond = (128, 128, 128)
		self.grille = pygame.image.load(f"images/gui/jeu/gagne_{self.gagnant}.png")
		self.rectGrille = self.grille.get_rect()
		self.rectGrille.center = (surfaceW / 2, surfaceH / 2)
		# Boutons Menu
		self._boutons = []
		b = OkBouton('ok', "", 640, 480, application.menu)
		self._boutons.append(b)
		for groupe in groupes:
			groupe.add(b)

	def update(self, application, events):
		self._fenetre.blit(self.grille, self.rectGrille)
		clicGauche = pygame.mouse.get_pressed()[0]
		clicDroit = pygame.mouse.get_pressed()[2]
		posPointeur = pygame.mouse.get_pos()
		for bouton in self._boutons:
			# Si le pointeur souris est au-dessus d'un bouton
			if bouton.rect.collidepoint(*posPointeur):
				# Changement du curseur par un quelconque
				pygame.mouse.set_cursor(*pygame.cursors.tri_left)
				# Changement de la couleur du bouton
				bouton.dessiner("survol")
				# Si le clic gauche a été pressé
				if clicGauche:
					if not self.gauche_presse:
						self.gauche_presse = True
						bouton.executerCommande(application.sons)
				else:
					self.gauche_presse = False
				break
			else:
				# Le pointeur n'est pas au-dessus du bouton
				bouton.dessiner("normal")
		else:
			# Le pointeur n'est pas au-dessus d'un des boutons
			# initialisation au pointeur par défaut
			pygame.mouse.set_cursor(*pygame.cursors.arrow)


class Application:
	""" Classe maîtresse gérant les différentes interfaces du jeu """

	def __init__(self):
		pygame.mixer.pre_init(44100, -16, 1, 512)
		pygame.init()
		pygame.display.set_caption("Bataille navale")
		self.icone = pygame.image.load("images/icone_bateau.png")
		pygame.display.set_icon(self.icone)
		pygame.mixer.music.load('sons/musiques/main_menu.mp3')
		pygame.mixer.music.play(-1)
		self.flotte1 = flottes.initialisation_flotte_vide()
		self.flotte2 = flottes.initialisation_flotte_vide()
		self.tour = "J1"
		self.n_joueur = 2
		self.mode = "solo"
		self.gagnant = ""
		self.sons = True
		self.musique = True
		self.fond = (150,) * 3
		self.fenetre = pygame.display.set_mode((surfaceW, surfaceH))
		# Groupe de sprites utilisé pour l'affichage
		self.groupeGlobal = pygame.sprite.Group()
		self.statut = True

	def _initialiser(self):
		try:
			self.ecran.detruire()
			# Suppression de tous les sprites du groupe
			self.groupeGlobal.empty()
		except AttributeError:
			pass

	def menu(self):
		# Affichage du menu
		self._initialiser()
		self.groupeGlobal.empty()
		self.fond = (150,) * 3
		self.ecran = Menu(self, self.groupeGlobal)

	def jeu(self):
		# Affichage du jeu
		self._initialiser()
		self.groupeGlobal.empty()
		self.fond = (150,) * 3
		self.ecran = Jeu(self, self.groupeGlobal)

	def positionnement(self):
		# Affichage du jeu
		self._initialiser()
		self.groupeGlobal.empty()
		self.fond = (150,) * 3
		self.ecran = Positionnement(self, self.groupeGlobal)

	def changement(self):
		self._initialiser()
		self.groupeGlobal.empty()
		self.fond = (150,) * 3
		self.ecran = Changement(self, self.groupeGlobal)

	def vainqueur(self):
		self._initialiser()
		self.groupeGlobal.empty()
		self.fond = (150,) * 3
		self.ecran = Vainqueur(self, self.groupeGlobal)

	def options(self):
		# Affichage des options
		self._initialiser()
		self.groupeGlobal.empty()
		self.fond = (150,) * 3
		self.ecran = Options(self, self.groupeGlobal)

	def quitter(self):
		self.statut = False

	def nothing(self):
		pass

	def update(self):
		events = pygame.event.get()

		for event in events:
			if event.type == pygame.QUIT:
				self.quitter()
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.groupeGlobal.empty()
					self.fond = (150,) * 3
					self.menu()

		self.fenetre.fill(self.fond)
		self.ecran.update(self, events)
		self.groupeGlobal.update()
		self.groupeGlobal.draw(self.fenetre)
		pygame.display.update()


def main():

	flotte1 = flottes.initialisation_flotte_vide()
	flotte2 = flottes.initialisation_flotte_vide()
	# flotte2["tirs"].extend(["A1", "A2", "A3", "A4", "A5", "A6", "B1", "D4"])
	# flotte2["effets"].extend(["touche", "touche", "touche", "touche"])
	# print(flotte2)

	app = Application()
	app.menu()

	clock = pygame.time.Clock()

	while app.statut:
		app.update()
		clock.tick(30)

	pygame.quit()


if __name__ == '__main__':
	main()
