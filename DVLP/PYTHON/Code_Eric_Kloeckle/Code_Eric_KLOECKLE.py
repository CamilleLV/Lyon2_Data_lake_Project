# -*- coding: utf-8 -*-
"""
Éditeur de Spyder
"""




###############################################################################
###############################################################################
#- Boite à outils Python pour le module Gestion des Donnes Massives 
#- T.D. DATALAKE
#- Master 2 BI&BD - Université Lyon2
#- Enseignant : Eric KLOECKLE
###############################################################################
###############################################################################



#==============================================================================
#==============================================================================
#Lecture et Stockage des Fichiers texte
#==============================================================================
#==============================================================================

#------------------------------------------------------------------------------
#Ouverture / Lecture / Affichage / Fermeture  d'un fichier texte
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#-- READ()
#------------------------------------------------------------------------------
#-- Ouverture d'un fichier présent sur le disque dur 
#------------------------------------------------------------------------------

myPathLog = "TD1/BIBD_2020_TD_DATALAKE_DATAS_sans_csv/TD_DATALAKE/LOGFILES/" #"C:/TD_DATALAKE/LOGFILES/" 
myPathHtml = "TD1/BIBD_2020_TD_DATALAKE_DATAS_sans_csv/TD_DATALAKE/DATALAKE/1_LANDING_ZONE/GLASSDOOR/SOC/"#'C:/TD_DATALAKE/DATALAKE/1_LANDING_ZONE/GLASSDOOR/SOC/'

print(myPathHtml)

myFilePathName = myPathLog + "mon_fichier_a_lire.txt"

print(myFilePathName)


#------------------------------------------------------------------------------
#-- Probleme encodage utf-8 lors du read() du fochoer ouvert en utf-8 :
#------------------------------------------------------------------------------
#    - myFilePtr = open(myFilePathName, "r", encoding="utf-8")    
#    - myFileContents = myFilePtr.read()
#    Erreur   : ==> UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 574: invalid continuation byte
#    Solutions : https://www.journaldunet.fr/web-tech/developpement/1441055-corriger-l-erreur-unicodedecodeerror-utf-8-codec-can-t-decode-byte-0xff-in-position-0-invalid-start-byte/
#    Solution : ==> myFilePtr = open(myFilePathName, "r", encoding="utf-8", errors="ignore")
#------------------------------------------------------------------------------
#myFilePtr = open(myFilePathName, "r")
#myFilePtr = open(myFilePathName, "r", encoding="utf-8")
myFilePtr = open(myFilePathName, "r", encoding="utf-8", errors="ignore")

print(myFilePtr)

#-- .read
myFileContents = myFilePtr.read()
print(len(myFileContents))
print(myFileContents)
#print("\n ****************","\n", "Longueur : " + str(len(myFileContents_read)) + " caractere(s)\n", "----------------", "\n" + myFileContents + chr(10), "****************")


#-- Parcours de tous les enreg du fichier texte
#------------------------------------------------------------------------------
for myLineRead in myFileContents: 
    print(myLineRead)  #-- "print" saute une ligne par defaut a chaque appel (donc ici pour chaque caractere)

for myLineRead in myFileContents: 
    print(myLineRead, end='')  #-- end='' permet de ne pas sauter de ligne a chaque appel de "print"
#-- OU

#maListe = ('a', 'b', 'c')
#print(maListe)
#type(maListe)
##'maListe = 'le village'
#len(range(3))

#print(myFileContents[872])

for myIndice in range(len(myFileContents)) :
    print(myFileContents[myIndice], end='')
#-- OU
myIndice = 0
while myIndice < len(myFileContents):
    print(myFileContents[myIndice], end='')
    myIndice = myIndice + 1


#------------------------------------------------------------------------------
#-- READLINES()
#------------------------------------------------------------------------------    
#-- Ouverture d'un fichier présent sur le disque dur 
#------------------------------------------------------------------------------
myFilePathName = myPathLog + "mon_fichier_a_lire.txt"
print(myFilePathName)

