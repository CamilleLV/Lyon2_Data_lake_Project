# -*- coding: utf-8 -*-

#======================================================================================
#  Auteur: Eric KLOECKLE
#  Etablissement: Université Lumière Lyon 2 - Bron
#  Cursus: Master 2  BI&A : « Business Intelligence & Analytics » 
#  Domaine: « Gestion de données massives »
#  Cours: Enseignement TD Datalake-House
# 
#-------------------------------------------------------------------------------------- 
#  02-PHASE-2_Extraction_des_donnéees_descriptives_de_la_LANDINGZONE_vers_la_CURATED-ZONE_v0.01.py
#======================================================================================


############################################################################### 
############################################################################### 
#
# Use Case n°1 : GLASSDOOR => Extraction "INFOS SUR ENTREPRISE"
#
############################################################################### 
############################################################################### 

#==============================================================================
# Chargement de la librairie python de "parsing" XML/HTML
#==============================================================================
from bs4 import BeautifulSoup


#==============================================================================
# Méthode de récupération des données source à ingérer dans le DataLake
#  - A partir d'un fichier HTML stocké sur un filesystem (ex.: disque dur du PC)
#  - A partir d'une URL pointant directement le site d'emploi originel (ex.: www.linkedin.com)
#==============================================================================

#-----------------------------------------------------------------------------
#-- 1er CAS : Ouverture d'un fichier HTML stocké sur le disque dur
# 
#  ==> Type de fichier : *INFO-SOC-GLASSDOOR*.html
#------------------------------------------------------------------------------

#-----------------------------------------------------------------------------
repertoire_des_fichiers_html = 'C:\\TD_DATALAKE\\DATALAKE\\0_SOURCE_WEB'
# print(repertoire_des_fichiers_html)
nom_de_fichier_html = "13546-INFO-SOC-GLASSDOOR-E12966_P1.html"
# print(repertoire_des_fichiers_html)

#-- Fichiers HTML concernés : *INFO-SOC*.html
chemin_du_fichier_html = repertoire_des_fichiers_html + "\\" + nom_de_fichier_html
# print(chemin_du_fichier_html)

objet_fichier_html = open(chemin_du_fichier_html, "r", encoding="utf8")
texte_source_html = objet_fichier_html.read()
objet_fichier_html.close()

# print(texte_source_html)

#-----------------------------------------------------------------------------
#-- 2eme CAS : Ouverture d'un flux HTML sur le Web 
#-----------------------------------------------------------------------------
# import requests
# url_de_site_web = "https://www.glassdoor.fr/Pr%C3%A9sentation/"
# # print(repertoire_des_fichiers_html)
# nom_de_page_html = "Travailler-chez-Atos-EI_IE10686.16,20.htm"
# # print(repertoire_des_fichiers_html)

# chemin_de_URL = url_de_site_web + "/" +  nom_de_page_html
# entete_http = {'User-Agent': 'Mozilla/5.0'}
# reponse_http = requests.get(str(chemin_de_URL), headers=entete_http)
# texte_source_html = reponse_http.text
# # print(texte_source_html)

#-----------------------------------------------------------------------------
#-- Commun aux 1er et 2eme CAS -  HTML File et URL
#-----------------------------------------------------------------------------
from bs4 import BeautifulSoup

objet_parser_html = BeautifulSoup(texte_source_html, 'lxml')

# print(objet_parser_html.h2)
# print(objet_parser_html.head)
# print(objet_parser_html.li)	 
# print(texte_source_html)
# print(objet_parser_html.prettify())



#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant le nom de l'entreprise
#==============================================================================
import re
def extraire_nom_entreprise_SOC(objet_html):
    texte_tmp = objet_html.find_all('h1', attrs = {'class':"strong tightAll"})[0].span.contents[0]
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        resultat = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
    return(resultat)

# print(extraire_nom_entreprise_SOC(objet_parser_html))



#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant la ville de l'entreprise
#==============================================================================
import re
def extraire_ville_entreprise_SOC(objet_html):
    texte_tmp = str(objet_html.find_all('div', attrs = {'class':"infoEntity"})[1].span.contents[0])

    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        texte_tmp_1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
        resultat = texte_tmp_1
    return(resultat)

# print(extraire_ville_entreprise_SOC(objet_parser_html))



#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant la taille de l'entreprise
#==============================================================================
import re
def extraire_taille_entreprise_SOC(objet_html):
    texte_tmp = str(objet_html.find_all('div', attrs = {'class':"infoEntity"})[2].span.contents[0])

    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        texte_tmp_1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
        resultat = texte_tmp_1
    return(resultat)

# print(extraire_taille_entreprise_SOC(objet_parser_html))


