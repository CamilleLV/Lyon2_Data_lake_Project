@echo off
ECHO Lancement du script 1...
"C:/Users/camil/AppData/Local/Programs/Python/Python310/python.exe" "C:/Users/camil/Cours/Lyon 2/Données massives/Lyon2_Data_lake_Project/0_to_1_Copy_Past_Files_Into_Landing_Zone.py" && (
    ECHO Script 1 termine avec succes. Lancement du script 2...
    "C:/Users/camil/AppData/Local/Programs/Python/Python310/python.exe" "C:/Users/camil/Cours/Lyon 2/Données massives/Lyon2_Data_lake_Project/1_to_2_Landing_to_Curated_Zone.py" && (
        ECHO Script 2 termine avec succes. Lancement du script 3...
        "C:/Users/camil/AppData/Local/Programs/Python/Python310/python.exe" "C:/Users/camil/Cours/Lyon 2/Données massives/Lyon2_Data_lake_Project/2_to_3_Curated_to_Production_Zone.py" && (
            ECHO Script 3 termine avec succes. Tous les scripts sont termines.
        )
    )
)

REM Cette ligne capture le code d'erreur final (0 si tout a reussi)
exit /b %errorlevel%