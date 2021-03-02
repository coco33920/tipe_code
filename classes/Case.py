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



# -------------------------------- Classe(s) --------------------------------
class Case:
	'''
		Définition de la classe 'Case'.

	'''



	# -------------------------------- Constructeur --------------------------------
	def __init__(self, liste_cases_disponibles = [], **parametres):
		'''
			Constructeur de la classe 'Case'.

			---------------- Paramètre(s) ----------------
				'liste_cases_disponibles' (optionnel, par défaut : []) : c'est une liste d'objet de type 'Case' 
				qui correspond à l'ensemble des cases qui sont directement accessibles via la case concernée.

				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble 
				des paramètres propres à la case. Ces paramètres (qui sont à définir soigneusement par 
				l'utilisateur) permettent de rendre la simulation 'plus naturelle'.

			----------------------------------------------

		'''

		# On initialise les différents champs de l'objet 'Case'.
		self.liste_cases_disponibles = liste_cases_disponibles

		# 'taux_dispersion' (optionnel, par défaut : 1.) : un réel entre 0 et 1 (inclus) 
		# qui caractérise la probabilité que, si une ou plusieurs entité(s) contaminée(s) 
		# se trouvent sur cette case, que le virus se diffuse à l'ensemble de la case et touche 
		# donc, potentiellement, les autres entités saines.

		# 'taux_presence' (optionnel, par défaut : 0.) : un réel entre 0 et 1 (inclus) 
		# qui caractérise la probabilité de présence du virus sur une case. Cette probabilité 
		# est influencée en fonction de l'état des entités qui s'y trouvent.
		self.parametres = {**{'taux_dispersion' : 1., 'taux_presence' : 0.}, **parametres}

	# ------------------------------------------------------------------------------



	# -------------------------------- Méthodes(s) --------------------------------
	def entrer(self, entite):
		'''
			Fonction 'entrer' qui gère l'entrée de l'entité 'entite' dans la case 
			concernée.

			---------------- Paramètre(s) ----------------
				'entite' : un objet de type 'Entite' qui correspond à l'entité qui 
				rentre sur la case concernée par l'action.

			----------------------------------------------

		'''

		# On calcul le nouveau taux de présence du virus sur la case. Le calcul se fait via la formule de la 
		# probabilité d'une union. On considère (et il est naturel de faire ainsi) que les événements «se faire contaminer par 
		# l'entité A» et «se faire contaminer par l'entité B» sont indépendants.
		if entite.parametres['sante'] == 1:															# Si l'entité concernée par l'action est contaminée.
			# On met à jour le taux de présence du virus de la case concernée.
			self.parametres['taux_presence'] = 1. - (1. - self.parametres['taux_presence']) * (1. - entite.parametres['taux_dispersion'])


	def sortir(self, entite):
		'''
			Fonction 'sortir' qui gère la sortie de l'entité 'entite' de la case 
			concernée.

			---------------- Paramètre(s) ----------------
				'entite' : un objet de type 'Entite' qui correspond à l'entité qui 
				sort de la case concernée par l'action.

			----------------------------------------------

		'''

		# On calcul le nouveau taux de présence du virus sur la case (c.f. le commentaire analogue de la fonction précédente).
		if entite.parametres['sante'] == 1:															# Si l'entité concernée par l'action est contaminée.
			# On met à jour le taux de présence de la case concernée.
			self.parametres['taux_presence'] = (self.parametres['taux_presence'] - entite.parametres['taux_dispersion']) / (1. - entite.parametres['taux_dispersion'])

	# -----------------------------------------------------------------------------



class Magasin(Case):
	'''
		Définition de la classe 'Magasin' hérité de la classe 'Case'.

	'''



	# -------------------------------- Constructeur --------------------------------
	def __init__(self, liste_cases_disponibles = [], **parametres):
		'''
			Constructeur de la classe 'Magasin'.

			---------------- Paramètre(s) ----------------
				'liste_cases_disponibles' (optionnel, par défaut : []) : c'est une liste d'objet de type 'Case' 
				qui correspond à l'ensemble des cases qui sont directement accessibles via la case concernée.

				'parametres' (optionnel, par défaut {}) : c'est un dictionnaire qui contient l'ensemble 
				des paramètres propres à la case. Ces paramètres (qui sont à définir soigneusement par 
				l'utilisateur) permettent de rendre la simulation 'plus naturelle'.

				'max_clients' : entier naturel non nul qui représente le nombre maximal de clients 
				que peut accueillir le magasin. Si cette jauge est atteinte, les nouveaux clients 
				seront envoyés dans une case auxiliaire qui sert de file d'attente (c'est d'ailleurs 
				sur cette case que les entités sont le plus susceptibles de se contaminer mutuellement).

				'temps_attente' (optionnel, par défaut : 5) : entier naturel non nul qui représente le 
				temps d'attente, pour chaque entité, dans le magasin considéré. Il s'agit du nombre de 
				tours (de boucle) avant que l'entité rentrée dans le magasin ne puisse sortir.

			----------------------------------------------

		'''

		# Appelle du constructeur de la classe 'Case'.
		super().__init__(liste_cases_disponibles, **{**{'taux_dispersion' : 0., 'max_clients' : 3, 'temps_attente' : 3, 'parametres_file_attente' : {}}, **parametres})

		# On créer la file d'attente associée au magasin concerné. Cette file d'attente se remplie lorsque la magasin concerné est plein. C'est d'ailleurs dans ces files d'attente que les entités se contaminent mutuellement.
		self.file_attente = Case([self], **self.parametres['parametres_file_attente'])

	# ------------------------------------------------------------------------------



	# -------------------------------- Méthodes(s) --------------------------------
	def entrer(self, entite):
		'''
			Fonction 'entrer' qui gère l'entrée de l'entité 'entite' dans la case 
			concernée.

			---------------- Paramètre(s) ----------------
				'entite' : un objet de type 'Entite' qui correspond à l'entité qui 
				rentre sur la case concernée par l'action.

			----------------------------------------------

		'''

		if self.parametres['max_clients'] > 0:														# Si il reste encore des places disponibles.
			self.parametres['max_clients'] -= 1														# Alors on décrémente le nombre de places disponibles dans la magasin.
			entite.parametres['etat'] = self.parametres['temps_attente']							# On fait patienter l'entité pendant 'self.temps_attente' tours (de boucle).

		else:																						# Sinon, si le magasin est plein.
			entite.case_courante = self.file_attente												# Par construction du graphe, le numéro des files d'attente est toujours égale à une unité de plus que le numéro du magasin.
			self.file_attente.entrer(entite)														# Alors on fait entrer l'entité dans la file d'attente.


	def sortir(self, entite):
		'''
			Fonction 'sortir' qui gère la sortie de l'entité 'entite' de la case 
			concernée.

			---------------- Paramètre(s) ----------------
				'entite' : un objet de type 'Entite' qui correspond à l'entité qui 
				sort de la case concernée par l'action.

			----------------------------------------------

		'''

		self.parametres['max_clients'] += 1															# Lorsque l'entité sort du magasin, on incrémente le nombre de places à nouveau disponibles (une place s'est libérée).

	# -----------------------------------------------------------------------------

# ---------------------------------------------------------------------------
