import pytest
from pathlib import Path
import sys
sys.path.insert(0, 'src')
from modele import Modele, TestModele
from main import CAS_IDEAL, prediction, amélioration

@pytest.fixture(scope="module")
def jeu_test():
    fichier = Path(__file__).parents[1] / "src" / "archive" / "donnees_propres.csv"
    donnees = Modele.charger_donnees(str(fichier))
    _, x_val, _, y_val, _ = Modele.separer_donnees(donnees)
    return x_val, y_val

@pytest.fixture(scope="module")
def modele():
    return TestModele.charger_modele("modele1_entrainé.joblib")

@pytest.fixture
def reponses_ideales():
    return {
        "genre": "Femme",
        "sante_mentale": "Bonne",
        "education_parents": "Doctorat",
        "internet": "Bonne",
        "age": 20,
        "heures_etude": 6,
        "temps_telephone": 1,
        "temps_reseaux_sociaux": 0.5,
        "temps_jeux": 0.5,
        "temps_tele": 0.5,
        "sommeil": 8,
        "temps_exercice": 1.5,
        "taux_presence": 98,
        "taux_travail": 98,
        "caffeine": 1,
        "motivation": 9,
    }

def test_predictions_plausibles(modele, jeu_test):
    X, _ = jeu_test
    pred = modele.predict(X)
    assert pred.min() >= 0 and pred.max() <= 100

def test_profil_ideal_donne_une_note_satisfaisante(modele, reponses_ideales):
    note = prediction(modele, reponses_ideales)
    assert 0 <= note <= 100
    assert note >= 80  

def test_profil_ideal_ne_suggere_pas_d_amelioration(modele, CAS_IDEAL, reponses_ideales):
    assert amélioration(modele, CAS_IDEAL, reponses_ideales) is None