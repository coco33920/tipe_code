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
		# Ce fichier contient la définition de la classe 'Entité'. Les entités se 
		# déplacent de case en case et peuvent, selon les circonstances, se contaminer 
		# entre-elles.

	# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------



# -------------------------------- Importations(s) --------------------------------
from copy import deepcopy

from random import choice, uniform																	# Pour choisir aléatoirement une cases parmi celles disponibles pour le déplacement des entités.

# ---------------------------------------------------------------------------------



# -------------------------------- Classe(s) --------------------------------
class Entite:
	'''
		Définition de la classe 'Entite'.

	'''



	# -------------------------------- Constructeur --------------------------------
	def __init__(self, case_courante, **parametres):
		'''
			Constructeur de la classe 'Entite'.

			---------------- Paramètre(s) ----------------
				'case_courante' : un objet de type 'Case' qui représente la case sur laquelle 
				se trouve l'entité concernée.

				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble 
				des paramètres propres à l'entité. Ces paramètres (qui sont à définir soigneusement par 
				l'utilisateur) permettent de rendre la simulation 'plus naturelle'.

			----------------------------------------------

		'''

		# On initialise les différents champs de l'objet 'Entite'.
		self.case_courante = case_courante

		# 'sante' (optionnel, par défaut : 0) : caractérise la santé de l'entité ; 
		# 0 pour saine et 1 pour contaminée.

		# 'etat' (optionnel, par défaut : 0) : entier naturel qui caractérise l'état de 
		# l'entité (0 pour près à marcher et sinon, compte le nombre de tour (de boucle) 
		# restant avant de pouvoir marcher à nouveau).

		# 'taux_dispersion' (optionnel, par défaut : .2) : un réel entre 0 (inclus) et 
		# 1 (exclus !) qui caractérise la probabilité que l'entité, si elle est contaminée, 
		# diffuse son virus sur la case où elle se trouve.

		# 'taux_contagion' (optionnel, par défaut : 1.) : un réel entre 0 et 1 (inclus) 
		# qui caractérise la probabilité que, si l'entité est exposée au virus, celle-ci 
		# devienne contaminée (si elle ne l'est pas déjà).
		self.parametres = {'sante' : 0, 'etat' : 0, 'taux_dispersion' : .01, 'taux_contagion' : 1.}
		self.parametres.update(parametres)

		# On fait entrer l'entité sur la case à laquelle elle a été assignée.
		self.case_courante.entrer(self)

	# ------------------------------------------------------------------------------



	# -------------------------------- Méthodes(s) --------------------------------
	def avancer(self):
		'''
			Fonction 'avancer' qui gère la marche de l'entité concernée sur les différentes 
			cases possibles.

		'''

		liste_cases_disponibles = self.case_courante.liste_cases_disponibles						# Obtention des informations sur l'emplacement de l'entité concernée.

		self.update_parametres()																	# Pour mettre à jour les paramètres de l'individu concerné.
		if self.parametres['etat'] == 0:															# Si l'entité concernée peut avancer.
			if liste_cases_disponibles != []:														# Si l'entité concernée peut rejoindre de nouvelles cases.
				self.case_courante.sortir(self)														# On fait sortir de la case courante l'entité concernée.

				self.case_courante = choice(liste_cases_disponibles)								# On choisi aléatoirement une nouvelle case parmi celles qui sont accessibles et on met à jour l'information sur l'entité.
				self.case_courante.entrer(self)														# On fait rentrer l'entité concernée sur une nouvelle case (parmi celles accessibles via la case courante).
				self.update_parametres()															# Pour mettre à jour les paramètres de l'individu concerné.

		else:																						# Sinon, si l'individu ne doit pas bouger de sa case.
			self.parametres['etat'] -= 1															# On décrémente le nombre de tour (de boucle) qu'il reste l'entité concernée avant de pouvoir avancer de nouveau.


	def update_parametres(self):
		'''
			Fonction 'update_parametres' qui gère la modification des différents paramètres de 
			l'entité concernée.

		'''

		if self.parametres['sante'] == 0:															# Si l'entité concernée est saine.
			# On calcul l'état de santé de l'entité 'entite' selon les différents paramètres qui rentrent en compte (taux de contagion du virus, taux de dispersion, taux de présence...).
			if (uniform(0, 1) <= self.parametres['taux_contagion'] * self.case_courante.parametres['taux_dispersion'] * self.case_courante.parametres['taux_presence']):
				self.parametres['sante'] = 1
				self.case_courante.entrer(self)

	# -----------------------------------------------------------------------------



class Source:
	'''
		Définition de la classe 'Source'.

	'''



	# -------------------------------- Constructeur --------------------------------
	def __init__(self, nombre_entite, contamination, case_depart):
		'''
			Constructeur de la classe 'Source'.

			---------------- Paramètre(s) ----------------
				'entite_type' : un objet de type 'Entite' qui correspond au profil type des entités 
				à envoyer à chaque tour (de boucle).

				'taux_contamine' (optionnel, par défaut : 0.1) : un réel entre 0 et 1 (inclus) qui 
				gère la probabilité qu'une entité émise par la source concernée soit contaminée ou 
				saine.

				'nombre_entites' (optionnel, par défaut : 5) : un entier naturel non nul qui caractérise 
				le nombre total d'entités à envoyer (un entité envoyée par tour (de boucle)).
				au total).

			----------------------------------------------

		'''

		# On initialise les différents champs de l'objet 'Source'.
		self.case = case_depart
		self.nombre = nombre_entite
		self.contamination = contamination
	# ------------------------------------------------------------------------------



	# -------------------------------- Méthodes(s) --------------------------------
	def envoyer(self):
		'''
			Fonction 'envoyer' qui gère l'envoie d'entité sur le 'graphe' selon la source concernée.

			---------------- Paramètre(s) ----------------
				'graphe' : un dictionnaire (c.f. construction du graphe pour le déplacement 
				des entités) qui contient la structure de la carte où se déplace les entités.

			----------------------------------------------

		'''
		if(self.nombre == 0):
			return (None)
		
		a = uniform(0,1)
		entite = Entite(self.case)
		entite.parametres['sante'] = (a<=self.contamination)
		self.nombre -= 1
		return (entite)
		

	# -----------------------------------------------------------------------------

# ---------------------------------------------------------------------------
