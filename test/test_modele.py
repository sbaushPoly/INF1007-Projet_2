import os
import numpy as np
import pandas as np
import joblib
from modele import x_train, x_val, y_train, y_val
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import mean_squared_error

def charger_modele(fichier):
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
        modele = joblib.load(fichier)
        return modele
    except FileNotFoundError as e:
        print(f"Erreur lors du chargement du modèle : {e}")

def evaluer(modele: LinearRegression, X_val: np.ndarray, y_val: np.ndarray):
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
    y_pred = modele.predict(X_val)
    mse = mean_squared_error(y_pred, y_val)
    rmse = np.sqrt(mse)

    return {"rmse": rmse, "mse": mse}

def main():

    #Instancier et entraîner votre modèle et effectuer la validation du modèle
    modele = charger_modele("modele_entarine.joblib")

    results = evaluer(modele, x_val, y_val)

    #Modele de comparaison
    prediction_baseline = np.full(
    len(y_val), y_train.mean())
    rmse_baseline = np.sqrt(mean_squared_error(y_val,prediction_baseline))

    #Afficher les métriques
    print("RMSE baseline :", rmse_baseline)
    print(f"validation RMSE : {results['rmse']:.2f}")
    """
    # Sauvegarder les métriques dans un fichier JSON
    metadata = {
        "colonnes": list(X.columns),
        "variable_cible": "final_exam_score",
        "modele": "LinearRegression",
        "rmse": results['rmse'],
        "nb_observations": len(donnees),
    }

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    """

if __name__ == "__main__":
    main()