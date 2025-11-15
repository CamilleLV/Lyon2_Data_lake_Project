# Projet : Mise en œuvre d'un Data Lakehouse dirigé par Eric Kloeckle

[cite_start]Ce projet consiste à implémenter un pipeline complet de traitement et d'ingestion de données pour construire un Data Lakehouse[cite: 1, 4]. [cite_start]Le processus couvre l'ensemble de la chaîne de traitement, de la collecte de données brutes (fichiers HTML) jusqu'à leur visualisation dans des outils de BI[cite: 5].

Le flux de traitement des données suit les étapes suivantes :
[cite_start]**Collecte → Ingestion → Extraction → Transformation → Analyse / Reporting**[cite: 9].

## 📂 Sources des données

[cite_start]Les données à la source de ce projet sont des fichiers HTML provenant des sites **LinkedIn** et **Glassdoor**[cite: 2, 11]. [cite_start]Ces fichiers, fournis dans le dossier `0_SOURCE_WEB` [cite: 22][cite_start], contiennent trois types d'informations[cite: 10]:

* [cite_start]Offres d'emploi (INFO-EMP) [cite: 10]
* [cite_start]Informations sur les entreprises (INFO-SOC) [cite: 10]
* [cite_start]Avis d'employés sur ces entreprises (AVIS-SOC) [cite: 10]

## 🏛️ Architecture du Data Lakehouse

[cite_start]L'architecture du Data Lakehouse est divisée en plusieurs zones, chacune ayant un rôle défini[cite: 68, 69]:

| Zone | Rôle | Contenu |
| :--- | :--- | :--- |
| **`00_METADATA`** | Méta-données pour chaque étape du projet, les données "curated_zone" ont été placés ici pour respecter la logique des données descriptives du projet.
| **`0_SOURCE_WEB`** | Données sources brutes | Fichiers HTML source (LinkedIn et Glassdoor) |
| **`1_LANDING_ZONE`** | Zone d'ingestion (données brutes) | Fichiers HTML copiés + Fichier CSV Métadonnées Techniques |
| **`3_PRODUCTION_ZONE`** | Zone analytique (REFINED) | Données structurées en modèle décisionnel pour la BI |

---

## ⚙️ Phases du projet

[cite_start]L'implémentation est décomposée en quatre phases principales[cite: 18]:

### [cite_start]Phase 0 : Recherche des sources de données [cite: 19]
[cite_start]Cette phase est déjà complétée[cite: 21]. [cite_start]Les données sources sont fournies dans le dossier `0_SOURCE_WEB`[cite: 22, 23]. [cite_start]Aucun travail n'est à réaliser pour cette étape[cite: 21].

### [cite_start]Phase 1 : Ingestion (vers `1_LANDING_ZONE`) [cite: 24]
* [cite_start]**Action :** Copier les fichiers HTML depuis `0_SOURCE_WEB` vers `1_LANDING_ZONE`[cite: 26].
* [cite_start]**Action :** Enregistrer simultanément les « métadonnées techniques » (date, chemins, type, etc.) dans un fichier CSV[cite: 27].
* [cite_start]**Livrables :** Scripts Python [cite: 40][cite_start], fichiers sources copiés en LANDING ZONE [cite: 41][cite_start], fichier de métadonnées techniques[cite: 42].

### [cite_start]Phase 2 : Extraction (vers `2_CURATED_ZONE`) [cite: 45]
* [cite_start]**Action :** Lire le fichier de métadonnées techniques pour localiser et traiter chaque fichier HTML présent en LANDING ZONE[cite: 46].
* [cite_start]**Action :** Extraire les « données descriptives » (nom société, ville, intitulé emploi, avis, note, etc.) contenues dans les fichiers HTML[cite: 47].
* [cite_start]**Action :** Stocker ces données extraites dans un fichier CSV de « métadonnées descriptives »[cite: 47, 51].
* [cite_start]**Livrables :** Script Python [cite: 50][cite_start], fichier de métadonnées descriptives[cite: 51].

### [cite_start]Phase 3 : ETL et Data Warehouse (vers `3_PRODUCTION_ZONE`) [cite: 53, 54]
* [cite_start]**Action :** À partir du fichier de métadonnées descriptives, utiliser un ETL (ou script Python) pour transformer, enrichir et charger les données vers la zone `3_PRODUCTION_ZONE` (REFINED ZONE)[cite: 55].
* [cite_start]**Action :** Modéliser et implémenter une structure de données décisionnelle (étoile, flocon) qui constituera le Data Warehouse[cite: 56].
* [cite_start]**Livrables :** Scripts ETL [cite: 58][cite_start], modèle de données décisionnel implémenté[cite: 59].

### [cite_start]Phase 4 : Reporting et Analyse [cite: 60]
* [cite_start]**Action :** Concevoir des tableaux de bord BI[cite: 62].
* [cite_start]**Action :** Utiliser des outils d'analyse pour explorer et afficher les données[cite: 63].
* [cite_start]**Livrables :** Rapports d'analyses et tableaux de bord BI dynamiques[cite: 66].

---

## [cite_start]💡 Bonnes pratiques [cite: 70]

* [cite_start]**Collecte non destructive :** Modification des objets sources interdite[cite: 71].
* [cite_start]**Traçabilité :** Assurée via les métadonnées techniques[cite: 71].
* [cite_start]**Évolutivité :** Utilisation d'une structure "verticale" pour les fichiers de métadonnées[cite: 72].