# -----------------------------------------------------------------------------
#-- RECAP control des fonctions d'extraction de données du html sur :
#   Les informations sur les sociétés : site web GLASDOOR
# -----------------------------------------------------------------------------
print()
print('='*80)
print("INFO SOC GLASSDOOR - nom de la société ==> " + extraire_nom_entreprise_SOC(objet_parser_html) + "\"")
print("INFO SOC GLASSDOOR - ville de la société ==> " +  extraire_ville_entreprise_SOC(objet_parser_html) + '"')
print("INFO SOC GLASSDOOR - taille de la société ==> " +  extraire_taille_entreprise_SOC(objet_parser_html) + '"')
print('='*80)


# #==============================================================================
# #-- GLASSDOOR (SOCIETE) : Fonction renvoyant la description de l'entreprise 
# #
# # !!! ==> A FAIRE !!!
# #
# #==============================================================================
# import re
# def extraire_description_entreprise_SOC(objet_html):
# #    texte_tmp = str(objet_parser_html.find_all('div', attrs = {'class':"infoEntity"})[1].span.contents[0])
#     texte_tmp = str(objet_html.find_all('div', attrs = {'id':"EmpBasicInfo"}))
#     #..........................................
#     #..
#     #... coder eventuellement des choses ici
#     #.......
#     #..........................................
#     if (texte_tmp == []) : 
#         resultat = 'NULL'
#     else:
#         objet_html_2 = objet_html(texte_tmp, 'lxml')
#         texte_tmp = str(objet_html_2.find_all('div', attrs = {'class':""})[2])
#         texte_tmp_1 = re.sub(r'(.*)data-full="(.*).<br/>(.*)', r'\2', texte_tmp)
#         resultat = texte_tmp_1
#     return(resultat)

# #-- A vous de le faire !!!
# print(extraire_description_entreprise_SOC(objet_parser_html))






############################################################################### 
############################################################################### 
#
# Use Case n°2 : GLASSDOOR => Extraction "AVIS SUR ENTREPRISE"
#
############################################################################### 
############################################################################### 

from bs4 import BeautifulSoup
#------------------------------------------------------------------------------
#-- 1er CAS : Ouverture d'un fichier HTML sur le disque dur
# 
#  ==> Type de fichier : *AVI-SOC-GLASSDOOR*.html
#------------------------------------------------------------------------------

chemin_du_fichier_html = repertoire_des_fichiers_html + "\\" + "13551-AVIS-SOC-GLASSDOOR-E794111_P1.html"
# print(chemin_du_fichier_html)

objet_fichier_html = open(chemin_du_fichier_html, "r", encoding="utf8")
texte_source_html = objet_fichier_html.read()
objet_fichier_html.close()
# print(texte_source_html)

#------------------------------------------------------------------------------
#-- 2eme CAS : Ouverture d'un flux HTML sur le Web 
#------------------------------------------------------------------------------
#  ==> Comme la section  [Use Case n°1 : GLASSDOOR => Extraction "INFOS SUR ENTREPRISE")]
#  Mais changer : chemin_de_URL = "https://www.glassdoor.fr/Avis/Atos-Avis-E10686.htm"

#-----------------------------------------------------------------------------
#-- Commun aux 1er et 2eme CAS -  HTML File et URL
#-----------------------------------------------------------------------------
objet_parser_html = BeautifulSoup(texte_source_html, 'lxml')

# print(objet_parser_html.h2)
# print(objet_parser_html.head)
# print(objet_parser_html.li)	 
# print(objet_parser_html.prettify())



#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant <nom_entreprise>
#==============================================================================
def extraire_nom_entreprise_AVI (objet_html):
    texte_tmp = objet_html.find_all('div', attrs = {"class":"header cell info"})[0].span.contents[0]
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        resultat = texte_tmp
    return(resultat)

# print(extraire_nom_entreprise_AVI(objet_parser_html))



#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant <Note_moy_entreprise>
#==============================================================================
def extraire_note_moy_entreprise_AVI(objet_html):
    texte_tmp = objet_html.find_all('div', attrs = {'class':'v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large'})[0].contents[0]
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        resultat = texte_tmp  
    return(resultat)

print(extraire_note_moy_entreprise_AVI(objet_parser_html))


# -----------------------------------------------------------------------------
#-- RECAP control des fonctions d'extraction de données du html sur :
#   Les avis sur les sociétés : site web GLASDOOR
# -----------------------------------------------------------------------------
print()
print('='*80)
print("AVIS SOC GLASSDOOR - nom de la société ==> " + extraire_nom_entreprise_AVI(objet_parser_html) + "\"")
print("AVIS SOC GLASSDOOR - note moyenne sur la société ==> " +  extraire_note_moy_entreprise_AVI(objet_parser_html) + '"')
print('='*80)