myFilePtr = open('C:/TD_DATALAKE/LOGFILES/mon_fichier_a_lire.txt', "r", encoding="utf8", errors="ignore")
print(myFilePtr)
#-- .readline
myFileContents = myFilePtr.readlines()
print(len(myFileContents))
print(myFileContents)
print(myFileContents[0])

#-- Parcours de tous les enreg du fichier texte
#------------------------------------------------------------------------------
for myLineRead in myFileContents: 
    print(myLineRead, end='')  #-- end='' permet de ne pas sauter de ligne a chaque appel de "print"

#-- Fermeture du "pointeur" de fichier
#------------------------------------------------------------------------------
myFilePtr.close()



#==============================================================================
#==============================================================================
#-- Ecrire dans un fichier CSV
#==============================================================================
#==============================================================================
myFilePathName = myPathLog + "mon_fichier_a_ecrire.txt"
print(myFilePathName)

#-- Ouverture du fichier en création (raz)
#------------------------------------------------------------------------------
myFilePtr = open(myFilePathName, "w", encoding = "utf-8")

#-- Ouverture du fichier en ajout (modification)
#------------------------------------------------------------------------------
myFilePtr = open(myFilePathName, "a", encoding = "utf-8")


#------------------------------------------------------------------------------
#-- Creation et remplissage d'une liste des lignes de texte a ecrire
#------------------------------------------------------------------------------
#-- Instanciation d'une liste vide 
myListeDeLigneAEcrire = [] 
print(len(myListeDeLigneAEcrire))
print(myListeDeLigneAEcrire)

#-- Remplissage de la liste 
myListeDeLigneAEcrire.append('"cle_unique";"colonne";"valeur"'+"\n")
myListeDeLigneAEcrire.append('16308;"nom_entreprise";"Business & décision"'+chr(10))

print(myListeDeLigneAEcrire[1])

myListeDeLigneAEcrire.append('16308;"ville_entreprise","Lyon 7 eme"')
myListeDeLigneAEcrire.append('16308;"note_entreprise",3,2')
#-- RQ : "\n" et chr(10)  = "Retour chariot" ou "Saut de ligne"

print(myListeDeLigneAEcrire)

#------------------------------------------------------------------------------
#-- Ecriture de chaque ligne de la liste dans un fichier texte de sortie
#------------------------------------------------------------------------------
#-- Test1 : Boucle d'écriture de chaque ligne de la liste d'éléments dans le fichier 
for myLigneAEcrire in myListeDeLigneAEcrire:
    myFilePtr.write(myLigneAEcrire+"\n")

#-- Test2 : Ecriture en une seule passe de la liste d'éléments dans le fichier 
myFilePtr.writelines(myListeDeLigneAEcrire)

    
myFilePtr.close()



#==============================================================================
#==============================================================================
#-- Parcourir et faire un traitement sur des fichiers d'un répertoire 
#==============================================================================
#==============================================================================
import sys, os, fnmatch

myListOfFile = []
myListOfFileTmp = []

#-- ramène tous les noms des fichiers du répertoire 
myListOfFileTmp = os.listdir(myPathHtml)
print(myListOfFileTmp)


#-- Filtrer les fichiers concernés 
myPattern = "*AVI*.html"

for myEntry in myListOfFileTmp : 
#    print('**', myEntry)
    if fnmatch.fnmatch(myEntry, myPattern):
        print(myEntry)
#        myListOfFile.append(myEntry)

for myFileName in myListOfFileTmp: print(myPathHtml + " --> " + str(myFileName))




###############################################################################
###############################################################################


#==============================================================================
#==============================================================================
#Lecture et Stockage en Base de données MySql
#==============================================================================
#==============================================================================
#-- Importer la bibliothèque Python MySQL
import sys
import mysql.connector

#------------------------------------------------------------------------------
#-- Ouvrir la connexion à la base
#------------------------------------------------------------------------------
#-- Connexion a la base de donnees --> MYSQL
myDbNameMySQL = 'BASE_CURATED_ZONE'
myHost = 'localhost'
myUser = 'root'
myPwd = ''
myTextConnexion = "self.conn = mysql.connector.connect(user=" + myUser +\
                  ", password=" + myPwd + ", host=" + myHost +\
                  ", database=" + myDbNameMySQL
                  
