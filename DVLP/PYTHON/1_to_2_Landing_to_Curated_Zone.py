#==============================================================================
#-- Import des bibliotheque
from fonctions_camille import * # type: ignore
import sys, os, fnmatch
import datetime
import csv
import re
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


#-- Initialisation des variables
# Path LANDING ZONE
myPathHtmlIn = "./DATALAKE/1_LANDING_ZONE"


# Path sous repertoires LANDING ZONE
myPathLandingZoneGlassdoorAVIS = "./DATALAKE/1_LANDING_ZONE/GLASSDOOR/AVIS"
myPathLandingZoneGlassdoorSOC = "./DATALAKE/1_LANDING_ZONE/GLASSDOOR/SOC"
myPathLandingZoneLinkedInEMP = "./DATALAKE/1_LANDING_ZONE/LINKEDIN/EMP"

# Path CURATED ZONE (Déplacé dans le dossier METADATA pour centraliser les fichiers CSV de métadonnées)
myPathCuratedZone = "./DATALAKE/00_METADATA"

#==============================================================================
#-- Puisque nous avons fait le choix de stocker les données dans des fichiers
#-- CSV, la "mise à jour" d'une ligne par rapport à un ID est plus complexe.
#-- Nous supprimons donc dans ce contexte de projet étudiant les lignes
#-- doublons du fichier METADATA_CURATED_ZONE.csv à la fin de l'éxecution de ce
#-- script.
#==============================================================================
def deduplicate_csv_file(filepath: str, csv_separator: str = ';'):
    """
    Lit un fichier CSV sans en-tête, supprime les lignes
    entièrement identiques, et réécrit le fichier propre.
    """
    try:
        # 1. Lire le fichier CSV
        # header=None : Spécifie que votre fichier n'a pas de ligne d'en-tête
        df = pd.read_csv(filepath, sep=csv_separator, header=None, engine='python')

        # 2. Compter les lignes avant suppression
        rows_before = len(df)

        # 3. Supprimer les doublons (garde la première occurrence par défaut)
        df_unique = df.drop_duplicates()

        # 4. Compter les lignes après suppression
        rows_after = len(df_unique)

        # 5. Réécrire le fichier propre
        # header=False : Ne pas écrire de ligne d'en-tête
        # index=False : Ne pas écrire l'index de pandas dans le fichier
        df_unique.to_csv(filepath, sep=csv_separator, header=False, index=False)

        print(f"\nNettoyage des doublons terminé pour : {filepath}")
        print(f"Lignes avant : {rows_before}")
        print(f"Lignes supprimées : {rows_before - rows_after}")
        print(f"Lignes après : {rows_after}")

    except pd.errors.EmptyDataError:
        # Le fichier est vide, rien à faire
        print(f"Le fichier {filepath} est vide. Aucun doublon à supprimer.")
    except Exception as e:
        print(f"Erreur lors du dédoublonnage du fichier {filepath}: {e}")


#==============================================================================
#-- Fonction permettant de nettoyer les textes récupérés
#==============================================================================
def clean_text(s: str) -> str:
    if not s:
        return "NULL"  # Retourner "NULL" textuel est souvent mieux pour le CSV final que ""
    
    # 1. Remplacer les points-virgules par des virgules (CRUCIAL si votre CSV est séparé par ;)
    s = s.replace(";", ",") 
    
    # 2. Remplacer tous les types de retours à la ligne et tabulations par un espace
    # \r, \n, \t, et le saut de page \f
    s = s.replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("\f", " ")
    
    # 3. Supprimer les guillemets simples et doubles qui cassent souvent les CSV
    s = s.replace('"', "'").replace("”", "'").replace("“", "'")
    
    # 4. Remplacer les espaces insécables (non-breaking space \xa0) qui traînent souvent dans le HTML
    s = s.replace(u'\xa0', ' ')

    # 5. Nettoyer les espaces multiples (remplace "  " par " ")
    s = " ".join(s.split())
    
    return s


