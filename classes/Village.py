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
		# Ce fichier contient la définition de la classe 'Village'. Le village est à la base 
		# de grands nombre de simulations et contient de précieux renseignements sur l'état des 
		# cases, des entités et des sources qu'il abrite.

	# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------



# -------------------------------- Importation(s) --------------------------------
from copy import deepcopy

import classes.Case as Case
from classes.Case import charger_structure_via_dictionnaire, dictionnaire_numeros_cases, compteur_cases
from classes.Entite import charger_entite_via_dictionnaire, charger_source_via_dictionnaire

# --------------------------------------------------------------------------------



# -------------------------------- Classe(s) --------------------------------
class Village:
	'''
		Définition de la classe 'Village'.

	'''



	# -------------------------------- Constructeur --------------------------------
	def __init__(self, **parametres):
		'''
			Constructeur de la classe 'Village'.

			---------------- Paramètre(s) ----------------
				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble
				des paramètres propres au village. Ces paramètres (qui sont à définir soigneusement par
				l'utilisateur) permettent de rendre la simulation 'plus naturelle'.

			----------------------------------------------

		'''

		# On initialise les différents champs de l'objet 'Village'.

		# 'liste_entites' (optionnel, par défaut : []) : c'est une liste d'éléments de type
		# 'Entite' qui correspond à l'ensemble des entités présentes dans le village.

		# 'liste_sources' (optionnel, par défaut []) : c'est une liste d'éléments de type
		# 'Source' qui correspond à l'ensemble des points qui permettent l'émission d'entités
		# dans le village à chaque tour (de boucle).

		# 'liste_cases' (optionnel, par défaut []) : c'est une liste d'éléments de type
		# 'Case' qui correspond à l'ensemble des cases qui constituent le village. Cette liste 
		# peut aussi contenir des structures (ensemble de plusieurs cases)

		# 'entites_malades_retirees' (optionnel, par défaut : 0) : c'est un entier naturel qui caractérise le nombre 
		# d'entités contaminées qui ont été supprimées du village (concerné) depuis le début de la simulation.
		self.parametres = {**{'liste_entites' : [], 'liste_sources' : [], 'liste_cases' : [], 'entites_malades_retirees' : 0}, **parametres} # Permet la 'concaténation' des deux dictionnaires.

		self.parametres['entites_malades_village'] = sum([entite.parametres['sante'] for entite in self.parametres['liste_entites']])

	# ------------------------------------------------------------------------------



	# -------------------------------- Méthodes(s) --------------------------------
	def mettre_a_jour(self):
		'''
			Fonction 'mettre_a_jour' qui gère la mise à jour du village dans son intégralité (soit,
			elle assure en autre : la marche des entités, l'évolution de leurs paramètres ainsi que
			ceux des cases...).

		'''

		# On met à jour toutes les entités du village (en les faisant avancer vers d'autres cases ou en les retirant du village).
		for entite in self.parametres['liste_entites']:												# Pour chaque entités dans la liste des entités du village.
			if entite.avancer() == False:															# Si l'entité est bloquée dans le village (si la case sur laquelle elle se trouve n'a pas de case(s) associée(s)).
				self.parametres['entites_malades_retirees'] += entite.parametres['sante']			# On incrémente le compteur d'entités malades 'disparues' selon si l'entité à supprimer est malade ou non.
				self.parametres['liste_entites'].remove(entite)										# On retire l'entité de la liste des entités du village.

				entite.case_courante.sortir(entite)


		# On "injecte" de nouvelles entités dans le village grâce aux sources.
		for source in self.parametres['liste_sources']:												# Pour chaque source dans la liste des sources du village.
			nouvelle_entite = source.envoyer()														# On demande à la source d'envoyer une nouvelle entité.

			if nouvelle_entite != None:																# Si la source concernée peut encore envoyer des entités (compteur d'entités restantes à envoyer non vide).
				if nouvelle_entite != False:														# Si la source a bien renvoyé une entité (c'est la probabilité d'envoie).
					self.parametres['liste_entites'].append(nouvelle_entite)						# On ajoute alors la nouvelle entité en fin de la liste des entités du village.
			else:																					# Sinon (dans ce cas, la source est vide d'entités).
				self.parametres['liste_sources'].remove(source)										# On la retire alors la source concernée de la liste des sources du villages.

		self.parametres['entites_malades_village'] = sum([entite.parametres['sante'] for entite in self.parametres['liste_entites']])


	def sauvegarder(self):
		'''
			Fonction 'sauvegarder' qui permet d'enregistrer l'ensemble des paramètres 
			du village concerné. Cette fonction renvoie un dictionnaire qui correspond 
			au village enregistré.

		'''

		dictionnaire_sauvegarde = deepcopy(self.__dict__)
		dictionnaire_sauvegarde['parametres']['liste_entites'] = [entite.sauvegarder() for entite in self.parametres['liste_entites']]
		dictionnaire_sauvegarde['parametres']['liste_sources'] = [source.sauvegarder() for source in self.parametres['liste_sources']]
		dictionnaire_sauvegarde['parametres']['liste_cases'] = [case.sauvegarder() for case in self.parametres['liste_cases']]

		return dictionnaire_sauvegarde

	# -----------------------------------------------------------------------------

# ---------------------------------------------------------------------------



# -------------------------------- Fonctions(s) --------------------------------
def charger_village_via_dictionnaire(dictionnaire):
	'''
		

	'''

	decalage = compteur_cases
	Case.liste_cases_chargees = []

	dictionnaire['parametres']['liste_cases'] = [charger_structure_via_dictionnaire(dictionnaire_structure, decalage) for dictionnaire_structure in dictionnaire['parametres']['liste_cases']]
	dictionnaire['parametres']['liste_entites'] = [charger_entite_via_dictionnaire(dictionnaire_entite, decalage) for dictionnaire_entite in dictionnaire['parametres']['liste_entites']]
	dictionnaire['parametres']['liste_sources'] = [charger_source_via_dictionnaire(dictionnaire_source, decalage) for dictionnaire_source in dictionnaire['parametres']['liste_sources']]

	# Gestion de la liste des cases disponibles pour l'ensemble des cases fraîchement instanciées.
	for case in Case.liste_cases_chargees:
		case.parametres['dictionnaire_cases_poids_disponibles'] = {dictionnaire_numeros_cases[int(numero_case) + decalage] : poids for (numero_case, poids) in case.parametres['dictionnaire_cases_poids_disponibles'].items()}

	return Village(**dictionnaire['parametres'])

# ------------------------------------------------------------------------------