self.conn = mysql.connector.connect(user=myUser, 
                                    password=myPwd, 
                                    host=myHost,
                                    database=myDbNameMySQL)
self.cursor = self.conn.cursor()
#../..

#------------------------------------------------------------------------------
#-- Suppression d'une table dans la base de données --> MYSQL
#------------------------------------------------------------------------------
MyRequeteSqlDropTbl = "DROP TABLE tbl_linkedin_brut"
self.cursor.execute(MyRequeteSqlDropTbl)
self.conn.commit()

#------------------------------------------------------------------------------
#-- Creation d'une table dans la base de données --> MYSQL
#------------------------------------------------------------------------------
MyRequeteSqlCreateTbl = "CREATE TABLE tbl_metadonnee ( "+\
"cle_unique VARCHAR(100), valeur BLOB, Id VARCHAR(100), valeur LONGTEXT )"
self.cursor.execute(MyRequeteSqlCreateTbl)
self.conn.commit()

#------------------------------------------------------------------------------
# - Ecriture d'une ligne dans une table de la base de données  --> MYSQL 
#------------------------------------------------------------------------------
tbl_metadonnee = "TBL_METADATA"
try:
    MyRequeteSqInsert = 'INSERT INTO ' + tbl_metadonnee + ' (cle_unique, colonne, valeur) VALUES (' + "'"+ "16308"  +"'" + ',' + "'"+ "nom_entreprise"+"'" + ',' + " Lyon 7 eme "  + ')'
    self.cursor.execute(MyRequeteSqInsert)
    self.conn.commit()

    MyRequeteSqInsert = 'INSERT INTO ' + tbl_metadonnee + ' (cle_unique, colonne, valeur) VALUES (' + "'"+ "16308" +"'" + ',' + "'"+ "ville_entreprise" + "'" + ',' + " Business & décision"  + ')'
    self.cursor.execute(MyRequeteSqInsert)
    self.conn.commit()

    MyRequeteSqInsert = 'INSERT INTO ' + tbl_metadonnee + ' (cle_unique, colonne, valeur) VALUES (' + "'"+ "16308" +"'" + ',' + "'"+ "note_entreprise"+"'" + ',' + "3,2"  + ')'
    self.cursor.execute(MyRequeteSqInsert)
    self.conn.commit()

#------------------------------------------------------------------------------
#-- Gestion des exception operation sur base de données --> MYSQL 
#------------------------------------------------------------------------------
#except MySQLdb.Error as e:
except mysql.connector.Error as e:
    print ("Error %d: %s" % (e.args[0],e.args[1]))
    sys.exit(1)
    #pass




###############################################################################
###############################################################################


#==============================================================================
#-- Les Fonctions :
#==============================================================================
#-- Fonction renvoyant <commentaire>  avec des paramètres en entrée et un paramètre en sortie
def  Retourner_votre_texte (myPrefix, myText):
    Result  =  myPrefix + myText
    return(Result)

myVar1 = Retourner_votre_texte ("Bonjour", ' il fait beau !')
print(myVar1)

myVar2 = Retourner_votre_texte (myText=' il fait beau !', myPrefix="Bonjour")
print(myVar2)

def maJolieFonction():
    return('Jolie Fonction')
print(maJolieFonction())



def maJolieFonction(monParam1):
    return(monParam1)
print(maJolieFonction())
print(maJolieFonction('coucou'))    


def maJolieFonction(monParam1='toto'):
    return(monParam1)
print(maJolieFonction())
print(maJolieFonction('coucou'))


myVar1 = maJolieFonction('coucou')
print(myVar1)

def maJolieFonction(monParam1='toto'):
    return(monParam1)

from datetime import datetime
myDateDuJour= str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

print(myDateDuJour)
print(Retourner_votre_texte("Aujourd'hui, le " + myDateDuJour + ", \n", "j'aime programmer en langage PYTHON"))
    
#==============================================================================
#-- Les Procedures :
#==============================================================================
#-- Procédure executant une instruction avec des paramètres en entrée
def  Afficher_Bonjour ():
#    print("Bonjour !")
    a = 1
    b = 2
    print(b)
    c = a + b

