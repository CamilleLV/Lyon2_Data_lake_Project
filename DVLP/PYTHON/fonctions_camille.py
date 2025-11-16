import os
import csv
import google.generativeai as genai
from dotenv import load_dotenv

# Cette ligne charge les variables de ton fichier .env
# (il doit se trouver dans le même dossier ou tu peux spécifier le chemin)
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

###############################################################################
#==============================================================================
#-- Création d'un fichier CSV de Métadonnées et d'une fonction pour écrire dans 
#-- ce fichier à chaque déplacement dans un répertoire.
#==============================================================================
def write_metadata_csv(csv_path, object_id, colonne, valeur):
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['OBJECT_ID', 'COLONNE', 'VALEUR'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'OBJECT_ID': object_id, 'COLONNE': colonne, 'VALEUR': valeur})



def trouver_fichiers_recursif(repertoire, liste_fichiers):
    """
    Parcourt un répertoire et ses sous-répertoires de manière récursive
    et ajoute le chemin complet de chaque fichier trouvé à une liste.
    """
    # Parcourir chaque élément (fichier ou dossier) dans le répertoire actuel
    for element in os.listdir(repertoire):
        # Construire le chemin complet de l'élément
        chemin_complet = os.path.join(repertoire, element)

        # Si l'élément est un répertoire...
        if os.path.isdir(chemin_complet):
            # print(f"Répertoire trouvé : {chemin_complet}")
            # ... on rappelle la fonction sur ce sous-répertoire
            trouver_fichiers_recursif(chemin_complet, liste_fichiers)
        # Sinon, c'est un fichier...
        else:
            # print(f"  Fichier trouvé : {chemin_complet}")
            # ... on l'ajoute à la liste
            liste_fichiers.append(chemin_complet)


###############################################################################



def prompt_gemini_emplois_description(texte_emploi: str):
    """
    Génère une description des emplois en utilisant l'API Gemini de Google.
    """

    print("Clé API Gemini utilisée :", GEMINI_API_KEY)
    genai.configure(api_key=GEMINI_API_KEY) #type: ignore

    # print('Available base models:', [m.name for m in genai.list_models()]) #type: ignore

    # Créez une instance du modèle
    print("Modèle Gemini chargé")
    model = genai.GenerativeModel("models/gemini-2.5-pro") #type: ignore

    # Posez votre question
    print("Génération de la réponse en cours...")
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

    print(response.text)


###############################################################################


if __name__ == "__main__":
    print(GEMINI_API_KEY)
    texte_emploi = """
    Issu du monde bancaire, CELAD a été créé en 1990 à Toulouse. Nos 1350 collaborateurs(trices) interviennent aujourd’hui sur 2 pôles d’activités : les systèmes d’information et l’informatique industrielle et ceci chez plus de 250 clients (PME/PMI et grands comptes).

Depuis 2006, l’entité CELAD Auvergne-Rhône-Alpes propose de nombreuses missions intéressantes et à forte valeur ajoutée sur l’ensemble de la région : Clermont-Ferrand, Montluçon, Lyon, Grenoble, St-Etienne, Valence, Dijon et Archamps.

Nous sommes entièrement impliqué(e)s dans la gestion de nos collaborateurs(trices), ce qui est la base de notre développement ainsi que le reflet de la qualité de notre travail.

Dotée d’un véritable processus de recrutement, l’agence CELAD Auvergne-Rhône-Alpes accompagne ses candidat(e)s avec beaucoup d’enthousiasme et de passion au quotidien.

Donc si vous souhaitez faire partie de l’aventure Celadienne, rejoignez-nous !

D’ailleurs, nous poursuivons notre développement et recrutons actuellement un(e) Ingénieur Expert(e) Talend pour intervenir chez un de nos clients.

Contexte : Vous interviendrez sur divers sujets liés à la gestion des EDI du Domaine Décisionnel.



Vos Principales Missions Quotidiennes

La convergence sur une plate-forme technique unique de l’ensemble des flux EDI existants.

La mise en uvre avec nos partenaires d’EDI disponibles et l’accompagnement de ce processus de bout en bout. Cet accompagnement intègre :

la communication et l’explicitation de nos spécifications sur les formats de flux et sur les modalités techniques de communication sécurisée auprès des partenaires concernés

la recette des flux produits par nos partenaires

l’accompagnement de la mise en production et de l’intégration sous la plate-forme de surveillance et de communication.

La participation potentielle à nos projets d’extension de l’offre de service EDI afin de couvrir de nouveaux besoins d’échange de données.

Environnement Technique

Expertise décisionnelle

Expertise Talend

Connaissance des métiers de l’Assurance serait un plus apprécié mais non indispensable

Formation : Bac +5 et expérience de 5 ans minimum sur un poste similaire
    """
    prompt_gemini_emplois_description(texte_emploi)


