import os
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns

def charger_donnees(fichier):
    """
    Charge les données à partir d'un fichier CSV.

    Args:
        fichier (str): Le chemin vers le fichier CSV. 

    Returns:
        pd.DataFrame: Un DataFrame contenant les données chargées.
    """
    if not os.path.exists(fichier):
        raise FileNotFoundError(f"Le fichier {fichier} n'existe pas.")
    
    try:
        donnees = pd.read_csv(fichier)
        return donnees
    except FileNotFoundError as e:
        print(f"Erreur lors du chargement des données : {e}")

dossier_actuel = os.path.dirname(os.path.abspath(__file__))
chemin = os.path.join(dossier_actuel, "archive", "student_digital_life.csv")
donnees = charger_donnees(chemin)
print(donnees.dtypes)
print(donnees.describe())
donnees.hist(figsize=(10, 8))
plt.show()

# df['x'] = pd.to_numeric(df['x'], errors='coerce') # Convertir une colonne en type numérique, en remplaçant les valeurs non convertibles par NaN
donnees = donnees.dropna()  # Supprime les lignes avec des valeurs manquantes

#Traiter les valeurs d'ages aberrantes (pas la bonne categorie de personne)
moyenne_age = donnees['age'].mean()
ecart_type_age = donnees['age'].std()
limite_basse_age = moyenne_age - 3*ecart_type_age
limite_haute_age = moyenne_age + 3*ecart_type_age
donnees = donnees[(donnees['age'] >= limite_basse_age) & (donnees['age'] <= limite_haute_age)]

#Traiter les valeurs de consommation de caféine aberrantes
moyenne_caffeine = donnees['caffeine_intake'].mean()
ecart_type_caffeine = donnees['caffeine_intake'].std()
limite_basse_caffeine = moyenne_caffeine - 3*ecart_type_caffeine
limite_haute_caffeine = moyenne_caffeine + 3*ecart_type_caffeine
donnees = donnees[(donnees['caffeine_intake'] >= limite_basse_caffeine) & (donnees['caffeine_intake'] <= limite_haute_caffeine)]

#Traiter les activites quotidiennes qui depassent une journee
habitudes_quotidiennes = ["study_hours_per_day", "smartphone_usage_hours", "social_media_hours", "gaming_hours", "streaming_hours", "sleep_hours", "exercise_hours"]
donnees["habitudes_heures"] = donnees[habitudes_quotidiennes].sum(axis=1)
donnees = donnees[donnees["habitudes_heures"] <= 24].copy()
donnees.drop(columns=["habitudes_heures"], inplace=True)

def nettoyer_string(colonne):
	donnees[colonne] = donnees[colonne].str.strip()
	donnees[colonne] = donnees[colonne].str.lower()
	return()
nettoyer_string("gender")
nettoyer_string("mental_health_status")
nettoyer_string("parent_education_level")
nettoyer_string("internet_quality")

def range_respect(colonne, minimum, maximum):
    donnees = donnees[(donnees[colonne] >= minimum) & (donnees[colonne] <= maximum)]
    return()
range_respect("class_attendance_percent", 0, 100)
range_respect("assignment_completion_percent", 0, 100)
range_respect("motivation_level", 0, 10)
range_respect("final_exam_score", 0, 100)

#donnees.to_csv('donnees_propres.csv', index=False)
#print("Nettoyage terminé. Le nouveau fichier 'donnees_propres.csv' a été créé !")