Afficher_Bonjour()

myVar1 = Afficher_Bonjour()
print(myVar1)

###############################################################################
###############################################################################


#==============================================================================
#-- Les Structures de contrôles :
#==============================================================================

#------------------------------------------------------------------------------    
#-- Les conditions :
#------------------------------------------------------------------------------    


#-- IF ... ELSE
#------------------------------------------------------------------------------    
myStrTest = 'OK'

if (myStrTest == 'OK') : 
    print('OK !!')
else:
    print('Pas OK !!')


#-- IF ... ELIF .. ELSE
#------------------------------------------------------------------------------    
myStrTest = 'PAS BIEN'

if (myStrTest == 'OK') : 
    print('OK !!')
elif (myStrTest == 'KO'):
    print('Pas OK !!')
elif (myStrTest == 'GOOD'):
    print('OK !!')
else:
    print('Je ne connais pas le terme <' + myStrTest + '>')


#------------------------------------------------------------------------------    
#-- Les itérations
#------------------------------------------------------------------------------    

#-- FOR
#------------------------------------------------------------------------------    
myString = 'Ma phrase'
for i in range(0, len(myString)) :
    print( myString[i], '-', end='') #-- Astuce : le parametre end=’’ permet à l’instruction « print » de ne pas sauter de ligne par défaut

for i in range(4):
    print( "i a pour valeur" , i)

for i in [0, 1, 2, 3]:
    print( "i a pour valeur" , str( i ))

c = ["Marc", "est", "dans", "le", "jardin"]
for i in c:
    print("i vaut", i )

#-- WHILE
#------------------------------------------------------------------------------    
x = 1
while x < 10:
    print('x a pour valeur', x)
    x = x * 2
print("Fin")





###############################################################################
###############################################################################


#==============================================================================    
#-- Manipulation de chaînes de caractères :
#==============================================================================

#------------------------------------------------------------------------------
#-- SUB (Remplacer des chaines de caracteres dans une chaine de caracteres)
#------------------------------------------------------------------------------    
import re
#-- Utilisation des Regular Expression 
myHTMLCode  = '<BR><BR><li><div class="minor">Nous sommes mardi</div><BR><BR>'

print(myHTMLCode)
#-- RQ : pour les caractere utilisé par les expression des regular expression, 
#        les préfixer par backslash : ex . pour "/div" rechercher "\/div"
print(re.sub(r'(.*)<li><div class="minor">(.*)<\/div>(.*)', r'\2', myHTMLCode))
print(re.sub(r'(.*)<li><div class="minor">(.*)<\/div>(.*)', r'\1\2\3', myHTMLCode))



#------------------------------------------------------------------------------
#-- JOIN (concatener toutes les chaines d'une liste)
#------------------------------------------------------------------------------
myListStr = ('Je', 'suis', 'en', 'master', 'BI&BD')
print(myListStr)
print(' '.join(myListStr)) 


#------------------------------------------------------------------------------
#-- SPLIT
#------------------------------------------------------------------------------
myStr = ('Je suis en master BI&BD , les cours sont tres interressants, mais beaucoup de travail')
print(myStr)

myListStr = myStr.split() #-- Utilise le caractere espace par défaut pour séparateur
print(myListStr)

myListStr = myStr.split(',')
print(myListStr)

#------------------------------------------------------------------------------
#-- SPLITLINES 
#------------------------------------------------------------------------------
myStr = ('Je suis en master BI&BD,\n  les cours sont tres interressants\nmais beaucoup de travail')
myListStr = myStr.splitlines()
print(myListStr)




###############################################################################
###############################################################################


#==============================================================================
#-- Chargement de bibliothèque Python :
#==============================================================================
#-- C:\Users\....\AppData\Local\Continuum\anaconda3\Scripts\pip install NomDeLaBibliotheque


#==============================================================================
#-- Importation de bibliotheques et de variables :
#==============================================================================

#--Importation de bibliotheques et de variables contenu dans d'autres module python

#-- On importe toutes les variables et fonctions declarees dan le module « variables_fonctions_glassdoor »
from variables_fonctions_glassdoor import *

