# coding: UTF-8
"""
Script: jeu_graphique.py
"""

import flottes
import outils
import pygame


class Menu:
	def __init__(self, application, *groupes):
		contenus = (
			("un_joueur", 50, 50, 'print("xd")'),
			("multijoueur", 50, 50, 'print("lol")')
		)
		self.conteneurs = []
		for nom, x, y, action in contenus:
			bouton = Conteneur(nom, x, y, action)
			self.conteneurs.append(bouton)


	def update(self):
		for conteneur in self.conteneurs:
			conteneur.dessiner((0, 200, 0))

	def detruire(self):
		pygame.mouse.set_cursor(*pygame.cursors.arrow)  # initialisation du pointeur


class Conteneur:
	def __init__(self, nom, x, y, action):
		super().__init__()
		self.nom = nom
		self.action = action
		self.surface = pygame.Surface((200, 20))
		self.image = pygame.image.load(f"images/gui/menu/{nom}.png")
		self.image_normal = pygame.image.load(f"images/gui/menu/{nom}.png")
		self.image_hovered = pygame.image.load(f"images/gui/menu/{nom}_hovered.png")
		self.r = self.image.get_rect()
		self.x = x
		self.y = y
		self.r.x = x
		self.r.y = y

	def dessiner(self, etat):
		self.surface.fill(etat)
		self.image.blit(self.image_normal, (self.x, self.y))

	def clic(self):
		exec(self.action)


class Application:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Ceci est le titre")
		self.fenetre = pygame.display.set_mode((600, 600))
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
		self.ecran = Menu(self, self.groupeGlobal)

	# def jeu(self):
	# 	# Affichage du jeu
	# 	self._initialiser()
	# 	self.ecran = Jeu(self, self.groupeGlobal)

	def quitter(self):
		self.statut = False

	def update(self):
		events = pygame.event.get()

		for event in events:
			if event.type == pygame.QUIT:
				self.quitter()
				return

		self.fenetre.fill((150,) * 3)
		self.ecran.update()
		self.groupeGlobal.update()
		self.groupeGlobal.draw(self.fenetre)
		pygame.display.update()

# Fonctions

def init_jeu():
	pygame.init()

	pygame.display.set_caption("Ceci est le titre")
	ecran = pygame.display.set_mode((600, 600))
	menu(ecran)

	pygame.quit()


def menu(ecran):
	i_water = 0
	image = Conteneur("un_joueur", 50, 50, 'print("xd")')
	image2 = Conteneur("multijoueur", 50, 150, 'print("lol")')
	fermer = False
	while not fermer:
		pygame.time.delay(50)
		i_water = (i_water + 1) % 36
		water_background = pygame.image.load(f"images/water_background/tmp-{i_water}.gif")
		ecran.blit(water_background, (0, 0))
		ecran.blit(image.image, (image.x, image.y))
		ecran.blit(image2.image, (image2.x, image2.y))
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				fermer = True
			image.etat()
			image2.etat()
		pygame.display.update()


def options(ecran):
	i_water = 0
	image = Conteneur("un_joueur", 50, 50, print("xd"))
	image2 = Conteneur("options", 50, 150, print("lol"))
	fermer = False
	while not fermer:
		pygame.time.delay(50)
		# i_water = (i_water + 1) % 36
		# water_background = pygame.image.load(f"images/water_background/tmp-{i_water}.gif")
		# ecran.blit(water_background, (0, 0))
		ecran.blit(image.image, (image.x, image.y))
		ecran.blit(image2.image, (image2.x, image2.y))
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				fermer = True
			image.etat()
			image2.etat()
		pygame.display.update()


# Programme principal
def main():
	flotte = {
		"bateaux": {
			"porte-avions": [
				"A1",
				"B1",
				"C1",
				"D1",
				"E1"
			],
			"croiseur": [
				"A3",
				"A4",
				"A5",
				"A6"
			],
			"contre-torpilleurs": [
				"J8",
				"J9",
				"J10"
			],
			"sous-marin": [
				"F1",
				"F2",
				"F3"
			],
			"torpilleur": [
				"D2",
				"E2"
			]
		},
		"tirs": [
			"A1",
			"A9",
			"D2",
			"E2",
			"F5",
			"J10"
		],
		"effets": [
			"touche",
			"eau",
			"touche",
			"coule",
			"eau",
			"eau"
		],
		"pseudo": "anonymous",
		"nbreTouche": 3,
		"nbreCoule": 1
	}
	flotte1 = flottes.initialisation_flotte_par_dictionnaire_fixe("flotte_presque_coulee")

	app = Application()
	app.menu()

	clock = pygame.time.Clock()

	while app.statut:
		app.update()
		clock.tick(30)

	pygame.quit()


if __name__ == '__main__':
	main()
