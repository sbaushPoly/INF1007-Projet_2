import os
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


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

def separer_donnees(donnees: pd.DataFrame):
    """
    Sépare les données en ensembles d'entraînement et de validation.

    Args:
        donnees (pd.DataFrame): Le DataFrame contenant les données à séparer.

    Returns:
        tuple: Quatre objets, x_train, x_val, y_train, y_val.
    """
    # Transforme automatiquement TOUTES les colonnes de type str / object du DataFrame
    donnees_encode = pd.get_dummies(donnees, drop_first=True, dtype=float)

    # Désigne les variables indépendants et la variable dépendant
    X = donnees_encode.drop(columns=['final_exam_score', 'student_id'])
    y = donnees_encode['final_exam_score']

    #Séparer le jeu de données en ensembles d'entraînement et de validation
    x_train, x_val, y_train, y_val = train_test_split(X, y, test_size= 0.2, train_size=0.8, random_state=0)
    
    return x_train, x_val, y_train, y_val

def entrainer_modele(x_train: np.ndarray, y_train: np.ndarray) -> LinearRegression:
    """
    Entraine un modèle de régression linéaire sur les données fournies
    
    parameters:
    ----------
    x_train : np.ndarray
        Matrice des variables explicatives pour l'entrainement
    y_train : np.ndarray
        Vecteur des valeurs cibles d'entrainement

    Returns
    ---------
    model : LinearRegression
        Modèle de régression linéaire ajusté sur les données.
    """

    modele = LinearRegression()
    modele.fit(x_train, y_train)
    return modele

def sauvegarder_modele(modele):
    """Sauvegarde le modèle entraîné dans un fichier."""
    joblib.dump(modele, "modele_entrainé.joblib")


def main():
    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin = os.path.join(dossier_actuel, "archive", "donnees_propres.csv") #modifier archive
    donnees = charger_donnees(chemin)

    x_train, x_val, y_train, y_val = separer_donnees(donnees)

    modele = entrainer_modele(x_train, y_train)

    sauvegarder_modele(modele)

    return


if __name__ == "__main__":
    main()