#-- On importe juste la variable « myNbrPagin » declaree dans le module « variables_fonctions_linkedin»
from variables_fonctions_linkedin import myNbrPagin



############################################################################### 
############################################################################### 
# - Extraction d'éléments d'information présents dans un fichier HTML (parser) 
# - Méthode de récupération du flux HTML selon origine Fichier ou Web
############################################################################### 
############################################################################### 


#==============================================================================
#==============================================================================
#-- Extraction d'information à partir d'un flux ou d'un fichier HTML en python
#==============================================================================
#==============================================================================

#------------------------------------------------------------------------------
#-- XPATH (A tester si necessaire)
#------------------------------------------------------------------------------
#-- Telecharger la bibliotheque xpath
#import xpath
#../..
#hxs = Selector(response)
#print( hxs.xpath( '//@href' ).extract() )
#../..

#------------------------------------------------------------------------------
#-- ETREE (A tester si necessaire)
#------------------------------------------------------------------------------
#from xml.etree.ElementTree import ElementTree
#import xml.etree.ElementTree as ET
#../..



############################################################################### 
#Exemple : GLASSDOOR (extraction INFOS SUR ENTREPRISE)
###############################################################################
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
#-----------------------------------------------------------------------------
#-- 1er CAS : Ouverture d'un fichier HTML sur le disque dur
#-----------------------------------------------------------------------------
#myHTMLPathFileName = "C:/TD_DATALAKE/DATALAKE/1_LANDING_ZONE/GLASSDOOR/SOC/13790-INFO-SOC-GLASSDOOR-E9028_P1.html"

#!!!!RQ-EKL: Utiliser le slash "/" et pas le backslash "\" pour le path avec beautifullsoup
myHTMLPathFileName = myPathHtml + "13550-INFO-SOC-GLASSDOOR-E10686_P1.html"
myHTMLPathFileName = myPathHtml + "13787-INFO-SOC-GLASSDOOR-E35333_P1.html"

print(myHTMLPathFileName)

f = open(myHTMLPathFileName, "r", encoding="utf8")
myHTMLContents = f.read()
f.close()

print(myHTMLContents)

#-----------------------------------------------------------------------------
#-- 2eme CAS : Ouverture d'un flux HTML sur le Web 
#-----------------------------------------------------------------------------
#import requests
#myURL = "https://www.glassdoor.fr/Pr%C3%A9sentation/Travailler-chez-Atos-EI_IE10686.16,20.htm"
#myHeaders = {'User-Agent': 'Mozilla/5.0'}
#myResponse = requests.get(str(myURL), headers=myHeaders)
#myHTMLContents = myResponse.text

#-----------------------------------------------------------------------------
#-- Commun aux 1er et 2eme CAS -  HTML File et URL
#-----------------------------------------------------------------------------
mySoup = BeautifulSoup(myHTMLContents, 'lxml')
print(mySoup.h2)
print(mySoup.head)
print(mySoup.li)	 
print(myHTMLContents)
print(mySoup.prettify())

#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant le nom de l'entreprise
#==============================================================================
import re
def Get_nom_entreprise_SOC(Soup):
    myTest = Soup.find_all('h1', attrs = {" strong tightAll"})[0]

    if (myTest == []) : 
        Result = 'NULL'
    else:
        myTxtTmp = str(myTest)
        Result = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', myTxtTmp)
    return(Result)


myTestTmp = mySoup.find_all('h1', attrs = {" strong tightAll"})[0]
print(myTestTmp)
#myVar2 = "<h1 class=' strong tightAll' title='' data-company='Atos'><span id=\"DivisionsDropdownComponent\">Atos</span></h1>"


myResultSoup = Get_nom_entreprise_SOC(mySoup)
print(myResultSoup)
#print(Get_nom_entreprise_SOC(mySoup))


#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant la ville de l'entreprise
#==============================================================================
import re
def Get_ville_entreprise_SOC(Soup):
    myTest = str(Soup.find_all('div', attrs = {'class':"infoEntity"})[1].span.contents[0])

    if (myTest == []) : 
        Result = 'NULL'
    else:
        myTxtTmp = str(myTest)
        myTxtTmp1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', myTxtTmp)
        Result = myTxtTmp1
    return(Result)