#==============================================================================
#-- Crée le prompt pour l'API Gemini pour extraire les informations
#-- de la description d'une offre d'emploi
#==============================================================================
def prompt_gemini_emplois_description(texte_emploi: str):

    # Pour l'instant je le laisse désactivé 
    # return("NULL;NULL;NULL;NULL;NULL;NULL")
    try:
        """
        Génère une description des emplois en utilisant l'API Gemini de Google.
        """

        # print("Clé API Gemini utilisée :", GEMINI_API_KEY)
        genai.configure(api_key=GEMINI_API_KEY) #type: ignore

        # print('Available base models:', [m.name for m in genai.list_models()]) #type: ignore

        # Créez une instance du modèle
        # print("Modèle Gemini chargé")
        model = genai.GenerativeModel("models/gemini-2.5-pro") #type: ignore

        # Posez votre question
        # print("Génération de la réponse en cours...")
        response = model.generate_content(
            texte_emploi+""" Sert toi uniquement du texte ci-dessus pour répondre à ma demande. Je veux que tu sois conscis et que tu me donnes à partir du texte précédent
            différentes informations pour ces champs : 
            - Nom de l'entreprise
            - niveau de formation demandé
            - niveau d'éxperience demandé
            - technologie principale
            - soft skill principal
            - missions
        Le résultat doit être de la forme type CSV séparé par des points-virgules.
        
        Chaque colonne correspond au resultat d'un champ demandé plus haut, pour les missions, 
        je veux que le texte soit récupéré entre guillemets. Pour les autres champs, ils doivent être très simples 
        (BAC+3 = 3 pour le champ "niveau de formation demandé" par exemple)
        Ne donne pas d'explications supplémentaires, juste le résultat au format demandé (liste séparée par des ;)
        """)

        # response = model.generate_content("""résume moi le texte suivant en une phrase courte et concise : """+texte_emploi)

        return(response.text)
    except Exception as e:
        print("Erreur lors de l'appel à l'API Gemini :", str(e))
        return("NULL;NULL;NULL;NULL;NULL;NULL")


#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant le nom de l'entreprise
#==============================================================================
def extraire_nom_entreprise_SOC(objet_html):
    texte_tmp = objet_html.find_all('h1', class_="strong tightAll")[0].span.contents[0]
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        resultat = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
    return(resultat)


#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant la ville de l'entreprise
#==============================================================================
def extraire_ville_entreprise_SOC(objet_html):
    texte_tmp = str(objet_html.find_all('div', class_="infoEntity")[1].span.contents[0])

    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        texte_tmp_1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
        resultat = texte_tmp_1
    return(resultat)


#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant la taille de l'entreprise
#==============================================================================
def extraire_taille_entreprise_SOC(objet_html):
    texte_tmp = str(objet_html.find_all('div', class_="infoEntity")[2].span.contents[0])

    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        texte_tmp_1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
        resultat = texte_tmp_1
    return(resultat)


#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant le type de la société
#==============================================================================
def extraire_type_entreprise_SOC(objet_html):
    texte_tmp = str(objet_html.find_all('div', class_="infoEntity")[4].span.contents[0])

    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        texte_tmp_1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
        resultat = texte_tmp_1
    return(resultat)

#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant le secteur de la société
#==============================================================================
def extraire_secteur_entreprise_SOC(objet_html):
    texte_tmp = str(objet_html.find_all('div', class_="infoEntity")[5].span.contents[0])

    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        texte_tmp_1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
        resultat = texte_tmp_1
    return(resultat)


#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant le siège social de la société
#==============================================================================
def extraire_siege_social_entreprise_SOC(objet_html):
    texte_tmp = str(objet_html.find_all('div', class_="infoEntity")[1].span.contents[0])

    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        texte_tmp_1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
        resultat = texte_tmp_1
    return(resultat)


#==============================================================================
#-- GLASSDOOR (SOCIETE) : Fonction renvoyant la date de création de l'entreprise
#==============================================================================
def extraire_date_creation_entreprise_SOC(objet_html):
    texte_tmp = str(objet_html.find_all('div', class_="infoEntity")[3].span.contents[0])

    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp)
        texte_tmp_1 = re.sub(r'(.*)<h1 class=" strong tightAll" data-company="(.*)" title="">(.*)', r'\2', texte_tmp)
        resultat = texte_tmp_1
    return(resultat)


