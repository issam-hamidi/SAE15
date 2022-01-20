import requests
from lxml import etree


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

parser = etree.XMLParser()

#requete = requests.get("https://data.montpellier3m.fr/sites/default/files/ressources/FR_MTP_ANTI.xml")

for parking in parkings:
    print(parking)
    requete = requests.get("https://data.montpellier3m.fr/sites/default/files/ressources/{}.xml".format(parking))
    brut = requete.text[requete.text.index(">")+1:]
    #Ici, je découpe manuellement la partie haute du contenu xml (<?xml version='1.0' encoding='UTF-8'?>)
    #Pour cela je supprime tous les caractères jusqu'au premier ">" (car la fonction index donne l'index du premier élement donné en argument)
    #ainsi que le caractère suivant qui correspond au retour chariot
    tree = etree.XML(brut, parser)
    chaine = ""
    for item in items:
        donnee = tree.xpath("/park/{}".format(item))[0]# On prend toujours le premier élément car il n'y a qu'un seul élement par tag
        chaine += "{}:{}".format(item,donnee.text)
    print(chaine)

'''
========================================================================================================================
                                Partie Velo
========================================================================================================================
'''


'''requete = requests.get("https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_VELOMAG.xml")

brut = requete.text

parser = etree.XMLParser()
donnee = etree.XML(brut, parser)

donnees = donnee.xpath("/vcs/sl/si")

dico = {
    "Name": "na",
    "Availables": "av",
    "From": "fr",
    "To": "to"
}

for element in donnees:
    chaine = ""
    for k,v in dico.items():
        chaine += "{}:{};".format(k, element.attrib[v])
    print(chaine)
'''