#print(Get_ville_entreprise_SOC(mySoup))


#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant la taille de l'entreprise
#==============================================================================
import re
def Get_taille_entreprise_SOC(Soup):
    myTest = str(Soup.find_all('div', attrs = {'class':"infoEntity"})[2].span.contents[0])

    if (myTest == []) : 
        Result = 'NULL'
    else:
        myTxtTmp = str(myTest)
        myTxtTmp1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', myTxtTmp)
        Result = myTxtTmp1
    return(Result)

#print(Get_taille_entreprise_SOC(mySoup))


#-- RECAP pour controle
print('"NOM_SOCIETE"', ";",  "\"" + Get_nom_entreprise_SOC(mySoup) + "\"")
print('"VILLE_SOCIETE"', ";", '"' + Get_ville_entreprise_SOC(mySoup) + '"')
print('"TAILLE_SOCIETE"', ";" , '"' + Get_taille_entreprise_SOC(mySoup) + '"')


#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant la description de l'entreprise 
#
# !!! ==> A FAIRE !!!
#
#==============================================================================
import re
def Get_description_entreprise_SOC(Soup):
#    myTest = str(mySoup.find_all('div', attrs = {'class':"infoEntity"})[1].span.contents[0])
    myTest = str(Soup.find_all('div', attrs = {'id':"EmpBasicInfo"}))
    #..........................................
    #..
    #... coder eventuellement des choses ici
    #.......
    #..........................................
    if (myTest == []) : 
        Result = 'NULL'
    else:
        Soup2 = Soup(myTest, 'lxml')
        myTxtTmp = str(Soup2.find_all('div', attrs = {'class':""})[2])
        myTxtTmp1 = re.sub(r'(.*)data-full="(.*).<br/>(.*)', r'\2', myTxtTmp)
        Result = myTxtTmp1
    return(Result)

#print(Get_description_entreprise_SOC(mySoup))


#-- A vous de le faire !!!
print(Get_description_entreprise_SOC(mySoup))



###############################################################################      
############################################################################### 
############################################################################### 
#
# Exemple : GLASSDOOR (extraction AVIS SUR ENTREPRISE)
#
############################################################################### 
############################################################################### 
###############################################################################     
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
#-----------------------------------------------------------------------------
#-- 1er CAS : Ouverture d'un fichier HTML sur le disque dur
#-----------------------------------------------------------------------------
myHTMLPathFileName = myPathHtml + "13550-AVIS-SOC-GLASSDOOR-E10686_P1.html"


f = open(myHTMLPathFileName, "r", encoding="utf8")
myHTMLContents = f.read()
f.close()

print(myHTMLContents)

#-----------------------------------------------------------------------------
#-- 2eme CAS : Ouverture d'un flux HTML sur le Web 
#-----------------------------------------------------------------------------
#import requests
#myURL = "https://???"
#myHeaders = {'User-Agent': 'Mozilla/5.0'}
#myResponse = requests.get(str(myURL), headers=myHeaders)
#myHTMLContents = myResponse.text

#-----------------------------------------------------------------------------
#-- Commun aux 1er et 2eme CAS -  HTML File et URL
#-----------------------------------------------------------------------------
mySoup = BeautifulSoup(myHTMLContents, 'lxml')
print(mySoup.h2)
print(mySoup.head)
print(mySoup.li)	 
print(mySoup.prettify())

#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant <datetime_ingestion>
#==============================================================================
from datetime import datetime
def Get_datetime_ingestion_AVI():
    Result = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return(Result)
    
#print(Get_datetime_ingestion_AVI())    

#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant <nom_entreprise>
#==============================================================================
def Get_nom_entreprise_AVI (Soup):
    myTest = Soup.find_all('div', attrs = {"class":"header cell info"})[0].span.contents[0]
    if (myTest == []) : 
        Result = 'NULL'
    else:
        Result = myTest
    return(Result)

#print(Get_nom_entreprise_AVI(mySoup))



