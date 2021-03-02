#!/usr/bin/python3
# -*- coding: utf-8 -*-



# -------------------------------- Introduction --------------------------------
	# -------------------------------- License --------------------------------
		# MIT License

		# Copyright (c) 2021 [Noms des propriétaires].

		# Permission is hereby granted, free of charge, to any person obtaining a copy
		# of this software and associated documentation files (the "Software"), to deal
		# in the Software without restriction, including without limitation the rights
		# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
		# copies of the Software, and to permit persons to whom the Software is
		# furnished to do so, subject to the following conditions:

		# The above copyright notice and this permission notice shall be included in all
		# copies or substantial portions of the Software.

		# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
		# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
		# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
		# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
		# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
		# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
		# SOFTWARE.

	# -------------------------------------------------------------------------



	# -------------------------------- Description --------------------------------
		# Ce fichier est le fichier principal du projet. Il contient la définition de la classe 
		# 'Village' qui permet de mettre en œuvre le projet.

	# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------


# -------------------------------- Importation(s) --------------------------------
from classes.Case import Case, Magasin
from classes.Entite import Entite, Source

from utilitaire.Courbes import Courbe
from utilitaire.Interpolation import Interpolation, sigmoide_asymetrique_5, sigmoide_asymetrique_generalisee, fonction_logistique_generalisee

import numpy as numpy

# --------------------------------------------------------------------------------



# -------------------------------- Classe(s) --------------------------------
class Village:
	'''
		Définition de la classe 'Village'.

	'''



	# -------------------------------- Constructeur --------------------------------
	def __init__(self, liste_entites = [], liste_sources = [], **parametres):
		'''
			Constructeur de la classe 'Village'.

			---------------- Paramètre(s) ----------------
				'liste_entites' (optionnel, par défaut : []) : c'est une liste d'éléments de type 
				'Entite' qui correspond à l'ensemble des entités présentes dans le village.

				'liste_sources' (optionnel, par défaut []) : c'est une liste d'éléments de type 
				'Source' qui correspond à l'ensemble des points qui permettent l'émission d'entités 
				dans le village à chaque tour (de boucle).

				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble 
				des paramètres propres au village. Ces paramètres (qui sont à définir soigneusement par 
				l'utilisateur) permettent de rendre la simulation 'plus naturelle'.

			----------------------------------------------

		'''

		# On initialise les différents champs de l'objet 'Village'.
		self.liste_entites = liste_entites
		self.liste_sources = liste_sources

		self.parametres = parametres

	# ------------------------------------------------------------------------------



	# -------------------------------- Méthodes(s) --------------------------------
	def mettre_a_jour(self):
		'''
			Fonction 'mettre_a_jour' qui gère la mise à jour du village dans son intégralité (soit, 
			elle assure en autre : la marche des entités, l'évolution de leurs paramètres ainsi que 
			ceux des cases...).

		'''

		#print(['1' if entite.parametres['sante'] else ' ' for entite in self.liste_entites])
		#print([entite.case_courante.parametres['taux_presence'] for entite in self.liste_entites])
		for entite in self.liste_entites:
			entite.avancer()


	def update_parametres(self):
		'''
			Fonction 'update_parametres' qui gère la modification des différents paramètres du 
			village concerné.

		'''

		pass

	# -----------------------------------------------------------------------------

# ---------------------------------------------------------------------------



# -------------------------------- Main --------------------------------
if __name__ == '__main__':																			# Instruction principale du programme.
	nb_points = 100
	temps_mesure = 5
	nb_simulations = 10000

	abscisses = [temps_mesure * k for k in range(nb_points)]
	ordonnees = [0] * nb_points

	for k in range(nb_simulations):
		case_1 = Case()

		village = Village([Entite(case_1, sante = 1), Entite(case_1), Entite(case_1)])

		for _ in range(abscisses[-1] + 1):
			if _ % temps_mesure == 0:
				ordonnees[_ // temps_mesure] += sum([entite.parametres['sante'] for entite in village.liste_entites])
			village.mettre_a_jour()

		if k % 1000 == 0:print('Simulation', k)

	ordonnees = numpy.divide(ordonnees, nb_simulations)


	#abscisses = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 320]
	#ordonnees = [1, 1.07, 1.42, 2.56, 4.08, 6.08, 8.3, 10.6, 13.0, 15.1, 17.1, 18.6, 20.0, 21.0, 21.9, 22.4, 22.8, 23.2, 23.4, 23.6, 23.7, 23.8, 23.8, 23.9, 23.9, 23.999]
	print(abscisses)
	print(ordonnees)
	print()


	courbe = Courbe(abscisses, ordonnees)

	modele = Interpolation(courbe, sigmoide_asymetrique_generalisee)
	parametres = modele.interpoler(maxfev = 100000)
	print(parametres)

	courbe.tracer('o')
	modele.tracer_interpolation(parametres[0])

	courbe.afficher()


# ----------------------------------------------------------------------
