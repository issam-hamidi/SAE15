import requests
import time
from lxml import etree

parser = etree.XMLParser()



'''
========================================================================================================================
                                Partie Voiture
========================================================================================================================
'''

items = [
    "DateTime",
    "Name",
    "Status",
    "Free",
    "Total"
]


parkings=['FR_MTP_ANTI','FR_MTP_COME','FR_MTP_CORU','FR_MTP_EURO',
'FR_MTP_FOCH','FR_MTP_GAMB','FR_MTP_GARE','FR_MTP_TRIA','FR_MTP_ARCT',
'FR_MTP_PITO','FR_MTP_CIRC','FR_MTP_SABI','FR_MTP_GARC','FR_MTP_SABL',
'FR_MTP_MOSS','FR_STJ_SJLC','FR_MTP_MEDC','FR_MTP_OCCI','FR_CAS_VICA',
'FR_MTP_GA109','FR_MTP_GA250','FR_CAS_CDGA','FR_MTP_ARCE','FR_MTP_POLY']


def extraction_donnees_voiture(parkings):
    '''
    Cette fonction sert à extraire les données de chaque parking afin de les placer dans une liste

    :param parkings: Contient la liste des abréviations des différents parkings afin de les insérer par la suite dans l'url
    :return: La fonction retourne la liste des données de chaque parking dans le format [données_parking1, données_parking2....]

    '''
    liste_donnees = []
    for parking in parkings:
        requete = requests.get("https://data.montpellier3m.fr/sites/default/files/ressources/{}.xml".format(parking))
        brut = requete.text[requete.text.index(">") + 1:]
        # Ici, je découpe manuellement la partie haute du contenu xml (<?xml version='1.0' encoding='UTF-8'?>)
        # Pour cela je supprime tous les caractères jusqu'au premier ">" (car la fonction index donne l'index du premier élement donné en argument)
        # ainsi que le caractère suivant qui correspond au retour chariot
        # Je fait cette opération car la fonction de parsage ci-dessous n'accepte pasla partie haute du contenu xml indiquée plus haut
        tree = etree.XML(brut, parser)
        chaine = ""        # sert à contenir les données d'un parking
        for item in items:
            donnee = tree.xpath("/park/{}".format(item))[0]  # On prend toujours le premier élément car il n'y a qu'un seul élement par tag
            chaine += "{}={};".format(item, donnee.text)    # On ajoute l'item ainsi que la valeur correspondante
        chaine += "|\n"     # Ici, le pipe servira à séparer les données de chaque parking lors de l'écriture dans le fichier. Le \n servira à faire un retour à la ligne
        liste_donnees.append(chaine)
    return liste_donnees

def initialisation_voiture(nom_fichier):
    '''
    Cette fonction sert à inscrire une première entrée de données afin d'initialiser le fichier qui contiendra les données concernant
    les parkings de voitures

    :param nom_fichier: Le nom du fichier que l'on veut initialiser afin d'y inscrire une première entrée de données
    :return: Ne retourne rien
    '''
    fichier = open(nom_fichier, "w", encoding="utf-8")
    liste_donnees = extraction_donnees_voiture(parkings)
    for element in liste_donnees:
        fichier.write(element)
    fichier.close()


def mise_a_jour_voiture(nom_fichier):
    liste_donnees = extraction_donnees_voiture(parkings)
    fichier = open(nom_fichier, "r", encoding="utf-8")
    lignes = [ligne.strip() for ligne in fichier]
    fichier.close()
    with open(nom_fichier, "w", encoding="utf-8") as fichier:
        for i in range(len(lignes)):
            fichier.write(lignes[i]+liste_donnees[i])
        fichier.close()

'''
========================================================================================================================
                                Partie Velo
========================================================================================================================
'''


requete = requests.get("https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_VELOMAG.xml")

brut = requete.text

donnee = etree.XML(brut, parser)

donnees = donnee.xpath("/vcs/sl/si")

dico = {
    "Name": "na",
    "Availables": "av",
    "From": "fr",
    "To": "to"
}

def extraction_donnees_velo(donnees):
    liste_donnees = []
    for element in donnees:
        chaine = ""
        for k,v in dico.items():
            chaine += "{}={};".format(k, element.attrib[v])
        chaine += "|\n"
        liste_donnees.append(chaine)
    return liste_donnees

def initialisation_velo(nom_fichier):
    fichier = open(nom_fichier, "w", encoding="utf-8")
    liste_donnees = extraction_donnees_velo(donnees)
    for element in liste_donnees:
        fichier.write(element)
    fichier.close()

def mise_a_jour_velo(nom_fichier):
    liste_donnees = extraction_donnees_velo(donnees)
    fichier = open(nom_fichier, "r", encoding="utf-8")
    lignes = [ligne.strip() for ligne in fichier]
    fichier.close()
    with open(nom_fichier, "w", encoding="utf-8") as fichier:
        for i in range(len(lignes)):
            fichier.write(lignes[i]+liste_donnees[i])
        fichier.close()


'''
============================================ INITIALISATION =========================================
Le but ici est d'initialiser les données conernant les parkings vélos en mettant en place une première requête, avant d'ajouter par la suite 
une serie de données à un intervalle de temps de 10 minutes pendant une durée de deux heures
'''

initialisation_voiture("voitures.txt")
initialisation_velo("velos.txt")


#faire une fonction extraction

'''
============================================ Suite des données ===========================================
Ici, nous ajoutons donc les données à la suite à un intervalle de temps de 10 minutes (600 secondes) jusqu'à atteindre un échantillon sur deux heures
soit 12 * 10 minutes
'''

for i in range(600):
    time.sleep(1)
    mise_a_jour_voiture("voitures.txt")
    mise_a_jour_velo("velos.txt")