#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant <nom_entreprise>
#==============================================================================
def extraire_nom_entreprise_AVI(objet_html):
    texte_tmp = objet_html.find_all('div', class_="header cell info")[0].span.contents[0]
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
    texte_tmp = objet_html.find('div', class_='v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large')
    if texte_tmp: 
        resultat = texte_tmp.get_text(strip=True)
    else:
        resultat = 'NULL'
    return(resultat)


#==============================================================================
#-- GLASSDOOR (AVIS) : Fonction renvoyant sous forme d'une liste les avis
#                      des employés contenu dans la page web des avis société
#==============================================================================
def extraire_liste_avis_employes_sur_entreprise_AVI(rev):
    
    objet_html_2 = BeautifulSoup(str(rev), 'html.parser')

    # 2 - Note de l'avis employe
    # Sélection de toutes les étoiles du bloc principal
    stars = objet_html_2.select(".gdStars .star")

    avis_note = 0

    for star in stars:
        # Le <i style="width:0%"> est dans le parent (ou en sibling) selon ton snippet.
        parent = star.parent if isinstance(star.parent, Tag) else None
        style_attr = ""

        if parent:
            # On prend le premier <i> enfant du parent (c'est celui qui porte parfois style)
            first_inner_i = parent.find("i")
            if isinstance(first_inner_i, Tag):
                style_attr = first_inner_i.attrs.get("style", "")

        # Si style contient width:0% => étoile vide, sinon étoile remplie
        if "width:0%" in style_attr:
            # étoile vide -> rien à faire
            continue
        else:
            avis_note += 1

    # 5 - Employe actuel (author job title)
    try:
        avis_etat_emploi = objet_html_2.find('span', class_='authorJobTitle middle reviewer').get_text(strip=True) # type: ignore
    except AttributeError:
        avis_etat_emploi = 'NULL'
        
    avis_etat_emploi = clean_text(avis_etat_emploi)
    # row.append(elem.get_text(strip=True) if elem else 'NULL')

    # 6 - Ville de l'employe
    try:
        avis_ville_emploi = objet_html_2.find('span', class_='authorLocation').get_text(strip=True) # type: ignore
    except AttributeError:
        avis_ville_emploi = 'NULL'
        
    avis_ville_emploi = clean_text(avis_ville_emploi)
    # row.append(elem.get_text(strip=True) if elem else 'NULL')

    # 7 - Commentaire texte libre employe
    try:
        avis_commentaire = objet_html_2.find('p', class_='mainText mb-0').get_text(strip=True) # type: ignore
    except AttributeError:
        avis_commentaire = 'NULL'
        
    avis_commentaire = clean_text(avis_commentaire)
    # row.append(elem.get_text(strip=True) if elem else 'NULL')

    # 8 & 9 - Avantages / Inconvénients (les deux utilisent la même classe)
    elems = objet_html_2.find_all('div', class_='mt-md common__EiReviewTextStyles__allowLineBreaks')
    if len(elems) >= 1:
        texte1 = clean_text(elems[0].get_text(strip=True))
        if texte1.startswith("Avantages"):
            texte1 = texte1.replace("Avantages", "Avantages : ", 1)
    else:
        texte1 = 'NULL'

    if len(elems) >= 2:
        texte2 = clean_text(elems[1].get_text(strip=True))
        if texte2.startswith("Inconvénients"):
            texte2 = texte2.replace("Inconvénients", "Inconvénients : ", 1)
    else:
        texte2 = 'NULL'
    avantages_inconvenients = clean_text(f"{texte1} {texte2}")
    

    return(avis_note, avis_etat_emploi, avis_ville_emploi, avis_commentaire, avantages_inconvenients)


#==============================================================================
#-- LINKEDIN (EMPLOI) : Libellé de l'offre
#==============================================================================
def extraire_libelle_emploi_EMP(objet_html):
    texte_tmp = objet_html.find_all('h1', class_='topcard__title') 
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)

#==============================================================================
#-- LINKEDIN (EMPLOI) : Nom de la Société demandeuse
#==============================================================================
def extraire_nom_entreprise_EMP(objet_html):
    texte_tmp = objet_html.find_all('span', class_='topcard__flavor') 
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)


