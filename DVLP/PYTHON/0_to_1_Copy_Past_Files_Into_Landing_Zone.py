###############################################################################
#==============================================================================
#-- Parcourir un dossier et stocker les noms de fichiers dans une liste
#==============================================================================
#-- Import des bibliotheque
import sys, os, fnmatch
import datetime
import shutil
import csv
from fonctions_camille import write_metadata_csv
import shutil
import filecmp

#-- Initialisation des variable
myListOfFile = []
myListOfFileTmp = []


#-- Chemin vers le dossier où se trouvent les fichiers HTML à aller déposer dans la Landing Zone
myPathHtmlIn = "DATALAKE/0_SOURCE_WEB"
# C:\Users\camil\Cours\Lyon 2\Données massives\Lyon2_Data_lake_Project\DATALAKE\0_SOURCE_WEB

# Ecriture des métadonnées dans le fichier CSV
metadata_file_path = "DATALAKE/00_METADATA/METADATA_LANDING_ZONE.csv"
# C:\Users\camil\Cours\Lyon 2\Données massives\Lyon2_Data_lake_Project\DATALAKE\1_LANDING_ZONE
    

#-- Recupere les noms longs  des fichiers dans le path
myListOfFileTmp = os.listdir(myPathHtmlIn)


# -- Affichage de la liste des fichiers trouvés
print("Nb de fichiers trouvés : " + str(len(myListOfFileTmp)))

for myEntry in myListOfFileTmp :
    print("Fichier trouvé : " + myEntry)
    myListOfFile.append(myEntry)

print("Traitement...")

#==============================================================================
#-- Copie des fichiers dans les bons répertoires de la Landing Zone
#-- Vérification de la copie et écriture des métadonnées
#==============================================================================
compteur = 0
nbrTotalFichier = len(myListOfFile)
#--------------
for monNomDeFichier in myListOfFile: 
    compteur += 1
    print("Copie de " + str(compteur) + " fichiers sur " + str(nbrTotalFichier))
    # ---------------------------------------------

    # print("Traitement du fichier :", monNomDeFichier)
    # Si Nom fichier contient "INFO-EMP" et "LINKEDIN" alors copier dans le répertoire LINKEDIN/EMP
    # SI Nom fichier contient "INFO-SOC" et "GLASSDOOR" alors copier dans le répertoire GLASSDOOR/SOC
    # SI Nom fichier contient "AVIS-SOC" et "GLASSDOOR" alors copier dans le répertoire GLASSDOOR/AVIS
    if "INFO-EMP" in monNomDeFichier and "LINKEDIN" in monNomDeFichier :
        # print("Copie dans LINKEDIN/EMP")
        myPathHtmlOut = "DATALAKE/1_LANDING_ZONE/LINKEDIN/EMP"
    elif "INFO-SOC" in monNomDeFichier and "GLASSDOOR" in monNomDeFichier :
        # print("Copie dans GLASSDOOR/SOC")
        myPathHtmlOut = "DATALAKE/1_LANDING_ZONE/GLASSDOOR/SOC"
    elif "AVIS-SOC" in monNomDeFichier and "GLASSDOOR" in monNomDeFichier :
        # print("Copie dans GLASSDOOR/AVIS")
        myPathHtmlOut = "DATALAKE/1_LANDING_ZONE/GLASSDOOR/AVIS"
    else :
        print("Aucun critère de copie trouvé")
        myPathHtmlOut = ""
    monPathFile_IN = myPathHtmlIn + "/" + monNomDeFichier
    monPathFile_OUT = myPathHtmlOut + "/" + monNomDeFichier

    # ----------------------------------------------------------------
    # Essayer d'effectuer la copie et écrire une erreur en cas d'échec
    # ----------------------------------------------------------------
    try:
        shutil.copy(monPathFile_IN, monPathFile_OUT)

        # ------------------------------
        # Vérification que le fichier a été copié correctement
        # ------------------------------
        if not filecmp.cmp(monPathFile_IN, monPathFile_OUT, shallow=False):
            raise Exception("Échec de la vérification : les fichiers ne sont pas identiques.")
        
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

#==============================================================================
print("Traitement terminé.")
print("Voir le fichier de métadonnées : " + metadata_file_path)
#==============================================================================