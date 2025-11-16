import csv
import os
from collections import defaultdict

#==============================================================================
#-- La suppression des doublons a déjà été effectuée dans le fichier
#-- 1_to_2_Landing_to_Curated_Zone.py, la copie ici "écrase" donc les fichiers
#-- précédents dans notre contexte. Normalement, nous devrions plutôt mettre
#-- à jour le fichier en ajoutant uniquement les nouvelles lignes.
#==============================================================================

# Chemin du fichier d'entrée
INPUT_FILE_PATH = r"./DATALAKE/00_METADATA/METADATA_CURATED_ZONE.csv"

# Chemin de sortie
OUTPUT_DIR = r"./DATALAKE/3_PRODUCTION_ZONE/BDD"

# Noms des fichiers de sortie
OUTPUT_FILES = {
    '1': os.path.join(OUTPUT_DIR, 'table_AVIS_SOC.csv'),
    '2': os.path.join(OUTPUT_DIR, 'table_INFO_SOC.csv'),
    '3': os.path.join(OUTPUT_DIR, 'table_EMP.csv')
}

# 'data' contiendra les données pivotées.
# La structure sera : {'1': {record_id: {col: val, ...}}, '2': ...}
data = {
    '1': defaultdict(dict),  # Pour AVIS_SOC
    '2': defaultdict(dict),  # Pour INFO_SOC
    '3': defaultdict(dict)   # Pour EMP
}

# 'headers' collectera tous les noms de colonnes uniques pour chaque table
headers = {
    '1': set(),
    '2': set(),
    '3': set()
}

print(f"Lecture et pivotement du fichier : {INPUT_FILE_PATH}...")

try:
    with open(INPUT_FILE_PATH, mode='r', encoding='utf-8') as infile:
        # Utilisation de csv.reader avec le délimiteur point-virgule
        reader = csv.reader(infile, delimiter=';')

        for i, row in enumerate(reader):
            # Ignorer les lignes vides ou mal formées
            if not row or len(row) < 5:
                print(f"Ligne {i+1} ignorée (format incorrect) : {row}")
                continue

            # Extraction des données de la ligne
            composite_key = row[0]
            attribute_name = row[1]
            attribute_value = row[2]
            source_file = row[4]  # Le nom du fichier source

            try:
                # Séparation de la clé : "1_1" -> table_type="1", record_id="1"
                table_type, record_id = composite_key.split('_', 1)
            except ValueError:
                print(f"Ligne {i+1} ignorée (clé composite invalide) : {composite_key}")
                continue

            # Vérifier si le type de table est celui que nous gérons
            if table_type in data:
                # C'est ici que le "pivot" se produit :
                # On assigne la valeur à la bonne colonne (attribute_name)
                # pour le bon enregistrement (record_id) de la bonne table (table_type)
                data[table_type][record_id][attribute_name] = attribute_value
                
                # On ajoute aussi le fichier source comme une colonne
                data[table_type][record_id]['fichier_source'] = source_file

                # On collecte les noms des colonnes pour les en-têtes
                headers[table_type].add(attribute_name)
                headers[table_type].add('fichier_source')
            else:
                print(f"Ligne {i+1} ignorée (type de table inconnu) : {table_type}")

except FileNotFoundError:
    print(f"ERREUR : Le fichier d'entrée n'a pas été trouvé.")
    print(f"Vérifiez le chemin : {INPUT_FILE_PATH}")
    exit()
except Exception as e:
    print(f"Une erreur est survenue lors de la lecture du fichier : {e}")
    exit()

print("Lecture et pivotement terminés.")
print("Écriture des fichiers de sortie...")

for table_type, output_filename in OUTPUT_FILES.items():
    
    table_data = data[table_type]
    
    # Si aucune donnée n'a été trouvée pour ce type, on ne crée pas de fichier
    if not table_data:
        print(f"Aucune donnée trouvée pour le type {table_type}. Fichier '{output_filename}' non créé.")
        continue

    # On convertit le set d'en-têtes en une liste triée pour un ordre stable
    fieldnames = sorted(list(headers[table_type]))

    print(f"-> Écriture de {output_filename} ({len(table_data)} lignes)")

    try:
        with open(output_filename, mode='w', encoding='utf-8', newline='') as outfile:
            # csv.DictWriter permet d'écrire les dictionnaires au format CSV
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            
            # Écriture de la ligne d'en-tête
            writer.writeheader()
            
            # Écriture de toutes les lignes de données pour cette table
            # On trie par record_id pour un fichier de sortie ordonné
            for record_id in sorted(table_data.keys()):
                writer.writerow(table_data[record_id])

    except Exception as e:
        print(f"ERREUR lors de l'écriture du fichier {output_filename} : {e}")

print("Traitement terminé !")