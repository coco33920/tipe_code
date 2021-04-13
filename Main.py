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
		# Ce fichier est le fichier principal du projet.

	# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------



# -------------------------------- Importation(s) --------------------------------
from classes.Case import Case, Magasin
from classes.Village import Village
from classes.Entite import Entite, Source
from classes.Simulation import Simulation, charger_simulation_via_dictionnaire

from utilitaire.Courbes import Courbe, afficher
from utilitaire.Interpolation import Interpolation, sigmoide_asymetrique_5, sigmoide_asymetrique_generalisee, fonction_logistique_generalisee
from utilitaire.Sauvegarde import enregistrer, charger

from numpy import inf, divide

# --------------------------------------------------------------------------------



# -------------------------------- Main --------------------------------
if __name__ == '__main__':																			# Instruction principale du programme.
	case1, magasin1, magasin2, puit = Case(), Magasin(), Magasin(), Case(capacite_contamination = inf)

	case1.parametres['dictionnaire_cases_poids_disponibles'] = {magasin1.case(0) : 1, magasin2.case(0) : 1}
	magasin1.case(1).parametres['dictionnaire_cases_poids_disponibles'] = {magasin2.case(0) : 1}
	magasin2.case(1).parametres['dictionnaire_cases_poids_disponibles'] = {puit : 1}

	source = Source(case1, nombre_entites = 50)

	village = Village(liste_sources = [source], liste_cases = [case1, magasin1, magasin2, puit])

	simulation = Simulation(village = village, nombre_points = 30)
	#simulation = charger('simulation_total_2', fonction_lecture = charger_simulation_via_dictionnaire)
	simulation.lancer()

	#enregistrer(simulation, nom_fichier = 'simulation_total_3')
	abscisse = simulation.parametres['liste_temps']
	courbe1 = Courbe(abscisse, divide(simulation.parametres['liste_total_contaminees'], simulation.parametres['nombre_simulations']))
	courbe2 = Courbe(abscisse, divide(simulation.parametres['liste_contaminees_restants'], simulation.parametres['nombre_simulations']))

	courbe1.tracer('o')
	courbe2.tracer('x')
	afficher(courbe1)

# ----------------------------------------------------------------------
