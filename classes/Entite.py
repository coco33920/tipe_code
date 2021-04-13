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
		# entre-elles.

	# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------



# -------------------------------- Importations(s) --------------------------------
from numpy import inf, array, append
from numpy.random import choice, uniform															# Pour choisir aléatoirement une cases parmi celles disponibles pour le déplacement des entités.

from copy import deepcopy

from classes.Case import dictionnaire_numeros_cases

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
		self.parametres = {**{'sante' : 0, 'etat' : 0, 'taux_dispersion' : .01, 'taux_contagion' : 1.}, **parametres}

		# On fait entrer l'entité concernée sur la case courante (celle qui lui a été initialement fixée).
		self.case_courante.entrer(self)

	# ------------------------------------------------------------------------------



	# -------------------------------- Méthodes(s) --------------------------------
	def avancer(self):
		'''
			Fonction 'avancer' qui gère la marche de l'entité concernée sur les différentes
			cases possibles.

		'''

		liste_cases_disponibles = self.case_courante.parametres['dictionnaire_cases_poids_disponibles']	# Obtention des informations sur l'emplacement de l'entité concernée.

		self.mettre_a_jour()																		# Pour mettre à jour les paramètres de l'individu concerné.
		if self.parametres['etat'] == 0:															# Si l'entité concernée peut avancer.
			if liste_cases_disponibles != {}:														# Si l'entité concernée peut rejoindre de nouvelles cases.
				liste_cases_accessibles = []														# On définit alors provisoirement la liste des cases accessibles par l'entité concernée.
				liste_poids = array([])																# On définit alors provisoirement la liste des poids des cases accessibles par l'entité concernée.

				for (case_disponible, poids) in liste_cases_disponibles.items():					# Pour chacune des cases disponibles que l'entité est susceptible de rejoindre.
					if case_disponible.parametres['capacite_case'] > 0:								# Si la case disponible peut encore accueillir des entités.
						liste_cases_accessibles.append(case_disponible)								# On ajoute alors cette case disponible dans la liste des cases accessibles.
						liste_poids = append(liste_poids, poids)									# On ajoute alors le poids de cette case disponible dans la liste des poids des cases.

				if liste_cases_accessibles != []:													# Si il existe des cases qui peuvent accueillir l'entité concernée parmi les cases disponibles.
					self.case_courante.sortir(self)													# On fait sortir de la case courante l'entité concernée.
					self.case_courante = choice(liste_cases_accessibles, p = liste_poids / sum(liste_poids)) # On choisi aléatoirement une nouvelle case parmi celles qui sont accessibles et on met à jour l'information sur l'entité.
					self.case_courante.entrer(self)													# On fait rentrer l'entité concernée sur une nouvelle case (parmi celles accessibles via la case courante).
					self.mettre_a_jour()															# Pour mettre à jour les paramètres de l'individu concerné.

			else:
				return False																		# Si l'entité concernée ne peut pas rejoindre de nouvelle cases, alors elle est bloquée, on la supprime donc du village.

		else:																						# Sinon, si l'individu ne doit pas bouger de sa case.
			self.parametres['etat'] -= 1															# On décrémente le nombre de tour (de boucle) qu'il reste l'entité concernée avant de pouvoir avancer de nouveau.

		return True


	def mettre_a_jour(self):
		'''
			Fonction 'mettre_a_jour' qui gère la modification des différents paramètres de
			l'entité concernée.

		'''

		if self.parametres['sante'] == 0 and (self.case_courante.parametres['capacite_contamination'] < 0):	# Si l'entité concernée est saine et qu'elle se trouve sur une case où elle peut être contaminée.
			# On calcul l'état de santé de l'entité 'entite' selon les différents paramètres qui rentrent en compte (taux de contagion du virus, taux de dispersion, taux de présence...).
			if (uniform(0, 1) <= self.parametres['taux_contagion'] * self.case_courante.parametres['taux_dispersion'] * self.case_courante.parametres['taux_presence']):
				self.case_courante.sortir(self)														# On fait sortir l'entité saine de sa case courante.
				self.parametres['sante'] = 1														# On modifie alors la santé de l'entité concernée, elle est maintenant contaminée.
				self.case_courante.entrer(self)														# On met alors à jour l'état de la case sur laquelle se trouvait précédemment l'entité saine.


	def sauvegarder(self):
		'''
			Fonction 'sauvegarder' qui permet d'enregistrer l'ensemble des paramètres 
			de l'entité concernée. Cette fonction renvoie un dictionnaire qui correspond 
			à l'entité enregistrée.

		'''

		dictionnaire_sauvegarde = deepcopy(self.__dict__)
		dictionnaire_sauvegarde['case_courante'] = self.case_courante.numero_case

		return dictionnaire_sauvegarde

	# -----------------------------------------------------------------------------



