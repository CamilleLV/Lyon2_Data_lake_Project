###############################################################################
#==============================================================================
#-- Parcourir un dossier et stocker les noms de fichiers dans une liste
#==============================================================================
#-- Import des bibliotheque
import sys, os, fnmatch
import datetime
import csv
from TD1.fonctions_camille import write_metadata_csv

#-- Initialisation des variable
myListOfFile = []
myListOfFileTmp = []

myPathHtml = "TD1/BIBD_2020_TD_DATALAKE_DATAS_sans_csv/TD_DATALAKE/DATALAKE/0_SOURCE_WEB" #"C:/TD_DATALAKE/DATALAKE/0_SOURCE_WEB/"
print(myPathHtml)

# Ecriture des métadonnées dans le fichier CSV
metadata_file_path = "TD1/BIBD_2020_TD_DATALAKE_DATAS_sans_csv/TD_DATALAKE/DATALAKE/00_METADATA/METADATA_LANDING_ZONE.csv"
    



#-- Recupere les noms longs  des fichiers dans le path
myListOfFileTmp = os.listdir(myPathHtml)
# -- Affichage de la liste des fichiers trouvés
print("Nb de fichiers trouvés : " + str(len(myListOfFileTmp)))
# print(myListOfFileTmp)

for myEntry in myListOfFileTmp :
    # print("Fichier trouvé : " + myEntry)
    myListOfFile.append(myEntry)

#-- Parcour de tous les fichiers trouvés
# for myEntry in myListOfFileTmp :  
#     #-- On n'ajoute que les fichiers concernés (INFO-EMP, INFO-SOC, AVIS-SOC)
#     if fnmatch.fnmatch(myEntry, "*INFO-EMP*.html")==True:
#         myListOfFile.append(myEntry)
#     if fnmatch.fnmatch(myEntry, "*INFO-SOC*.html")==True:
#         myListOfFile.append(myEntry)
#     if fnmatch.fnmatch(myEntry, "*AVIS-SOC*.html")==True:   
#         myListOfFile.append(myEntry)

#-- Affichage du résultat
# for i in myListOfFile : print("Ligne : " + i)


# for myFileName in myListOfFile: print(myPathHtml + " --> " + str(myFileName))

#==============================================================================
###############################################################################

###############################################################################
#==============================================================================
#-- Copier des fichier d'une répertoir dans un autre
#==============================================================================
import shutil
import csv

myPathHtmlIn = "TD1/BIBD_2020_TD_DATALAKE_DATAS_sans_csv/TD_DATALAKE/DATALAKE/0_SOURCE_WEB"

monPathFile_Test_IN = myPathHtmlIn + "/" + "13799-INFO-EMP-LINKEDIN-FR-1555991658.html"
monPathFile_Test_OUT = "TD1/BIBD_2020_TD_DATALAKE_DATAS_sans_csv/TD_DATALAKE/DATALAKE/1_LANDING_ZONE/LINKEDIN/EMP" + "/" + "monTest.html"

# print(monPathFile_Test_IN)
# print(monPathFile_Test_OUT)


shutil.copy(monPathFile_Test_IN, monPathFile_Test_OUT)

print("Traitement...")
#--------------
for monNomDeFichier in myListOfFile: 
    # print("Traitement du fichier :", monNomDeFichier)
    # Si Nom fichier contient "INFO-EMP" et "LINKEDIN" alors copier dans le répertoire LINKEDIN/EMP
    # SI Nom fichier contient "INFO-SOC" et "GLASSDOOR" alors copier dans le répertoire GLASSDOOR/SOC
    # SI Nom fichier contient "AVIS-SOC" et "GLASSDOOR" alors copier dans le répertoire GLASSDOOR/AVIS
    if "INFO-EMP" in monNomDeFichier and "LINKEDIN" in monNomDeFichier :
        # print("Copie dans LINKEDIN/EMP")
        myPathHtmlOut = "TD1/BIBD_2020_TD_DATALAKE_DATAS_sans_csv/TD_DATALAKE/DATALAKE/1_LANDING_ZONE/LINKEDIN/EMP"
    elif "INFO-SOC" in monNomDeFichier and "GLASSDOOR" in monNomDeFichier :
        # print("Copie dans GLASSDOOR/SOC")
        myPathHtmlOut = "TD1/BIBD_2020_TD_DATALAKE_DATAS_sans_csv/TD_DATALAKE/DATALAKE/1_LANDING_ZONE/GLASSDOOR/SOC"
    elif "AVIS-SOC" in monNomDeFichier and "GLASSDOOR" in monNomDeFichier :
        # print("Copie dans GLASSDOOR/AVIS")
        myPathHtmlOut = "TD1/BIBD_2020_TD_DATALAKE_DATAS_sans_csv/TD_DATALAKE/DATALAKE/1_LANDING_ZONE/GLASSDOOR/AVIS"
    else :
        print("Aucun critère de copie trouvé")
        myPathHtmlOut = ""
    monPathFile_IN = myPathHtmlIn + "/" + monNomDeFichier
    monPathFile_OUT = myPathHtmlOut + "/" + monNomDeFichier
    # print(monPathFile_IN)
    # print(monPathFile_OUT)

    
    # ----------------------------------------------------------------
    # Essayer d'effectuer la copie et écrire une erreur en cas d'échec
    # ----------------------------------------------------------------
    try:
        shutil.copy(monPathFile_IN, monPathFile_OUT)
    except Exception as e:
        print("Erreur lors de la copie :", e)
        # Ajout du statut du déplacement
        write_metadata_csv(metadata_file_path, monNomDeFichier, "COPY_STATUS", "ERROR")
        continue

    
    # L'identifiant de la ligne est les 5 premières lettres du nom du fichier

    # Ajout de l'heure exacte du déplacement
    write_metadata_csv(metadata_file_path, monNomDeFichier, "DATE_COPY", str(datetime.datetime.now()))
    # Ajout du chemin source et destination du fichier copié
    write_metadata_csv(metadata_file_path, monNomDeFichier, "SOURCE_PATH", monPathFile_IN + "/" + monNomDeFichier)
    write_metadata_csv(metadata_file_path, monNomDeFichier, "DESTINATION_PATH", monPathFile_OUT + "/" + monNomDeFichier)
    # Ajout du type du fichier copié (csv, html, txt, ...)
    write_metadata_csv(metadata_file_path, monNomDeFichier, "FILE_TYPE", monNomDeFichier.split('.')[-1])
    # Ajout du statut du déplacement
    write_metadata_csv(metadata_file_path, monNomDeFichier, "COPY_STATUS", "SUCCESS")

#--------------

print("Traitement terminé.")
print("Voir le fichier de métadonnées : " + metadata_file_path)
#==============================================================================



###############################################################################