#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant sous forme d'une liste les avis
#                      des employés contenu dans la page web des avis société
#==============================================================================
def extraire_liste_avis_employes_sur_entreprise_AVI(objet_html):
    #------------------------------------------------------------------------------
    # Traitement de sortie si pas de page trouvee a l Url
    #------------------------------------------------------------------------------
    texte_tmp = objet_parser_html.find_all('li', attrs = {'class':'empReview'})
    # print(texte_tmp)
    
    if (texte_tmp == []) : 
        pass
        # print("NULL")
    else:
        liste_de_page_web=[[]]
    #    print(liste_de_page_web)
    
        #------------------------------------------------------------------------------
        # Traitement de chaque fiche avis saisie sur la page web
        #------------------------------------------------------------------------------
        for x in range(0, len(texte_tmp)) :
            #--------------------------------------------------------------------------
            #-- 0 - ID de l'avis (arbitraire) incremental
            #--------------------------------------------------------------------------
            if x == 0: 
                liste_de_page_web[0] = ['"0"']
            else:
                liste_de_page_web.append(['"'+str(x)+'"'])
                # print("Avis n° : " + str(x+1) )
        
            #--------------------------------------------------------------------------
            #-- On recupere par une boucle les donnees XML de chaque avis
            #--------------------------------------------------------------------------
            objet_html_2 = BeautifulSoup(str(texte_tmp[x]), 'lxml')
        
            #--------------------------------------------------------------------------
            #-- 1 - Note moyenne entreprise 
            #--------------------------------------------------------------------------
            texte_tmp = (extraire_note_moy_entreprise_AVI(objet_parser_html))
            liste_de_page_web[x].append('"' + texte_tmp + '"')
            # print(x, texte_tmp)
            
        
            #--------------------------------------------------------------------------
            #-- 2 - Date Time 
            #--------------------------------------------------------------------------
            # texte_tmp = donner_datetime_actuel()
            # liste_de_page_web[x].append('"' + texte_tmp + '"')
        
            #--------------------------------------------------------------------------
            #-- 3 - Titre de l'avis de l'employe sur la societe (review)
            #--------------------------------------------------------------------------
            # texte_tmp = extraire_review_titre ('GLASSDOOR', objet_html_2 )
            # liste_de_page_web[x].append('"' + texte_tmp + '"')
        
            #--------------------------------------------------------------------------
            #-- 5 - Employe actuel
            #--------------------------------------------------------------------------
            texte_html_trouve = objet_html_2.find_all('span', attrs = {'class':'authorJobTitle middle reviewer'})
            if (texte_html_trouve == []) :        
                liste_de_page_web[x].append('NULL')
            else :
                texte_tmp = re.sub(r'<span (.*)">(.*)</span>(.*)', r'\2', str(texte_html_trouve[0]))
                # print(texte_tmp)
                liste_de_page_web[x].append('"' + texte_tmp + '"')
        
            #--------------------------------------------------------------------------
            #-- 6 - Ville de l'employe 
            #--------------------------------------------------------------------------
            texte_html_trouve = objet_html_2.find_all('span', attrs = {'class':'authorLocation'}) 
            if (texte_html_trouve == []) :
                liste_de_page_web[x].append('NULL')
            else :
                texte_tmp = re.sub(r'<span (.*)">(.*)</span>(.*)', r'\2', str(texte_html_trouve[0]))
                # print(texte_tmp)
                liste_de_page_web[x].append('"' + texte_tmp + '"')
        
            #--------------------------------------------------------------------------
            #-- 7 - Commentaire texte libre employe sur entreprise
            #--------------------------------------------------------------------------
            texte_html_trouve= objet_html_2.find_all('p', attrs = {'class':'mainText mb-0'}) 
        
            if (texte_html_trouve == []) :        
                liste_de_page_web[x].append('NULL')
            else :
                texte_tmp = texte_html_trouve[0].text
                # print(texte_tmp)
                liste_de_page_web[x].append('"' + texte_tmp + '"')
    
            #--------------------------------------------------------------------------
            #-- 8 - Avantages
            #--------------------------------------------------------------------------
            texte_html_trouve= objet_html_2.find_all('div', attrs = {'class':'mt-md common__EiReviewTextStyles__allowLineBreaks'}) 
        
            # print(texte_html_trouve)
            if (texte_html_trouve == []) :        
                liste_de_page_web[x].append('NULL')
            else :
                texte_tmp = texte_html_trouve[0].text
                # print(texte_tmp)
                liste_de_page_web[x].append('"' + texte_tmp + '"')
    
    
            #--------------------------------------------------------------------------
            #-- 9 - Inconvénients
            #--------------------------------------------------------------------------
            texte_html_trouve= objet_html_2.find_all('div', attrs = {'class':'mt-md common__EiReviewTextStyles__allowLineBreaks'}) 
        
            # print(texte_html_trouve)
            if (texte_html_trouve == []) :        
                liste_de_page_web[x].append('NULL')
            else :
                texte_tmp = texte_html_trouve[1].text
                # print(texte_tmp)
                liste_de_page_web[x].append('"' + texte_tmp + '"')

    return(liste_de_page_web)            