#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant <Note_moy_entreprise>
#==============================================================================
def Get_note_moy_entreprise_AVI(Soup):
    myTest = Soup.find_all('div', attrs = {'class':'v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large'})[0].contents[0]
    if (myTest == []) : 
        Result = 'NULL'
    else:
        Result = myTest  
    return(Result)

#print(Get_note_moy_entreprise_AVI(mySoup))


#-- RECAP pour controle
print(Get_datetime_ingestion_AVI())    
print(Get_nom_entreprise_AVI(mySoup))
print(Get_note_moy_entreprise_AVI(mySoup))


#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
myTest = mySoup.find_all('li', attrs = {'class':'empReview'})
#print(myTest)
#------------------------------------------------------------------------------
# Date Time d'Ingestion de la donnee
#------------------------------------------------------------------------------
myDatetime_Ingestion = Get_datetime_ingestion_AVI()
   
#--------------------------------------------------------------------------    
#myIDEntreprise = Id_Entreprise
#print("\n *** ID Entreprise : " +  str(myIDEntreprise))

#--------------------------------------------------------------------------
myNomEntreprise = Get_nom_entreprise_AVI(mySoup)
#print("\n*** NOM Entreprise : " +  str(myNomEntreprise))

#--------------------------------------------------------------------------    
myNote_moy_entreprise = Get_note_moy_entreprise_AVI(mySoup)
#print("\n Note moyenne de la societe : " + myNote_moy_entreprise)
	
#------------------------------------------------------------------------------
# Traitement de sortie si pas de page trouvee a l Url
#------------------------------------------------------------------------------
if (myTest == []) : 
    print("NULL")
else:
    myListTab=[[]]
#    print(myListTab)

    #------------------------------------------------------------------------------
    # Traitement de chaque fiche avis saisie sur la page web
    #------------------------------------------------------------------------------
    for x in range(0, len(myTest)) :
        #--------------------------------------------------------------------------
        #-- 0 - ID de l'avis (arbitraire) incremental
        #--------------------------------------------------------------------------
        if x == 0: 
            myListTab[0] = ['"0"']
        else:
            myListTab.append(['"'+str(x)+'"'])
            print("Avis n° : " + str(x+1) )
    
        #--------------------------------------------------------------------------
        #-- On recupere par une boucle les donnees XML de chaque avis
        #--------------------------------------------------------------------------
        soup2 = BeautifulSoup(str(myTest[x]), 'lxml')
    
        #--------------------------------------------------------------------------
        #-- 1 - Note moyenne entreprise 
        #--------------------------------------------------------------------------
        txtclean = (Get_note_moy_entreprise_AVI(mySoup))
        myListTab[x].append('"' + txtclean + '"')
        print(x, txtclean)
        
    
        #--------------------------------------------------------------------------
        #-- 2 - Date Time 
        #--------------------------------------------------------------------------
        txtclean = Get_datetime_ingestion_AVI()
        myListTab[x].append('"' + txtclean + '"')
    
        #--------------------------------------------------------------------------
        #-- 3 - Titre de l'avis de l'employe sur la societe (review)
        #--------------------------------------------------------------------------
#        txtclean = Get_review_titre ('GLASSDOOR', soup2 )
#        myListTab[x].append('"' + txtclean + '"')
    
        #--------------------------------------------------------------------------
        #-- 5 - Employe actuel
        #--------------------------------------------------------------------------
        myTest2 = soup2.find_all('span', attrs = {'class':'authorJobTitle middle reviewer'})
        if (myTest2 == []) :        
            myListTab[x].append('NULL')
        else :
            txtclean = re.sub(r'<span (.*)">(.*)</span>(.*)', r'\2', str(myTest2[0]))
            print(txtclean)
            myListTab[x].append('"' + txtclean + '"')
    
        #--------------------------------------------------------------------------
        #-- 6 - Ville de l'employe 
        #--------------------------------------------------------------------------
        myTest2 = soup2.find_all('span', attrs = {'class':'authorLocation'}) 
        if (myTest2 == []) :
            myListTab[x].append('NULL')
        else :
            txtclean = re.sub(r'<span (.*)">(.*)</span>(.*)', r'\2', str(myTest2[0]))
            print(txtclean)
            myListTab[x].append('"' + txtclean + '"')
    
        #--------------------------------------------------------------------------
        #-- 7 - Commentaire texte libre employe sur entreprise
        #--------------------------------------------------------------------------
        myTest2= soup2.find_all('p', attrs = {'class':'mainText mb-0'}) 
    
        if (myTest2 == []) :        
            myListTab[x].append('NULL')
        else :
            txtclean = myTest2[0].text
            print(txtclean)
            myListTab[x].append('"' + txtclean + '"')

