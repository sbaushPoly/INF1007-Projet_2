import os
import numpy as np
import pandas as np
import joblib
import json
from modele import x_train, x_val, y_train, y_val
from sklearn.linear_model import mean_squared_error

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
    print("Test modele 1 : LinearRegression")
    modele_1 = TestModele.charger_modele("modele1_entrainé.joblib")
    results_1 = modele_1.evaluer(x_val, y_val)

    prediction_baseline = np.full(
    len(y_val), y_train.mean())
    rmse_baseline = np.sqrt(mean_squared_error(y_val,prediction_baseline)) #Modele de comparaison

    print("RMSE baseline :", rmse_baseline)
    print(f"validation RMSE : {results_1['rmse']:.2f}")


    print("Test modele 2 : Ridge")
    modele_2 = TestModele.charger_modele("modele2_entrainé.joblib")
    results_2 = modele_2.evaluer(x_val, y_val)

    prediction_baseline = np.full(
    len(y_val), y_train.mean())
    rmse_baseline = np.sqrt(mean_squared_error(y_val,prediction_baseline))
    
    print("RMSE baseline :", rmse_baseline)
    print(f"validation RMSE : {results_2['rmse']:.2f}")


    print("Test modele 3 : SVR")
    modele_3 = TestModele.charger_modele("modele3_entrainé.joblib")
    results_3 = modele_3.evaluer(x_val, y_val)

    prediction_baseline = np.full(
    len(y_val), y_train.mean())
    rmse_baseline = np.sqrt(mean_squared_error(y_val,prediction_baseline))
    
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