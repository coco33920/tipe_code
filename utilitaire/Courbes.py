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
		# Ce fichier facilite en quelques sortes le tracé des courbes (via les différentes données 
		# obtenues) lors des simulations pour ce projet. Les calculs reposent pour la plupart 
		# grâce au module matplotlib et à la fonction 'plot' (c.f. 
		# https://matplotlib.org/3.3.4/api/_as_gen/matplotlib.pyplot.plot.html pour plus de renseignements).

	# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------



# -------------------------------- Importation(s) --------------------------------
import matplotlib.pyplot as plot

# --------------------------------------------------------------------------------



# -------------------------------- Classe(s) --------------------------------
class Courbe:
	'''
		Définition de la classe 'Courbe'.

	'''



	# -------------------------------- Constructeur --------------------------------
	def __init__(self, liste_points_abscisses, liste_points_ordonnees):
		'''
			Constructeur de la classe 'Courbe'.

			---------------- Paramètre(s) ----------------
				'liste_points_abscisses' : c'est une liste de réels contenant l'ensemble des abscisses 
				des points à tracer.

				'liste_points_ordonnees' : c'est une liste de réels contenant l'ensemble des ordonnées 
				des points à tracer.

			----------------------------------------------

		'''

		# On initialise les différents champs de l'objet 'Courbe'.
		self.liste_points_abscisses = liste_points_abscisses
		self.liste_points_ordonnees = liste_points_ordonnees

	# ------------------------------------------------------------------------------


	# -------------------------------- Méthodes(s) --------------------------------
	def tracer(self, *arguments, **parametres):
		'''
			Fonction 'tracer' qui permet de tracer les points associés à la courbe concernée 
			grâce au module matplotlib.

			---------------- Paramètre(s) ----------------
				'arguments' (optionnel, par défaut []) : c'est une liste qui contient l'ensemble des arguments 
				propres à la courbes. Ces arguments sont ceux définis pour la fonction 
				'plot' du module matplotlib (voir https://matplotlib.org/3.3.4/api/_as_gen/matplotlib.pyplot.plot.html 
				pour une liste détaillée).

				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble 
				des paramètres propres à la courbe. Ces paramètres sont ceux définis pour la fonction 
				'plot' du module matplotlib (voir https://matplotlib.org/3.3.4/api/_as_gen/matplotlib.pyplot.plot.html 
				pour une liste détaillée).

			----------------------------------------------

		'''

		plot.plot(self.liste_points_abscisses, self.liste_points_ordonnees, *arguments, **parametres)

	# -----------------------------------------------------------------------------

# ---------------------------------------------------------------------------



# -------------------------------- Fonction(s) --------------------------------
def afficher(self):
	'''
		Fonction 'afficher' qui permet d'afficher, grâce au module matplotlib, dans une fenêtre 
		graphique la courbe.

	'''

	plot.show()

# -----------------------------------------------------------------------------
