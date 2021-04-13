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
		# Ce fichier contient la définition de la classe 'Case'. Les cases constituent 
		# la base de la rue. Celle-ci peut se décliner de trois façon : une case standard, 
		# un magasin ou une source émettrice d'entités.

	# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------



# -------------------------------- Importation(s) --------------------------------
from numpy import inf

from copy import deepcopy

# --------------------------------------------------------------------------------



# -------------------------------- Variables(s) --------------------------------
compteur_cases = 0
dictionnaire_numeros_cases = {}

liste_cases_chargees = []

# ------------------------------------------------------------------------------



# -------------------------------- Classe(s) --------------------------------
class Case:
	'''
		Définition de la classe 'Case'.

	'''



	# -------------------------------- Constructeur --------------------------------
	def __init__(self, **parametres):
		'''
			Constructeur de la classe 'Case'.

			---------------- Paramètre(s) ----------------
				'parametres' (optionnel, par défaut {'liste_cases_disponibles' : [], 'taux_dispersion' : 1., 
				'taux_presence' : 0., 'capacite_contamination' : 0, 'capacite_case' : inf, 'temps_attente' : 0}) : 
				c'est un dictionnaire qui contient l'ensemble des paramètres propres à la case. Ces paramètres 
				(qui sont à définir soigneusement par l'utilisateur) permettent de rendre la simulation 'plus naturelle'.

			----------------------------------------------

		'''

		global compteur_cases, dictionnaire_numeros_cases

		# On initialise les différents champs de l'objet 'Case'.

		# 'dictionnaire_cases_poids_disponibles' (optionnel, par défaut : {}) : c'est un dictionnaire de la forme
		# 'Case' : poids qui correspond à l'ensemble des cases qui sont directement accessibles via la case concernée 
		# associée à une pondération (un réel positif) qui prend son importance lors que choix aléatoire de la marche 
		# des entités.

		# 'taux_dispersion' (optionnel, par défaut : 1.) : un réel entre 0 et 1 (inclus) 
		# qui caractérise la probabilité que, si une ou plusieurs entité(s) contaminée(s) 
		# se trouvent sur cette case, que le virus se diffuse à l'ensemble de la case et touche 
		# donc, potentiellement, les autres entités saines.

		# 'taux_presence' (optionnel, par défaut : 0.) : un réel entre 0 et 1 (inclus) 
		# qui caractérise la probabilité de présence du virus sur une case. Cette probabilité 
		# est influencée en fonction de l'état des entités qui s'y trouvent.

		# 'capacite_contamination' (optionnel, par défaut : 0) : un entier (à priori positif, ou inf - voir la 
		# bibliothèque NumPy) qui caractérise la capacité d'accueil maximale de la case concernée avant que les 
		# individus ne se contaminent inévitablement. Si fixé à 0, les individus se contaminent au fur et à 
		# mesure de leur arrivé sur la case concernée.

		# 'capacite_case' (optionnel, par défaut : inf) : un entier strictement positif (ou inf - voir la 
		# bibliothèque NumPy) qui caractérise le nombre maximal d'individus qui peuvent être présent sur la case.

		# 'temps_attente' (optionnel, par défaut : 0) : un entier positif qui caractérise le temps que doit attendre 
		# un individu placé sur la case concernée avant de pouvoir continuer à avancer vers d'autres cases.
		self.parametres = {**{'dictionnaire_cases_poids_disponibles' : {}, 'taux_dispersion' : 1., 'taux_presence' : 0., 'capacite_contamination' : 0, 'capacite_case' : inf, 'temps_attente' : 0}, **parametres} # Permet la 'concaténation' des deux dictionnaires.

		self.numero_case = compteur_cases
		dictionnaire_numeros_cases[self.numero_case] = self
		compteur_cases += 1

	# ------------------------------------------------------------------------------



	# -------------------------------- Méthodes(s) --------------------------------
	def mettre_a_jour(self, entite, mode = 1):
		'''
			Fonction 'mettre_a_jour' qui gère permet de mettre à jour

			---------------- Paramètre(s) ----------------
				'entite' : un objet de type 'Entite' qui correspond à l'entité qui 
				rentre sur la case concernée par l'action.

				'mode' (optionnel, par défaut 1) : un entier (soit -1 soit 1) qui caractérise 
				le type d'interaction de l'entité 'entite' avec la case concernée : 1 pour l'entrée 
				de cette entité sur la case courante, -1 si celle-ci sort de la case concernée.

			----------------------------------------------

		'''

		self.parametres['capacite_contamination'] -= mode
		self.parametres['capacite_case'] -= mode

		# On calcul le nouveau taux de présence du virus sur la case. Le calcul se fait via la formule de la 
		# probabilité d'une union. On considère (et il est naturel de faire ainsi) que les événements «se faire contaminer par 
		# l'entité A» et «se faire contaminer par l'entité B» sont indépendants.
		if entite.parametres['sante'] == 1:															# Si l'entité concernée par l'action est contaminée.
			# On met à jour le taux de présence du virus de la case concernée.
			self.parametres['taux_presence'] = 1. - (1. - self.parametres['taux_presence']) * ((1. - entite.parametres['taux_dispersion']) ** mode)


	def entrer(self, entite):
		'''
			Fonction 'entrer' qui gère l'entrée de l'entité 'entite' de la case 
			concernée.

			---------------- Paramètre(s) ----------------
				'entite' : un objet de type 'Entite' qui correspond à l'entité qui 
				entre sur la case concernée par l'action.

			----------------------------------------------

		'''

		entite.parametres['etat'] = self.parametres['temps_attente']
		self.mettre_a_jour(entite)


	def sortir(self, entite):
		'''
			Fonction 'sortir' qui gère la sortie de l'entité 'entite' de la case 
			concernée.

			---------------- Paramètre(s) ----------------
				'entite' : un objet de type 'Entite' qui correspond à l'entité qui 
				sort de la case concernée par l'action.

			----------------------------------------------

		'''

		self.mettre_a_jour(entite, -1)


	def sauvegarder(self, mode = 'json'):
		'''
			Fonction 'sauvegarder' qui permet d'enregistrer l'ensemble des paramètres 
			de la case concernée. Cette fonction renvoie un dictionnaire qui correspond 
			à la case enregistrée.

		'''

		dictionnaire_sauvegarde = deepcopy(self.__dict__)
		dictionnaire_sauvegarde['parametres']['dictionnaire_cases_poids_disponibles'] = {case.numero_case : poids for (case, poids) in self.parametres['dictionnaire_cases_poids_disponibles'].items()}

		return dictionnaire_sauvegarde

	# -----------------------------------------------------------------------------



