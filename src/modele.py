import os
import numpy as np
import pandas as pd
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, mean_squared_error
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

class TestModele:   
    def __init__(self, modele: object):
        self.modele = modele

    def charger_modele(self,fichier):
        """
        Charge le modèle entraîné à partir d'un fichier.

        Args:
            fichier (str): Le chemin vers le fichier du modèle.

        Returns:
            sklearn.linear_model.LinearRegression: Le modèle chargé.
        """
        if not os.path.exists(fichier):
            raise FileNotFoundError(f"Le fichier {fichier} n'existe pas.")
        try:
            self.modele = joblib.load(fichier)
            return self.modele
        except FileNotFoundError as e:
            print(f"Erreur lors du chargement du modèle : {e}")

    def evaluer(self, X_val: np.ndarray, y_val: np.ndarray):
        """
        Évalue les performances du modèle sur un ensemble de validation

        Parameters
        ----------
        model : LinearRegression
            Modèle de régression linéaire préalablement entraîné.
        X_val : np.ndarray
            Matrice des variables explicatives pour la validation
        y_val : np.ndarray
            Vecteur des valeurs cibles pour la validation
        
        Returns
        -------
        metrics : dict[str, float]
            Dictionnaire contenant les métriques, où les clés sont :

            - ``rmse`` : erreur quadratique moyenne racine.
            - ``mse``  : erreur quadratique moyenne.
        """
        y_pred = self.modele.predict(X_val)
        mse = mean_squared_error(y_pred, y_val)
        rmse = np.sqrt(mse)

        return {"rmse": rmse, "mse": mse}

def main():
    # Entrainement des modèles
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



    #Évaluation des modèles
    prediction_baseline = np.full(
    len(y_val), y_train.mean())
    rmse_baseline = np.sqrt(mean_squared_error(y_val,prediction_baseline)) #Modele de comparaison

    print("Test modele 1 : LinearRegression")
    modele_1 = TestModele.charger_modele("modele1_entrainé.joblib")
    results_1 = modele_1.evaluer(x_val, y_val)
    print("RMSE baseline :", rmse_baseline)
    print(f"validation RMSE : {results_1['rmse']:.2f}")


    print("Test modele 2 : Ridge")
    modele_2 = TestModele.charger_modele("modele2_entrainé.joblib")
    results_2 = modele_2.evaluer(x_val, y_val)
    print("RMSE baseline :", rmse_baseline)
    print(f"validation RMSE : {results_2['rmse']:.2f}")


    print("Test modele 3 : SVR")
    modele_3 = TestModele.charger_modele("modele3_entrainé.joblib")
    results_3 = modele_3.evaluer(x_val, y_val)
    print("RMSE baseline :", rmse_baseline)
    print(f"validation RMSE : {results_3['rmse']:.2f}")
    
    """
    # Sauvegarder les métriques dans un fichier JSON
    metadata = {
        "colonnes": list(X.columns),
        "variable_cible": "final_exam_score",
        "modele": "LinearRegression",
        "rmse": results_1['rmse'],
        "nb_observations": len(donnees),
    }

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    """

if __name__ == "__main__":
    main()


