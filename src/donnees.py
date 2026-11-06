import os
import pandas as pd
import matplotlib.pyplot as plt

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


def afficher_graphiques(donnees, colonnes, titre):
    """
    Affiche des graphiques pour l'exploration des données.

    Args:
        donnees (pd.DataFrame): Le DataFrame contenant les données à visualiser.
        colonnes (list): nom des colonnes à visualiser.
        titre (str): Le titre du graphique.
    """
    plt.figure(figsize=(10, 6))
    plt.boxplot(donnees[colonnes])
    plt.title(titre)
    plt.show()


def controle_habitudes_quotidiennes(donnees):
    """
    Vérifie que la somme des heures pour les habitudes quotidiennes ne dépasse pas 24 heures.

    Args:
        donnees (pd.DataFrame): Le DataFrame contenant les données à vérifier.

    Returns:
        pd.DataFrame: Un DataFrame filtré ne contenant que les lignes respectant la contrainte.
    """
    habitudes_quotidiennes = ["study_hours_per_day", "smartphone_usage_hours", "social_media_hours", 
                              "gaming_hours", "streaming_hours", "sleep_hours", "exercise_hours"]
    donnees["habitudes_heures"] = donnees[habitudes_quotidiennes].sum(axis=1)
    donnees_filtrees = donnees[donnees["habitudes_heures"] <= 24].copy()
    donnees_filtrees.drop(columns=["habitudes_heures"], inplace=True)
    
    print("Nombre de lignes > 24h :", (donnees["habitudes_heures"] > 24).sum())
    
    return donnees_filtrees


def nettoyer_string(colonne):
    """
    Supprime les espaces et mets le texte en minuscules.

    Args:
        colonne (str): Le nom de la colonne à nettoyer.
    """
    donnees[colonne] = donnees[colonne].str.strip()
    donnees[colonne] = donnees[colonne].str.lower()
    return()

def range_respect(colonne, minimum, maximum):
    """
    Conserve uniquement les valeurs dans la plage spécifiée pour une colonne donnée.
    
    Args:
        colonne (str): Le nom de la colonne à vérifier.
        minimum (float): La valeur minimale acceptable.
        maximum (float): La valeur maximale acceptable.
    """
    donnees = donnees[(donnees[colonne] >= minimum) & (donnees[colonne] <= maximum)]
    return()

def nettoyer_donnees(donnees):
    """
    Nettoie le DataFrame en supprimant les valeurs aberrantes et en filtrant les données.

    Args:
        donnees (pd.DataFrame): Le DataFrame à nettoyer.

    Returns:
        pd.DataFrame: Un DataFrame nettoyé.
    """
    # Supprime les lignes avec des valeurs manquantes
    donnees = donnees.dropna() 

    # Nettoyage des colonnes de type string
    colonnes_string = ["gender", "mental_health_status", "parent_education_level", "internet_quality"]
    for colonne in colonnes_string:
        nettoyer_string(colonne)

    # Nettoyage des colonnes numériques avec des plages spécifiques
    range_respect("class_attendance_percent", 0, 100)
    range_respect("assignment_completion_percent", 0, 100)
    range_respect("motivation_level", 0, 10)
    range_respect("final_exam_score", 0, 100)

    # Nettoyage pour vérifier la cohérence des habitudes quotidiennes
    donnees = controle_habitudes_quotidiennes(donnees)
    return donnees

#----------------------------
# Chargement des données
#----------------------------
dossier_actuel = os.path.dirname(os.path.abspath(__file__))
chemin = os.path.join(dossier_actuel, "archive", "student_digital_life.csv")
donnees = charger_donnees(chemin)

#----------------------------
# Exploration des données
#----------------------------
print(donnees.dtypes)
print(donnees.describe()) 
afficher_graphiques(donnees, "age", "Distribution de l'âge des étudiants")
afficher_graphiques(donnees, "caffeine_intake_cups", "Distribution de la consommation de caféine")

# Conclusion :
# Aucune valeur aberrante significative observée
# donc aucune suppression effectuée.

# ----------------------------
# Nettoyage
# ----------------------------
donnees = nettoyer_donnees(donnees)
print("Nombre de données après nettoyage :")
print(len(donnees))

# Sauvegarde
#donnees.to_csv('donnees_propres.csv', index=False)
#print("Nettoyage terminé. Le nouveau fichier 'donnees_propres.csv' a été créé !")