#==============================================================================

for mySousListeTab in myListTab : print(str(mySousListeTab[3]))
    
    
###############################################################################     
############################################################################### 
############################################################################### 
#
# Exemple : LINKEDIN (INFOS EMPLOIS)
#
############################################################################### 
############################################################################### 
############################################################################### 
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

#-- 1er CAS : Ouverture d'un fichier HTML sur le disque dur
myHTMLPathFileName = myPathHtml + "13551-INFO-EMP-LINKEDIN-FR-1602929951.html"

f = open(myHTMLPathFileName, "r", encoding="utf8")
myHTMLContents = f.read()
f.close()

print(myHTMLContents)

#-- 2eme CAS : Ouverture d'un flux HTML sur le Web 
#import requests
#myURL = "https://fr.linkedin.com/jobs/view/data-analyst-f-h-at-intitek-1602929951"
#myHeaders = {'User-Agent': 'Mozilla/5.0'}
#myResponse = requests.get(str(myURL), headers=myHeaders)
#myHTMLContents = myResponse.text

#------------------------------
#-- 1er et 2eme CAS -  HTML File et URL
mySoup = BeautifulSoup(myHTMLContents, 'lxml')
print(mySoup.h2)
print(mySoup.head)
print(mySoup.li)	 
print(mySoup.prettify())


#==============================================================================
#-- LINKEDIN (EMPLOI) : Libellé de l'offre
#==============================================================================
def Get_libelle_emploi_EMP(Soup):
    myTest = Soup.find_all('h1', attrs = {'class':'topcard__title'}) 
    if (myTest == []) : 
        Result = 'NULL'
    else:
        myTest = str(myTest[0].text)
        if (myTest == []) : 
            Result = 'NULL'
        else:
            Result = myTest
    return(Result)

#print(Get_libelle_emploi_EMP(mySoup))


#==============================================================================
#-- LINKEDIN (EMPLOI) : Nom de la Société demandeuse
#==============================================================================
def Get_nom_entreprise_EMP(Soup):
    myTest = Soup.find_all('span', attrs = {'class':'topcard__flavor'}) 
    if (myTest == []) : 
        Result = 'NULL'
    else:
        myTest = str(myTest[0].text)
        if (myTest == []) : 
            Result = 'NULL'
        else:
            Result = myTest
    return(Result)

#print(Get_nom_entreprise_EMP(mySoup))



#==============================================================================
#-- LINKEDIN (EMPLOI) : Ville de l'emploi proposé
#==============================================================================
def Get_ville_emploi_EMP (Soup):
    myTest = Soup.find_all('span', attrs = {'class':'topcard__flavor topcard__flavor--bullet'}) 
    if (myTest == []) : 
        Result = 'NULL'
    else:
        myTest = str(myTest[0].text)
        if (myTest == []) : 
            Result = 'NULL'
        else:
            Result = myTest
    return(Result)

#print(Get_ville_emploi_EMP(mySoup))


#==============================================================================
#-- LINKEDIN (EMPLOI) : Texte de l'offre d'emploi
#==============================================================================
def Get_texte_emploi_EMP (Soup):
    myTest = Soup.find_all('div', attrs = {"description__text description__text--rich"})
    if (myTest == []) : 
        Result = 'NULL'
    else:
        myTest = str(myTest[0].text)
        if (myTest == []) : 
            Result = 'NULL'
        else:
            Result = myTest
    return(Result)

#print(Get_texte_emploi_EMP(mySoup))


#-- RECAP pour controle
print(Get_libelle_emploi_EMP(mySoup))
print(Get_nom_entreprise_EMP(mySoup))
print(Get_ville_emploi_EMP(mySoup))
print(Get_texte_emploi_EMP(mySoup))
