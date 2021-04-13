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
		# Ce fichier contient la définition de la classe 'Simulation'. Elle permet de 
		# faciliter la création de simulations et offre diverses options (enregistrement
		# de simulation, tracé de graphiques, ...).

	# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------



# -------------------------------- Importation(s) --------------------------------
import sys
from copy import deepcopy

from classes.Village import Village, charger_village_via_dictionnaire

from utilitaire.Sauvegarde import enregistrer
from utilitaire.Liste import retailler

# --------------------------------------------------------------------------------



# -------------------------------- Classe(s) --------------------------------
class Simulation:
	'''
		Définition de la classe 'Simulation'.

	'''



	# -------------------------------- Constructeur --------------------------------
	def __init__(self, **parametres):
		'''
			Constructeur de la classe 'Simulation'.

			---------------- Paramètre(s) ----------------
				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble
				des paramètres propres à la simulation. Ces paramètres (qui sont à définir soigneusement par
				l'utilisateur) permettent de rendre la simulation 'plus naturelle'.

			----------------------------------------------

		'''

		# On initialise les différents champs de l'objet 'Simulation'.
		self.parametres = {**{'village' : Village(), 'nombre_points' : 10, 'temps_mesure' : 10, 'nombre_simulations' : 1000, 'indice_debut' : 0, 'temps' : 0, 'liste_temps' : [], 'liste_total_contaminees' : [], 'liste_nouveaux_contamines' : [], 'liste_contaminees_restants' : []}, **parametres} # Permet la 'concaténation' des deux dictionnaires.

		# Construction de la liste des temps des différentes mesures.
		# Construction de la liste comptant le nombre total d'entités qui ont été contaminées durant la simulation.
		# Construction de la liste comptant le nombre de nouvelles entités qui ont été contaminées entre deux instants consécutifs.
		# Construction de la liste comptant le nombre d'entités contaminées présentes dans le village.

	# ------------------------------------------------------------------------------



	# -------------------------------- Méthodes(s) --------------------------------
	def lancer(self, affichage = True, temps_affichage = 500):
		'''
			Fonction 'lancer' qui permet de mettre en œuvre la simulation concernée.

			---------------- Paramètre(s) ----------------
				'affichage' (optionnel, par défaut : True) : un booléen qui gère l'affichage ou non 
				d'informations/d'avertissement/d'erreurs qui peuvent se produire au cours de la 
				simulation.

				'temps_affichage' (optionnel, par défaut : 1000) : un entier naturel strictement positif qui 
				permet de contrôler à quelle fréquence il faut afficher l'information concernant le nombre 
				de simulations déjà effectuées.

			----------------------------------------------

		'''

		self.parametres['liste_temps'] = [self.parametres['temps_mesure'] * points for points in range(self.parametres['nombre_points'])]
		self.parametres['liste_total_contaminees'] = retailler(self.parametres['liste_total_contaminees'], self.parametres['nombre_points'])
		self.parametres['liste_contaminees_restants'] = retailler(self.parametres['liste_contaminees_restants'], self.parametres['nombre_points'])

		while self.parametres['indice_debut'] < self.parametres['nombre_simulations']:
			village = deepcopy(self.parametres['village'])

			temps = self.parametres['temps']
			try:
				while temps < self.parametres['temps_mesure'] * self.parametres['nombre_points']:
					if temps % self.parametres['temps_mesure'] == 0:
						indice = temps // self.parametres['temps_mesure']

						self.parametres['liste_total_contaminees'][indice] += village.parametres['entites_malades_village'] + village.parametres['entites_malades_retirees']
						self.parametres['liste_contaminees_restants'][indice] += village.parametres['entites_malades_village']

					village.mettre_a_jour()
					temps += 1

			except KeyboardInterrupt:
				print("[Information] : demande d'arrêt de la simulation. Enregistrement...")
				return None

			if affichage == True and self.parametres['indice_debut'] % temps_affichage == 0:
				print("[Information] : simulation", self.parametres['indice_debut'], "effectuée.")

			self.parametres['temps'] = 0
			self.parametres['indice_debut'] += 1


	def sauvegarder(self):
		'''
			Fonction 'sauvegarder' qui permet d'enregistrer l'ensemble des paramètres 
			de la simulation concernée. Cette fonction renvoie un dictionnaire qui correspond 
			à la simulation enregistrée.

		'''

		dictionnaire_sauvegarde = deepcopy(self.__dict__)
		dictionnaire_sauvegarde['parametres']['village'] = self.parametres['village'].sauvegarder()

		return dictionnaire_sauvegarde

	# -----------------------------------------------------------------------------

# ---------------------------------------------------------------------------



# -------------------------------- Fonctions(s) --------------------------------
def charger_simulation_via_dictionnaire(dictionnaire):
	'''
		

	'''

	dictionnaire['parametres']['village'] = charger_village_via_dictionnaire(dictionnaire['parametres']['village'])
	return Simulation(**dictionnaire['parametres'])

# ------------------------------------------------------------------------------