#==============================================================================
#-- LINKEDIN (EMPLOI) : Ville de l'emploi proposé
#==============================================================================
def extraire_ville_emploi_EMP (objet_html):
    texte_tmp = objet_html.find_all('span', class_='topcard__flavor topcard__flavor--bullet') 
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)


#==============================================================================
#-- LINKEDIN (EMPLOI) : Texte de l'offre d'emploi
#==============================================================================
def extraire_texte_emploi_EMP (objet_html):
    texte_tmp = objet_html.find_all('div', class_="description__text description__text--rich")
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)

#==============================================================================
#-- LINKEDIN (EMPLOI) : Type de l'emploi
#==============================================================================
def extraire_type_emploi_EMP (objet_html):
    texte_tmp = objet_html.find_all('span', class_="job-criteria__text job-criteria__text--criteria")
    if (texte_tmp == []) : 
        resultat = 'NULL'
    else:
        texte_tmp = str(texte_tmp[0].text)
        if (texte_tmp == []) : 
            resultat = 'NULL'
        else:
            resultat = texte_tmp
    return(resultat)

#==============================================================================
#-- LINKEDIN (EMPLOI) : Niveau hiérarchique, type d'emploi, 
#-- fonction et secteur d'activité
#==============================================================================
def extraire_criteres_emplois_EMP (objet_html):
    elements = objet_html.select(".job-criteria__text.job-criteria__text--criteria")
    # Assigner les 4 premiers éléments à 4 variables
    # On ajoute .get_text(strip=True) pour récupérer le texte nettoyé
    # On ajoute une vérification pour éviter les erreurs si moins de 4 éléments sont trouvés

    niveau_hierarchique = elements[0].get_text(strip=True) if len(elements) > 0 else "Pas d'informations"
    type_emploi = elements[1].get_text(strip=True) if len(elements) > 1 else "Pas d'informations"
    fonction_emploi = elements[2].get_text(strip=True) if len(elements) > 2 else "Pas d'informations"
    secteur_emploi = elements[3].get_text(strip=True) if len(elements) > 3 else "Pas d'informations"

    return(niveau_hierarchique, type_emploi, fonction_emploi, secteur_emploi)

#-- Nous allons parcourir chaque fichier dans le répertoire d'entrée, qui sont au format HTML,
#-- et on va récupérer les données importantes pour les stocker dans des fichiers CSV dans 
#-- le répertoire de sortie. Nous allons également écrire des métadonnées sur chaque opération 
#-- de traitement dans un fichier CSV de métadonnées, et y rajouter les données descriptives 
#-- retrouvées dans les fichiers HTML.
myListOfFileGlassdoorAVIS = []
myListOfFileGlassdoorSOC = []
myListOfFileLinkedInEMP = []


#-- Pour chaque sous repertoire, récupérer la liste des fichiers et les placer dans une liste 
#-- propre et dans chaque repertoire vérifier qu'il n'y ait pas d'autres repertoires et ainsi 
#-- de suite jusqu'à récupérer plusieurs listes de fichiers
trouver_fichiers_recursif(myPathLandingZoneGlassdoorAVIS, myListOfFileGlassdoorAVIS)
trouver_fichiers_recursif(myPathLandingZoneGlassdoorSOC, myListOfFileGlassdoorSOC)
trouver_fichiers_recursif(myPathLandingZoneLinkedInEMP, myListOfFileLinkedInEMP)

#-- Pour chaque fichier HTML, nous allons lire son contenu, extraire les données importantes,


