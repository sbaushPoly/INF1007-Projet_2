import os
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.svm import SVR

class Modele:
    """
    Gérer chaque modele d'entrainement: 
    Le chargement des données, la séparation des ensembles d'entraînement et de validation, 
    l'entraînement et la sauvegarde du modèle."""

    def __init__(self, x_train: np.ndarray, x_val: np.ndarray, y_train: np.ndarray, y_val: np.ndarray):
        self.x_train = x_train
        self.x_val = x_val
        self.y_train = y_train
        self.y_val = y_val

    @staticmethod
    def charger_donnees(fichier: str) -> pd.DataFrame:
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

    @staticmethod
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

    def entrainer_modele(self, modele, x_train: np.ndarray, y_train: np.ndarray) -> LinearRegression:
        """
        Entraine un modèle de régression linéaire sur les données fournies
        
        Args:
        x_train : np.ndarray
            Matrice des variables explicatives pour l'entrainement
        y_train : np.ndarray
            Vecteur des valeurs cibles d'entrainement
        modele : Un modèle de régression linéaire (ex: LinearRegression, Ridge, SVR)

        Returns
        modele : Le modèle entraîné
        """

        modele.fit(x_train, y_train)
        return modele

    @staticmethod
    def sauvegarder_modele(modele, titre_fichier: str ):
        """
        Sauvegarde le modèle entraîné dans un fichier.
        Args:
            modele : Le modèle entraîné à sauvegarder.
            titre_fichier (str): Le nom du fichier dans lequel sauvegarder le modèle.
        """

        joblib.dump(modele, titre_fichier)


def main():
    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin = os.path.join(dossier_actuel, "archive", "donnees_propres.csv") #modifier archive
    donnees = Modele.charger_donnees(chemin)

    x_train, x_val, y_train, y_val = Modele.separer_donnees(donnees)

    modele1 = Modele.entrainer_modele(LinearRegression(), x_train, y_train)
    Modele.sauvegarder_modele(modele1, "modele1_entrainé.joblib")

    modele2 = Modele.entrainer_modele(Ridge(), x_train, y_train)
    Modele.sauvegarder_modele(modele2, "modele2_entrainé.joblib")

    modele3 = Modele.entrainer_modele(SVR(), x_train, y_train)
    Modele.sauvegarder_modele(modele3, "modele3_entrainé.joblib")

    return


if __name__ == "__main__":
    main()


