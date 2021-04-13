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
		# Ce fichier facilite en quelques sortes l'interpolation des différentes données 
		# obtenues lors des simulations pour ce projet. Les calculs reposent pour la plupart 
		# grâce au module scipy et à la fonction 'curve_fit' (c.f. 
		# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html pour 
		# plus de renseignements).

	# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------



# -------------------------------- Importation(s) --------------------------------
from scipy.optimize import curve_fit

import numpy as numpy

from utilitaire.Courbes import Courbe

# --------------------------------------------------------------------------------



# -------------------------------- Classe(s) --------------------------------
class Interpolation:
	'''
		Définition de la classe 'Interpolation'.

	'''



	# -------------------------------- Constructeur --------------------------------
	def __init__(self, courbe, fonction_modele):
		'''
			Constructeur de la classe 'Interpolation'.

			---------------- Paramètre(s) ----------------
				'courbe' : un objet de type 'Courbe' qui représente la courbe à interpoler.

				'fonction_modele' : c'est une fonction dont le premier argument est l'inconnue et les autres 
				arguments sont les paramètres associés au modèle concerné.

			----------------------------------------------

		'''

		# On initialise les différents champs de l'objet 'Interpolation'.
		self.courbe = courbe

		self.fonction_modele = fonction_modele

	# ------------------------------------------------------------------------------


	# -------------------------------- Méthodes(s) --------------------------------
	def interpoler(self, **parametres):
		'''
			Fonction 'interpoler' qui permet de "trouver" les valeurs des paramètres du modèle (ou, au moins 
			d'en trouver des valeurs adéquates) associé à l'objet 'Interpolation' concerné.

			---------------- Paramètre(s) ----------------
				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble 
				des paramètres propres à la l'interpolation. Ces paramètres sont ceux définis pour la fonction 
				'curve_fit' du module scipy (voir https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html 
				pour une liste détaillée).

			----------------------------------------------

		'''

		return curve_fit(self.fonction_modele, self.courbe.liste_points_abscisses, self.courbe.liste_points_ordonnees, **parametres)


	def tracer_interpolation(self, modele_interpole, **parametres):
		'''
			Fonction 'tracer_interpolation' qui permet de tracer le modèle une fois interpolé.

			---------------- Paramètre(s) ----------------
				'modele_interpole' : c'est une liste de réels qui contient les valeurs les plus adéquates du modèle.
				'c.f. la fonction 'interpoler').

				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble 
				des paramètres propres à la courbe. Ces paramètres sont ceux définis pour la fonction 
				'plot' du module matplotlib (voir https://matplotlib.org/3.3.4/api/_as_gen/matplotlib.pyplot.plot.html 
				pour une liste détaillée).

			----------------------------------------------

		'''

		points_ordonnees = self.fonction_modele(self.courbe.liste_points_abscisses, *modele_interpole)
		Courbe(self.courbe.liste_points_abscisses, points_ordonnees).tracer(**parametres)

	# -----------------------------------------------------------------------------

# ---------------------------------------------------------------------------



# -------------------------------- Fonction(s) --------------------------------
def sigmoide_asymetrique_5(x, a, b, c, d, m):
	'''
		Fonction 'sigmoide_asymetrique_5' qui représente le modèle d'une sigmoïde asymétrique à 1 
		inconnue réelle et 5 paramètres réels.

		---------------- Paramètre(s) ----------------
			'x' : c'est une variable réelle.

			'a', 'b', 'c', 'd' et 'm' : des réels qui représentent les divers paramètres du modèle qui 
			devront être ajuster au mieux lors de la phase d'interpolation.

		----------------------------------------------

	'''

	return sigmoide_asymetrique_generalisee(x, a, b, c, d, 1, 1, m)


def sigmoide_asymetrique_generalisee(x, a, b, c, d, e, f, m):
	'''
		Fonction 'sigmoide_asymetrique_generalisee' qui représente le modèle d'une sigmoïde asymétrique à 1 
		inconnue réelle et 7 paramètres réels.

		---------------- Paramètre(s) ----------------
			'x' : c'est une variable réelle.

			'a', 'b', 'c', 'd', 'e', 'f' et 'm' : des réels qui représentent les divers paramètres du modèle qui 
			devront être ajuster au mieux lors de la phase d'interpolation.

		----------------------------------------------

	'''

	return d + (a - d) / (e + f * numpy.divide(x, c)**b)**m


def fonction_logistique_3(x, a, b, c):
	'''
		Fonction 'fonction_logistique_3' qui représente le modèle d'une fonction logistique à 1 
		inconnue réelle et 3 paramètres réels.

		---------------- Paramètre(s) ----------------
			'x' : c'est une variable réelle.

			'a', 'b' et 'c' : des réels qui représentent les divers paramètres du modèle qui 
			devront être ajuster au mieux lors de la phase d'interpolation.

		----------------------------------------------

	'''

	return fonction_logistique_generalisee(x, 0, b, 1, d, e, 1, 0)


def fonction_logistique_generalisee(x, a, b, c, d, e, f, g):
	'''
		Fonction 'fonction_logistique_generalisee' qui représente le modèle d'une fonction logistique à 1 
		inconnue réelle et 7 paramètres réels.

		---------------- Paramètre(s) ----------------
			'x' : c'est une variable réelle.

			'a', 'b', 'c', 'd', 'e', 'f' et 'g' : des réels qui représentent les divers paramètres du modèle qui 
			devront être ajuster au mieux lors de la phase d'interpolation.

		----------------------------------------------

	'''

	return a + (b - a) / (c + d * numpy.exp(- numpy.array(x - g) * e))**(1 / f)

# -----------------------------------------------------------------------------