#==============================================================================


#------------------------------------------------------------------------------
#  Exemple d'affichage des éléments contenus dans la liste créé à partir
#  de l'extraction des avis contenus dans une même page web.
#------------------------------------------------------------------------------

liste_de_page_web = extraire_liste_avis_employes_sur_entreprise_AVI(objet_parser_html)

print(); print("*" * 80)
print("* Exemple d'extraction des plusieurs avis contenus dans une même page web")
print("*" * 80, '\n')
print("-" * 80)
for sous_liste_de_page_web in liste_de_page_web : 
    print(str(sous_liste_de_page_web))
    print("-" * 80)
print(); print("*" * 80)   
    

    
    
############################################################################### 
############################################################################### 
#
# Use Case n°3 : LINKEDIN => Extraction "INFOS OFFRES D'EMPLOIS"
#
############################################################################### 
############################################################################### 
from bs4 import BeautifulSoup

#-----------------------------------------------------------------------------
#-- 1er CAS : Ouverture d'un fichier HTML sur le disque dur
# 
#  ==> Type de fichier : *INFO-EMP-LINKEDIN*.html
#------------------------------------------------------------------------------

chemin_du_fichier_html = repertoire_des_fichiers_html + "\\" + "13552-INFO-EMP-LINKEDIN-FR-1599166885.html"
# print(chemin_du_fichier_html)

objet_fichier_html = open(chemin_du_fichier_html, "r", encoding="utf8")
texte_source_html = objet_fichier_html.read()
objet_fichier_html.close()

# print(texte_source_html)


#-----------------------------------------------------------------------------
#-- 2eme CAS : Ouverture d'un flux HTML sur le Web 
#-----------------------------------------------------------------------------
#  ==> Comme la section  [Use Case n°1 : GLASSDOOR => Extraction "INFOS SUR ENTREPRISE")]
#  Mais changer : chemin_de_URL = "https://fr.linkedin.com/jobs/view/data-analyst-f-h-at-intitek-1602929951"

#-----------------------------------------------------------------------------
#-- 1er et 2eme CAS -  HTML File et URL
#-----------------------------------------------------------------------------
objet_parser_html = BeautifulSoup(texte_source_html, 'lxml')

# print(objet_parser_html.h2)
# print(objet_parser_html.head)
# print(objet_parser_html.li)	 
# print(objet_parser_html.prettify())


#==============================================================================
#-- LINKEDIN (EMPLOI) : Libellé de l'offre
#==============================================================================
def extraire_libelle_emploi_EMP(objet_html):
    texte_tmp = objet_html.find_all('h1', attrs = {'class':'topcard__title'}) 
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)

# print(extraire_libelle_emploi_EMP(objet_parser_html))



#==============================================================================
#-- LINKEDIN (EMPLOI) : Nom de la Société demandeuse
#==============================================================================
def extraire_nom_entreprise_EMP(objet_html):
    texte_tmp = objet_html.find_all('span', attrs = {'class':'topcard__flavor'}) 
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)

# print(extraire_nom_entreprise_EMP(objet_parser_html))



#==============================================================================
#-- LINKEDIN (EMPLOI) : Ville de l'emploi proposé
#==============================================================================
def extraire_ville_emploi_EMP (objet_html):
    texte_tmp = objet_html.find_all('span', attrs = {'class':'topcard__flavor topcard__flavor--bullet'}) 
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)

# print(extraire_ville_emploi_EMP(objet_parser_html))



#==============================================================================
#-- LINKEDIN (EMPLOI) : Texte de l'offre d'emploi
#==============================================================================
def extraire_texte_emploi_EMP (objet_html):
    texte_tmp = objet_html.find_all('div', attrs = {"description__text description__text--rich"})
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)

# print(extraire_texte_emploi_EMP(objet_parser_html))



# -----------------------------------------------------------------------------
#-- RECAP control des fonctions d'extraction de données du html sur :
#   Les offres d'emplois proposée : site web LINKEDIN
# -----------------------------------------------------------------------------
print()
print('=' * 80)
print("INFO EMP LINKEDIN - nom de la société ==> " + extraire_nom_entreprise_EMP(objet_parser_html))
print("INFO EMP LINKEDIN - ville de l'emploi ==> " + extraire_ville_emploi_EMP(objet_parser_html))
print("INFO EMP LINKEDIN - libellé de l'emploi ==> " + extraire_libelle_emploi_EMP(objet_parser_html))
print('-' * 80)
print("INFO EMP LINKEDIN - texte descriptif de l'emploi ==> \n" + extraire_texte_emploi_EMP(objet_parser_html))
print('=' * 80)
