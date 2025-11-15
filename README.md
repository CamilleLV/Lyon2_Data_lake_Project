# Projet : Mise en œuvre d'un Data Lakehouse dirigé par Eric Kloeckle

Ce projet consiste à implémenter un pipeline complet de traitement et d'ingestion de données pour construire un Data Lakehouse. Le processus couvre l'ensemble de la chaîne de traitement, de la collecte de données brutes (fichiers HTML) jusqu'à leur visualisation dans des outils de BI.

Le flux de traitement des données suit les étapes suivantes :
**Collecte → Ingestion → Extraction → Transformation → Analyse / Reporting**.

## 📂 Sources des données

Les données à la source de ce projet sont des fichiers HTML provenant des sites **LinkedIn** et **Glassdoor**. Ces fichiers, fournis dans le dossier `0_SOURCE_WEB`, contiennent trois types d'informations :

* Offres d'emploi (INFO-EMP)
* Informations sur les entreprises (INFO-SOC)
* Avis d'employés sur ces entreprises (AVIS-SOC)

## 🏛️ Architecture du Data Lakehouse

L'architecture du Data Lakehouse est divisée en plusieurs zones, chacune ayant un rôle défini :

| Zone | Rôle | Contenu |
| :--- | :--- | :--- |
| **`00_METADATA`** | Méta-données pour chaque étape du projet, les données "curated_zone" ont été placés ici pour respecter la logique des données descriptives du projet.
| **`0_SOURCE_WEB`** | Données sources brutes | Fichiers HTML source (LinkedIn et Glassdoor) |
| **`1_LANDING_ZONE`** | Zone d'ingestion (données brutes) | Fichiers HTML copiés + Fichier CSV Métadonnées Techniques |
| **`3_PRODUCTION_ZONE`** | Zone analytique (REFINED) | Données structurées en modèle décisionnel pour la BI |

---

## ⚙️ Phases du projet

L'implémentation est décomposée en quatre phases principales :

### Phase 0 : Recherche des sources de données
Cette phase est déjà complétée. Les données sources sont fournies dans le dossier `0_SOURCE_WEB`. Aucun travail n'est à réaliser pour cette étape.

### Phase 1 : Ingestion (vers `1_LANDING_ZONE`)
* **Action :** Copier les fichiers HTML depuis `0_SOURCE_WEB` vers `1_LANDING_ZONE`.
* **Action :** Enregistrer simultanément les « métadonnées techniques » (date, chemins, type, etc.) dans un fichier CSV.
* **Livrables :** Scripts Python, fichiers sources copiés en LANDING ZONE, fichier de métadonnées techniques.

### Phase 2 : Extraction (vers `2_CURATED_ZONE`)
* **Action :** Lire le fichier de métadonnées techniques pour localiser et traiter chaque fichier HTML présent en LANDING ZONE.
* **Action :** Extraire les « données descriptives » (nom société, ville, intitulé emploi, avis, note, etc.) contenues dans les fichiers HTML.
* **Action :** Stocker ces données extraites dans un fichier CSV de « métadonnées descriptives ».
* **Livrables :** Script Python, fichier de métadonnées descriptives.

### Phase 3 : ETL et Data Warehouse (vers `3_PRODUCTION_ZONE`)
* **Action :** À partir du fichier de métadonnées descriptives, utiliser un ETL (ou script Python) pour transformer, enrichir et charger les données vers la zone `3_PRODUCTION_ZONE` (REFINED ZONE).
* **Action :** Modéliser et implémenter une structure de données decisionnelle (étoile, flocon) qui constituera le Data Warehouse.
* **Livrables :** Scripts ETL, modèle de données décisionnel implémenté.

### Phase 4 : Reporting et Analyse
* **Action :** Concevoir des tableaux de bord BI.
* **Action :** Utiliser des outils d'analyse pour explorer et afficher les données.
* **Livrables :** Rapports d'analyses et tableaux de bord BI dynamiques.

---

## 💡 Bonnes pratiques

* **Collecte non destructive :** Modification des objets sources interdite.
* **Traçabilité :** Assurée via les métadonnées techniques.
* **Évolutivité :** Utilisation d'une structure "verticale" pour les fichiers de métadonnées.
