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
		# Ce fichier contient plusieurs fonctions qui permettent de faciliter la sauvegarde 
		# complète d'une simulation (qui serait fastidieuse dans le cas échéant).

	# -----------------------------------------------------------------------------

# ------------------------------------------------------------------------------



# -------------------------------- Importations(s) --------------------------------
import json

# ---------------------------------------------------------------------------------



# -------------------------------- Fonctions(s) --------------------------------
def enregistrer(objet, **parametres):
	'''
		

	'''

	parametres = {**{'format' : 'json', 'chemin_enregistrement' : '', 'nom_fichier' : str(objet), 'encodage' : 'utf-8'}, **parametres}

	if parametres['format'] == 'json':
		chemin_complet = parametres['chemin_enregistrement'] + parametres['nom_fichier'] + '.json'

		with open(chemin_complet, mode ='w', encoding = parametres['encodage']) as fichier:
			fichier.write(json.JSONEncoder(sort_keys = True, separators = (',', ' : '), indent = 4).encode(objet.sauvegarder()))

		print("[Information] : l'objet", objet, "a été enregistré dans", chemin_complet, "avec succès.")

	else:
		raise("[Erreur] : le format d'enregistrement", parametres['format'], "n'est pas reconnu/supporté par le programme !")


def charger(nom_fichier, **parametres):
	'''
		

	'''

	parametres = {**{'format' : 'json', 'chemin_enregistrement' : '', 'fonction_lecture' : None, 'encodage' : 'utf-8'}, **parametres}

	if parametres['fonction_lecture'] == None:
		raise("[Erreur] : aucune fonction de lecture des données n'a été trouvée !")

	elif parametres['format'] == 'json':
		chemin_complet = parametres['chemin_enregistrement'] + nom_fichier + '.json'

		objet = None
		with open(chemin_complet, mode ='r', encoding = parametres['encodage']) as fichier:
			objet = parametres['fonction_lecture'](json.JSONDecoder().decode(fichier.read()))

		print("[Information] : le contenu du fichier", chemin_complet, "a été chargé avec succès.")
		return objet

	else:
		raise("[Erreur] : le format d'enregistrement", parametres['format'], "n'est pas reconnu/supporté par le programme !")

# ------------------------------------------------------------------------------