# FONCTIONNE A REACTIVER QUAND BESOIN D'EXTRAIRE LES AVIS EMPLOYES GLASSDOOR
# #------------------------------------------------------------------------------
cle_incrementale_AVIS = 1
for i in myListOfFileGlassdoorAVIS:
    f = open(i, "r", encoding="utf8")
    myHTMLContents = f.read()
    f.close()
    mySoup = BeautifulSoup(myHTMLContents, 'html.parser')

    #------------------------------------------------------------------------------
    #  Exemple d'affichage des éléments contenus dans la liste créé à partir
    #  de l'extraction des avis contenus dans une même page web.
    #------------------------------------------------------------------------------

    # Informations récupérées pour la table DIM_Avis_Soc :
    # id_avis_soc
    # nom_societe
    # note_moyenne
    # avis_note
    # avis_etat_emploi
    # avis_localisation
    # avis_commentaire
    # avantages_inconvenients


    nom_societe = extraire_nom_entreprise_AVI(mySoup)
    note_moyenne = extraire_note_moy_entreprise_AVI(mySoup)

    print("AVIS SOC GLASSDOOR - nom de la société ==> " , nom_societe)
    print("AVIS SOC GLASSDOOR - note moyenne sur la société ==> " , note_moyenne)
    try:
        reviews = mySoup.find_all('li', class_='empReview')
    except Exception as e:
        print("Erreur lors de l'extraction des avis :", str(e))
        reviews = []

    print("*" * 80) 
    print("* Exemple d'extraction des plusieurs avis contenus dans une même page web")
    print("*" * 80, '\n')
    print("-" * 80)
    # liste_de_page_web = []

    cle_incrementale_AVIS_local = 1

    for rev in enumerate(reviews): #idx, rev in enumerate(reviews):
        # row = ['"{}"'.format(idx)]
        # liste_de_page_web = extraire_liste_avis_employes_sur_entreprise_AVI(mySoup)
        avis_note, avis_etat_emploi, avis_ville_emploi, avis_commentaire, avantages_inconvenients = extraire_liste_avis_employes_sur_entreprise_AVI(rev)
        print("AVIS EMPLOYE GLASSDOOR - note de l'avis employé ==> " , avis_note)
        print("AVIS EMPLOYE GLASSDOOR - état de l'emploi ==> " , avis_etat_emploi)
        print("AVIS EMPLOYE GLASSDOOR - ville de l'emploi ==> " , avis_ville_emploi)
        print("AVIS EMPLOYE GLASSDOOR - commentaire de l'employé ==> " , avis_commentaire)
        print("AVIS EMPLOYE GLASSDOOR - avantages et inconvénients ==> " , avantages_inconvenients)
        print("-" * 80)
        with open(f"{myPathCuratedZone}/METADATA_CURATED_ZONE.csv", 'a', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';')
            # ID LIGNE
            csvwriter.writerow([f"{1}_{cle_incrementale_AVIS}", "id_avis_soc", cle_incrementale_AVIS, "fichier_source", os.path.basename(i)])
            
            # Nom de la société
            csvwriter.writerow([f"{1}_{cle_incrementale_AVIS}", "nom_societe", nom_societe, "fichier_source", os.path.basename(i)])
            
            # Note moyenne sur la société
            csvwriter.writerow([f"{1}_{cle_incrementale_AVIS}", "note_moyenne", note_moyenne, "fichier_source", os.path.basename(i)])
            
            # Note donnée par un (ex) employé 
            csvwriter.writerow([f"{1}_{cle_incrementale_AVIS}", "avis_note", avis_note, "fichier_source", os.path.basename(i)])
            
            # Etat actuel de l' (ex) employé
            csvwriter.writerow([f"{1}_{cle_incrementale_AVIS}", "avis_etat_emploi", avis_etat_emploi, "fichier_source", os.path.basename(i)])
            
            # Localisation de l' (ex) employé
            csvwriter.writerow([f"{1}_{cle_incrementale_AVIS}", "avis_localisation", avis_ville_emploi, "fichier_source", os.path.basename(i)])
            
            # Commentaire de l' (ex) employé
            csvwriter.writerow([f"{1}_{cle_incrementale_AVIS}", "avis_commentaire", avis_commentaire, "fichier_source", os.path.basename(i)])
            
            # Avantages et inconvénients de l' (ex) employé
            csvwriter.writerow([f"{1}_{cle_incrementale_AVIS}", "avantages_inconvenients", avantages_inconvenients, "fichier_source", os.path.basename(i)])
        cle_incrementale_AVIS_local += 1
    print("*" * 80)  


    cle_incrementale_AVIS += 1

