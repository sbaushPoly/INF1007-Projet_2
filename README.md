# INF1007-Projet_2

## Description du projet:
Cette application permet de prédire la note à un examen final à partir des caractéristiques et habitudes données par un utilisateur entre l'âge de 17 à 25 ans. La prédiction est faite à l'aide d'un modèle entrainé sur le jeu de données choisi. À partir des réponses, les habitudes ne se trouvant pas dans l'intervalle idéale seront délimitées et celle pour laquelle la réponse de l'utilisateur a le plus grand écart avec la limite de l'intervalle plus proche sera proposée comme changement d'habitude à faire pour atteindre cette intervalle. Une nouvelle prédiction sera faite pour montrer la note qui serait obtenue avec ce changement. Si tous les habitudes se trouvent dans les intervalles idéales, aucune amélioration sera proposée.

## Source du jeu de données
L'ensemble de données utilisée pour ce projet est la suivante:
[Digital Distraction vs Academic Performance](https://www.kaggle.com/datasets/neurocipher/digital-distraction-vs-academic-performance)
par NeuroCipher sur Kaggle
## Licence du jeu de données
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

## Commandes d'installation et de lancement
1. Installer les modules python suivants:
    - pytest
    - matplotlib (version 3.11.0)
    - pandas
    - joblib
    - scikit-learn
    - numpy (version 2.5.4)

2. Exécuter src/interface.py

## Structure de code
- github\workflows
    - tests.yml
- archive
    - student_digital_life.csv
- assets/
    - fleche.png
    - papier_background.png
- donnees/
    - donnees_propres.csv
- modeles/
    - modele1_entrainé.joblib
    - modele2_entrainé.joblib
    - modele3_entrainé.joblib
- src/
    - donnees.py
    - exeptions.py
    - interface.py
    - main.py
    - modele.py
- test/
    - test_donnees.py
    - test_modele.py
- DECISIONS.md
- JOURNAL_IA.md
- metadata.json
- questions.txt
- README.md
- requirements.txt

## Résultat du modèle
Trois modèles de régression ont été testés afin de prédire la note finale d'examen :
Modèle 1 : Linear Regression,
Modèle 2 : Ridge,
Modèle 3 : SVR.

La performance des modèles est évaluée à l'aide de la métrique RMSE (Root Mean Squared Error). Plus cette valeur est faible, plus les prédictions du modèle sont proches des valeurs réelles. Pour calculer l'erreur quadratique moyenne de référence (la baseline), le RMSE a été calculé en considérant que le modèle prédit constamment une valeur égale à la moyenne des valeurs observées.
Voici les résultats obtenus lors de l'exécution :
| **Modèle** | **RMSE baseline** | **RMSE validation** |
| ----------- | ----------- | ----------- |
| Linear Regression | 18.99 | 12.10 |
| Ridge | 18.99 | 12.10 |
| SVR | 18.99 | 16.77 |

## Analyse des résultats
Les modèles Linear Regression et Ridge obtiennent les meilleurs résultats, avec un RMSE de validation de 12.10.
Le modèle SVR obtient un RMSE de 16.77, ce qui représente une performance inférieure aux deux autres modèles.
Les trois modèles obtiennent un résultat meilleur que le baseline, dont le RMSE est de 18.99.

Ainsi, Linear Regression et Ridge sont les deux modèles les plus performants parmi ceux testés.

## Couverture de tests
| Nom du fichier | Nombre de lignes couvertes | Nombre de lignes manquées | Couverture | Lignes manquantes |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| src\donnees.py | 66 | 54 | 18% | 18-24, 36-48, 62-70, 80-82, 94-95, 108-123, 130-158 |
| src\exeptions.py | 1 | 0 | 100% | |
| src\main.py | 150 | 110 | 27% | 16-27, 39-85, 153, 262, 264, 268-273, 279-293, 302-358 |
| src\modele.py | 90 | 58 | 36% | 18-21, 34-40, 54-63, 80-81, 92, 96, 113, 117-118, 142-147, 157-215, 219 |
| test\test_donnees.py | 45 | 0 | 100% | |
| test\test_modele.py | 33 | 4 | 88% | 58-61 |
| Total | 385 | 226 | 41% | |
## Documentation consultée
Documentation tkinter : [https://docs.python.org/3/library/tkinter.html#](https://docs.python.org/3/library/tkinter.html#) 

Documentation matplotlib :[https://matplotlib.org/stable/index.html](https://matplotlib.org/stable/index.html)

Documentation Pandas : https://pandas.pydata.org/docs/

Documentation Scikit-learn : https://scikit-learn.org/stable/

Documentation Pytest : https://docs.pytest.org/en/stable/

Documentation Pathlib : https://docs.python.org/3/library/pathlib.html

## Outil du chapitre 7 utilisé
Nous avons utilisé lambda à la ligne 279 de main.py afin de choisir la proposition à faire selon celui qui a le plus grand écart. La valeur de l'écart est placé à l'index 0 du tuple regroupant les informations sur une proposition.