class Source:
	'''
		Définition de la classe 'Source'.

	'''



	# -------------------------------- Constructeur --------------------------------
	def __init__(self, case_associee, **parametres):
		'''
			Constructeur de la classe 'Source'.

			---------------- Paramètre(s) ----------------
				'case_associee' : un objet de type 'Case' qui représente la case sur laquelle
				la source courante doit envoyer ses entités.

				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble
				des paramètres propres à la source. Ces paramètres (qui sont à définir soigneusement par
				l'utilisateur) permettent de rendre la simulation 'plus naturelle'.

			----------------------------------------------

		'''

		# On initialise les différents champs de l'objet 'Source'.
		self.case_associee = case_associee

		# 'nombre_entites' (optionnel, par défaut : 10) : caractérise le nombre d'entités
		# présente dans la source courante. Il est possible de définir une source émettrice 
		# d'entités 'continue', au sens où, celle-ci envoie en permanence des entités grâce 
		# à la valeur 'inf' du module NumPy (voir la bibliothèque NumPy).

		# 'taux_contamination' (optionnel, par défaut : .2) : un réel entre 0 et
		# 1 (inclus) qui caractérise la probabilité que la nouvelle entité qui sera envoyée
		# dans le village par la source courante soit contaminée.

		# 'probabilite_envoie' (optionnel, par défaut : .75) : un réel entre 0 et 1 (inclus)
		# qui caractérise la probabilité que, lorsque la source doit envoyer une entité dans le village, celle-ci
		# soit réellement envoyée.

		# 'parametres_entite_type' (optionnel, par défaut {}) : un dictionnaire qui représente l'ensemble des paramètres 
		# 'types' des entités qui sortent de la source concernée (le paramètre 'santé' est toutefois géré à part,
		# il s'agit d'un point clé sur lequel agit une source).
		self.parametres = {**{'nombre_entites': 10, 'taux_contamination' : 0.2, 'probabilite_envoie' : 0.75, 'parametres_entite_type' : {}}, **parametres}

	# ------------------------------------------------------------------------------



	# -------------------------------- Méthodes(s) --------------------------------
	def envoyer(self):
		'''
			Fonction 'envoyer' qui gère l'envoie d'entité dans le village selon la source concernée.

		'''

		if self.parametres['nombre_entites'] <= 0:													# Si la source courante ne peut plus envoyer d'entités.
			return None																				# On renvoie 'None' : il faudra supprimer la source de la liste des sources du village.

		elif uniform(0, 1) <= self.parametres['probabilite_envoie']:								# Si la source courante peut envoyer une nouvelle entité dans le village.
			self.parametres['nombre_entites'] -= 1													# On décroît le nombre d'entité restantes dans la source courante.
			self.parametres['parametres_entite_type']['sante'] = (uniform(0, 1) <= self.parametres['taux_contamination']) # On modifie l'état de santé de la nouvelle entité.

			nouvelle_entite = Entite(self.case_associee, **self.parametres['parametres_entite_type']) # On crée la nouvelle entité à envoyer dans le village.

			return nouvelle_entite																	# Une fois la nouvelle entité crée et paramétrée, on la renvoie, prête à être ajoutée dans la liste des entités du village.

		return False																				# Si la source ne peut pas envoyer d'entités actuellement, on renvoie 'False' (pas d'entité envoyée).


	def sauvegarder(self):
		'''
			Fonction 'sauvegarder' qui permet d'enregistrer l'ensemble des paramètres 
			de la source concernée. Cette fonction renvoie un dictionnaire qui correspond 
			à la source enregistrée.

		'''

		dictionnaire_sauvegarde = deepcopy(self.__dict__)
		dictionnaire_sauvegarde['case_associee'] = self.case_associee.numero_case

		return dictionnaire_sauvegarde

	# -----------------------------------------------------------------------------

# ---------------------------------------------------------------------------



# -------------------------------- Fonctions(s) --------------------------------
def charger_entite_via_dictionnaire(dictionnaire, decalage = 0):
	'''
		

	'''

	case_courante = dictionnaire_numeros_cases[dictionnaire['case_courante'] + decalage]
	return Entite(case_courante, **dictionnaire['parametres'])


def charger_source_via_dictionnaire(dictionnaire, decalage = 0):
	'''
		

	'''

	case_associee = dictionnaire_numeros_cases[dictionnaire['case_associee'] + decalage]
	return Source(case_associee, **dictionnaire['parametres'])

# ------------------------------------------------------------------------------
