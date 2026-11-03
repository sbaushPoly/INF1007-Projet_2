import numpy as np
import pandas as pd
import donnees
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def train(X_train: np.ndarray, y_train: np.ndarray) -> LinearRegression:
    """
    Entraine un modèle de régression linéaire sur les données fournies
    
    parameters:
    ----------
    X_train : np.ndarray
    Matrice des variables explicatives pour l'entrainement
    y_train : np.ndarray
    Vecteur des valeurs cibles d'entrainement

    Returns
    ---------
    model : LinearRegression
    Modèle de régression linéaire ajusté sur les données.
    """

    modele = LinearRegression
    modele.fit(X_train, y_train)
    return modele

def eval(modele: LinearRegression, X_val: np.ndarray, y_val: np.ndarray):
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
        - ``r2``   : coefficient de détermination R².
    """
    y_pred = modele.predict(X_val)
    #mae = mean_absolute_error(y_val, y_pred)
    mse = mean_squared_error(y_pred, y_val)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_val, y_pred)

    return {"rmse": rmse, "mse": mse, "r2": r2}


def main():
    # Transforme automatiquement TOUTES les colonnes de type str / object du DataFrame
    donnees_encode = pd.get_dummies(donnees, drop_first=True, dtype=int)

    # Désigne les variables indépendants et la variable dépendant
    X = donnees_encode.drop(columns=['final_exam_score', 'student_id', 'age', 'gender'])
    y = donnees_encode['final_exam_score']

    #Séparer le jeu de données en ensembles d'entraînement et de validation
    x_train, x_val, y_train, y_val = train_test_split(X, y, test_size= 0.2, train_size=0.8, random_state=0)

    #Instancier et entraîner votre modèle et effectuer la validation du modèle
    modele = train(x_train, y_train)
    results = eval(modele, x_val, y_val)

    #Afficher les métriques, les coefficients et l'ordonnée à l'origine du modèle
    print(f"validation RMSE : {results['rmse']:.2f}")
    print(f"validation MSE : {results['mse']:.2f}")
    print(f"validation R² : {results['r2']:.2f}")
    print(f"Coefficients : {modele.coef_}")
    print(f"Ordonnée à l'origine : {modele.intercept_}")


if __name__ == "__main__":
    main()