class Structure:
	'''
		Définition de la classe 'Structure'.

	'''



# -------------------------------- Constructeur --------------------------------
	def __init__(self, **parametres):
		'''
			Constructeur de la classe 'Structure'.

			---------------- Paramètre(s) ----------------
				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble
				des paramètres propres à la structure. Ces paramètres (qui sont à définir soigneusement par
				l'utilisateur) permettent de rendre la simulation 'plus naturelle'.

			----------------------------------------------

		'''

		# On initialise les différents champs de l'objet 'Structure'.

		# 'liste_cases' (optionnel, par défaut []) : c'est une liste d'éléments de type
		# 'Case' qui correspond à l'ensemble des cases qui constituent la structure.
		self.parametres = {**{'liste_cases' : []}, **parametres} # Permet la 'concaténation' des deux dictionnaires.

	# ------------------------------------------------------------------------------



	# -------------------------------- Méthodes(s) --------------------------------
	def case(self, indice = 0):
		'''
			Fonction 'case' qui permet d'obtenir une case particulière de la structure concernée 
			étant donné son indice dans la liste des cases qui caractérise cette structure.

			---------------- Paramètre(s) ----------------
				'indice' (optionnel, par défaut 0) : c'est un entier naturel qui représente l'indice 
				de la case, dans la structure concernée, que l'utilisateur souhaite obtenir.

			----------------------------------------------

		'''

		if indice >= len(self.parametres['liste_cases']):
			raise("[Erreur] : la structure", struct, "possède strictement moins de", indice + 1, "cases !")

		return self.parametres['liste_cases'][indice]


	def sauvegarder(self):
		'''
			Fonction 'sauvegarder' qui permet d'enregistrer l'ensemble des paramètres 
			de la structure concernée. Cette fonction renvoie un dictionnaire qui correspond 
			à la structure enregistrée.

		'''

		dictionnaire_sauvegarde = deepcopy(self.__dict__)
		dictionnaire_sauvegarde['parametres']['liste_cases'] = [case.sauvegarder() for case in self.parametres['liste_cases']]

		return dictionnaire_sauvegarde

	# -----------------------------------------------------------------------------



class Magasin(Structure):
	'''
		Définition de la classe 'Magasin' qui hérite de la classe 'Structure'.

	'''



# -------------------------------- Constructeur --------------------------------
	def __init__(self, **parametres):
		'''
			Constructeur de la classe 'Magasin'.

			---------------- Paramètre(s) ----------------
				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble
				des paramètres propres au magasin. Ces paramètres (qui sont à définir soigneusement par
				l'utilisateur) permettent de rendre la simulation 'plus naturelle'.

			----------------------------------------------

		'''

		# On initialise les différents champs de l'objet 'Magasin'.

		# 'liste_cases' (optionnel, par défaut []) : c'est une liste d'éléments de type
		# 'Case' qui correspond à l'ensemble des cases qui constituent la structure.
		self.parametres = {**{'parametres_file_attente' : {'capacite_contamination' : 2}, 'parametres_magasin' : {'taux_dispersion' : 0., 'capacite_case' : 10, 'temps_attente' : 5}}, **parametres} # Permet la 'concaténation' des deux dictionnaires.

		file_attente, magasin = Case(**self.parametres['parametres_file_attente']), Case(**self.parametres['parametres_magasin'])
		file_attente.parametres['dictionnaire_cases_poids_disponibles'] = {magasin : 1}

		super().__init__(liste_cases = [file_attente, magasin])

	# ------------------------------------------------------------------------------

# ---------------------------------------------------------------------------



# -------------------------------- Fonctions(s) --------------------------------
def charger_case_via_dictionnaire(dictionnaire, decalage = 0):
	'''
		

	'''

	global compteur_cases, liste_cases_chargees

	compteur_cases = decalage + dictionnaire['numero_case']
	case = Case(**dictionnaire['parametres'])

	liste_cases_chargees.append(case)
	return case


def charger_structure_via_dictionnaire(dictionnaire, decalage = 0):
	'''
		

	'''

	if dictionnaire['parametres'].get('liste_cases', None) == None:
		return charger_case_via_dictionnaire(dictionnaire, decalage)

	dictionnaire['parametres']['liste_cases'] = [charger_structure_via_dictionnaire(dictionnaire_structure, decalage) for dictionnaire_structure in dictionnaire['parametres']['liste_cases']]
	return Structure(**dictionnaire['parametres'])

# ------------------------------------------------------------------------------
