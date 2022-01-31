# Script d'interprétation de données

# Copyright Issam Hamidi Donovan Blanc-Potard

# Version 1.0

# Date : 22/01/2022

import fonctions as fc


'''
============================================ PARTIE VELO===================================================
'''

def extraction_moyennes_velos(fichier):
    '''
    :param fichier: fichier à partir duquel on souhaite extraire les données
    :return: Retourne la liste des Moyennes du taux d'occupation de tous les parkings vélo à intervalle de temps défini
    '''
    fichier = open(fichier, "r", encoding="utf-8")
    lignes = fichier.readlines()
    fichier.close()

    parkings = []
    for ligne in lignes:
        ligne = ligne.strip()
        ligne = ligne.strip("|")
        ligne = ligne.split("|")
        parkings.append(ligne)

    nombre_parkings = len(parkings)
    nombre_prelevements = len(parkings[0])  # correspond au nombre de prélèvements effectués
    moyennes = []

    for i in range(nombre_prelevements):
        pourcentages = []
        for j in range(nombre_parkings):
            parking = parkings[j][i] #on prélève les données par colonne afin de les trier par intervalle de temps (d'abord t0, puis t1 ...)
            parking = parking.strip(";")
            parking = parking.split(";")
            nom, dispo, de, jusqua = [element.split("=")[1] for element in parking]
            pourcentages.append(fc.pourcentage(int(dispo), int(jusqua)))
        moyennes.append(fc.moyenne(pourcentages))
    return moyennes


'''
=============================================== PARTIE VOITURE ======================================================
'''

def extraction_moyennes_voitures(fichier):
    '''
    :param fichier: fichier à partir duquel on souhaite extraire les données
    :return: Retourne la liste des moyennes du taux d'occupation de tous les parkings voiture à intervalle de temps défini
    '''
    fichier = open(fichier, "r", encoding="utf-8")
    lignes = fichier.readlines()
    fichier.close()

    parkings = []
    for ligne in lignes:
        ligne = ligne.strip()
        ligne = ligne.strip("|")
        ligne = ligne.split("|")
        parkings.append(ligne)

    nombre_parkings = len(parkings)
    nombre_prelevements = len(parkings[0])  # correspond au nombre de prélèvements effectués
    moyennes = []

    for i in range(nombre_prelevements):
        pourcentages = []
        for j in range(nombre_parkings):
            parking = parkings[j][i] #on prélève les données par colonne afin de les trier par intervalle de temps (d'abord t0, puis t1 ...)
            parking = parking.strip(";")
            parking = parking.split(";")
            date, nom, statut, libres, total = [element.split("=")[1] for element in parking]
            pourcentages.append(fc.pourcentage(int(libres), int(total)))
        moyennes.append(fc.moyenne(pourcentages))
    return moyennes





moyennes_velos = extraction_moyennes_velos("velos.txt")
moyennes_voitures = extraction_moyennes_voitures("voitures.txt")

moyenne_totale_velos = fc.moyenne(moyennes_velos)
moyenne_totale_voitures = fc.moyenne(moyennes_voitures)

nombre_prelevements = len(moyennes_velos)

with open("donnees_courbe.dat", "w", encoding="utf-8") as fichier:
    for i in range(nombre_prelevements):
        fichier.write("{} {} {}\n".format(moyennes_velos[i], moyennes_voitures[i], i*5)) # ici, on inscrit les moyennes des parkings vélos, des parkings voitures ainsi que le temps (en min) sur une colonne différente
    fichier.close()

coefficient_correlation = fc.coefficient_correlation(moyennes_velos, moyennes_voitures, moyenne_totale_velos, moyenne_totale_voitures)

#print(coefficient_correlation)