cle_incrementale_SOC=1
for i in myListOfFileGlassdoorSOC:
    f = open(i, "r", encoding="utf8")
    myHTMLContents = f.read()
    f.close()
    mySoup = BeautifulSoup(myHTMLContents, 'html.parser')
    # -----------------------------------------------------------------------------
    #-- RECAP control des fonctions d'extraction de données du html sur :
    #   Les avis sur les sociétés : site web GLASDOOR
    # -----------------------------------------------------------------------------
    print('='*80)
    print(i)

    ## Informations qu'il faut pour la table DIM_Soc : 
    # id_soc
    # nom_soc
    # taille_soc
    # Date_creation_soc
    # Siege_social_soc
    # type_soc
    # secteur_soc
    # Lieu_soc
    # Distinction_prix_soc
    # id_departement
    

    nom_societe = extraire_nom_entreprise_SOC(mySoup)
    ville_entreprise = extraire_ville_entreprise_SOC(mySoup)
    taille_entreprise = extraire_taille_entreprise_SOC(mySoup)
    type_entreprise = extraire_type_entreprise_SOC(mySoup)
    secteur_entreprise = extraire_secteur_entreprise_SOC(mySoup)
    siege_social_entreprise = extraire_siege_social_entreprise_SOC(mySoup)
    date_creation_entreprise = extraire_date_creation_entreprise_SOC(mySoup)

    print("INFOS SOC GLASSDOOR - nom de la société ==> " , nom_societe)
    print("INFOS SOC GLASSDOOR - ville de l'entreprise ==> " , ville_entreprise)
    print("INFOS SOC GLASSDOOR - taille de l'entreprise ==> " , taille_entreprise)
    print('='*80)

    with open(f"{myPathCuratedZone}/METADATA_CURATED_ZONE.csv", 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')

        # ID LIGNE
        csvwriter.writerow([f"{2}_{cle_incrementale_SOC}", "id_soc", cle_incrementale_SOC, "fichier_source", os.path.basename(i)])
        
        # Nom de la société
        csvwriter.writerow([f"{2}_{cle_incrementale_SOC}", "nom_societe", nom_societe, "fichier_source", os.path.basename(i)])
        
        # Taille de l'entreprise
        csvwriter.writerow([f"{2}_{cle_incrementale_SOC}", "taille_entreprise", taille_entreprise, "fichier_source", os.path.basename(i)])

        # Ville de l'entreprise 
        csvwriter.writerow([f"{2}_{cle_incrementale_SOC}", "ville_entreprise", ville_entreprise, "fichier_source", os.path.basename(i)])

        # Type de l'entreprise 
        csvwriter.writerow([f"{2}_{cle_incrementale_SOC}", "type_entreprise", type_entreprise, "fichier_source", os.path.basename(i)])

        # Secteur de l'entreprise 
        csvwriter.writerow([f"{2}_{cle_incrementale_SOC}", "secteur_entreprise", secteur_entreprise, "fichier_source", os.path.basename(i)])

        # Siege social de l'entreprise 
        csvwriter.writerow([f"{2}_{cle_incrementale_SOC}", "siege_social_entreprise", siege_social_entreprise, "fichier_source", os.path.basename(i)])

        # Date de création de l'entreprise 
        csvwriter.writerow([f"{2}_{cle_incrementale_SOC}", "date_creation_entreprise", date_creation_entreprise, "fichier_source", os.path.basename(i)])

    cle_incrementale_SOC += 1

cle_incrementale_EMP = 1
for i in myListOfFileLinkedInEMP:
    f = open(i, "r", encoding="utf8")
    myHTMLContents = f.read()
    f.close()
    mySoup = BeautifulSoup(myHTMLContents, 'html.parser')
    
    # -----------------------------------------------------------------------------
    #-- RECAP control des fonctions d'extraction de données du html sur :
    #   Les offres d'emplois proposée : site web LINKEDIN
    # -----------------------------------------------------------------------------

    ## Informations qu'il faut pour la table DIM_Emp : 
    # id_emp
    # titre_emp
    # lieu_emp
    # type_emp
    # fonction_emp
    # secteur_emp
    # experience_emp
    # formation_emp
    # missions_emp
    # technos_emp
    # soft_skills_emp
    # id_departement

    nom_societe = extraire_nom_entreprise_EMP(mySoup)
    ville_emploi = extraire_ville_emploi_EMP(mySoup)
    libelle_emploi = extraire_libelle_emploi_EMP(mySoup)

    description_emploi = extraire_texte_emploi_EMP(mySoup)
    retour_gemini = prompt_gemini_emplois_description(description_emploi)

    niveau_hierarchique, type_emploi, fonction_emploi, secteur_emploi = extraire_criteres_emplois_EMP(mySoup)


    print('=' * 80)
    print("INFO EMP LINKEDIN - nom de la société ==> ", nom_societe)
    print("INFO EMP LINKEDIN - ville de l'emploi ==> ", ville_emploi)
    print("INFO EMP LINKEDIN - libellé de l'emploi ==> ", libelle_emploi)
    print("INFO EMP LINKEDIN - niveau hiérarchique ==> ", niveau_hierarchique)
    print("INFO EMP LINKEDIN - type d'emploi ==> ", type_emploi)
    print("INFO EMP LINKEDIN - fonction ==> ", fonction_emploi)
    print("INFO EMP LINKEDIN - secteur d'activité ==> ", secteur_emploi)
    # print("INFO EMP LINKEDIN - texte descriptif de l'emploi ==> \n", description_emploi)
    print('~' * 80)
    # print("\n Utilisation de Gemini pour le traitement de texte : \n", retour_gemini)
    print("Décomposition du retour de Gemini :")
    # 1. On découpe la chaîne à chaque ";"
    # Cela crée une liste (un "array") de 6 éléments.
    champs_liste = retour_gemini.split(';')
    # 2. On assigne chaque élément de la liste à une variable
    # C'est ce qu'on appelle "l'unpacking" de liste.
    nom_entreprise_gemini = champs_liste[0]
    niveau_formation = champs_liste[1]
    niveau_experience = champs_liste[2]
    technologie_principale = champs_liste[3]
    soft_skill_principal = champs_liste[4]
    missions = champs_liste[5]
    print("Nom de l'entreprise :", nom_entreprise_gemini)
    print("Niveau de formation demandé :", niveau_formation)
    print("Niveau d'expérience demandé :", niveau_experience)
    print("Technologie principale :", technologie_principale)
    print("Soft skill principal :", soft_skill_principal)
    print("Missions :", missions)

    print('~' * 80)
    print("Ajout dans le fichier CSV")

    with open(f"{myPathCuratedZone}/METADATA_CURATED_ZONE.csv", 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')

        # ID LIGNE
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "id_emp", cle_incrementale_EMP, "fichier_source", os.path.basename(i)])

        # Titre de l'emploi
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "titre_emp", libelle_emploi, "fichier_source", os.path.basename(i)])

        # lieu de l'emploi
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "lieu_emp", ville_emploi, "fichier_source", os.path.basename(i)])

        # type de l'emploi
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "type_emp", type_emploi, "fichier_source", os.path.basename(i)])

        # Fonction de l'emploi
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "fonction_emp", fonction_emploi, "fichier_source", os.path.basename(i)])

        # Secteur de l'emploi
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "secteur_emp", secteur_emploi, "fichier_source", os.path.basename(i)])

        # Experience de l'emploi
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "experience_emp", niveau_experience, "fichier_source", os.path.basename(i)])

        # Formation de l'emploi
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "formation_emp", niveau_formation, "fichier_source", os.path.basename(i)])

        # Missions de l'emploi
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "missions_emp", missions, "fichier_source", os.path.basename(i)])

        # Technos de l'emploi
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "technos_emp", technologie_principale, "fichier_source", os.path.basename(i)])

        # Soft skills de l'emploi
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "soft_skills_emp", soft_skill_principal, "fichier_source", os.path.basename(i)])

        # Nom de la société
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "nom_societe_scrap", nom_societe, "fichier_source", os.path.basename(i)])

        # Nom de la société gemini
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "nom_societe_gemini", nom_entreprise_gemini, "fichier_source", os.path.basename(i)])

        # niveau hierarchique de la société gemini
        csvwriter.writerow([f"{3}_{cle_incrementale_EMP}", "niveau_hierarchique", niveau_hierarchique, "fichier_source", os.path.basename(i)])

    print('=' * 80)
    cle_incrementale_EMP += 1

#==============================================================================
#-- Dédoublonnage du fichier METADATA_CURATED_ZONE.csv
path_metadata_curated_zone = f"{myPathCuratedZone}/METADATA_CURATED_ZONE.csv" 
deduplicate_csv_file(path_metadata_curated_zone, csv_separator=';')
