# INF1007-Projet_2

## Description du projet:
Cet application permet de prédire la note finale d'examen à partir des caractéristiques et habitudes données par un utilisateur entre l'âge de 17 à 25 ans. La prédiction est faite à l'aide d'un modèle entrainé sur le jeu de données choisi.

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

## Couverture de tests
| Nom du fichier | Nombre de lignes couvertes | Nombre de lignes manquées | Couverture | Lignes manquantes |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| src\donnees.py | 66 | 54 | 18% | 18-24, 36-48, 62-70, 80-82, 94-95, 108-123, 130-158 |
| src\exeptions.py | 1 | 0 | 100% | |
| src\main.py | 147 | 111 | 24% | 15-26, 38-84, 142, 216, 237, 239, 243-248, 254-268, 277-333 |
| src\modele.py | 90 | 49 | 46% | 18-21, 35, 39-40, 80-81, 92, 96, 113, 117-118, 142-147, 157-215, 219 |
| test\test_donnees.py | 45 | 0 | 100% | |
| test\test_modele.py | 29 | 0 | 100% | |
| Total | 378 | 214 | 43% | |
## Documentation consultée
Documentation tkinter : [https://docs.python.org/3/library/tkinter.html#](https://docs.python.org/3/library/tkinter.html#)
Documentation matplotlib :[https://matplotlib.org/stable/index.html](https://matplotlib.org/stable/index.html)

## Outil du chapitre 7 utilisé
Nous avons utilisé lambda à la ligne 254 de main.py afin de choisir la proposition à faire qui a le plus grand écart.