import pytest
from pathlib import Path
import sys
sys.path.insert(0, 'src')
from src.modele import Modele, TestModele
from src.main import prediction, amélioration

CAS_IDEAL = {
    "heures_etude": {
        "ideal": (5, 8), "echelle": 8,
        "plus": "étudier davantage (visez environ (cible)h par jour)", #{cible:g}
        "moins": "étudier un peu moins (visez environ (cible)h par jour)",
    },
    "temps_telephone": {
        "ideal": (0, 2), "echelle": 10,
        "moins": "réduire votre temps sur le cellulaire (visez environ (cible)h par jour)",
    },
    "temps_reseaux_sociaux": {
        "ideal": (0, 1), "echelle": 6,
        "moins": "réduire votre temps sur les réseaux sociaux (visez environ (cible)h par jour)",
    },
    "temps_jeux": {
        "ideal": (0, 1), "echelle": 6,
        "moins": "réduire vos heures de jeux vidéo (visez environ (cible)h par jour)",
    },
    "temps_tele": {
        "ideal": (0, 1), "echelle": 6,
        "moins": "réduire votre temps devant la télé ou le streaming (visez environ (cible)h par jour)",
    },
    "sommeil": {
        "ideal": (7, 9), "echelle": 5,
        "plus": "dormir davantage (visez environ (cible)h par nuit)",
        "moins": "dormir un peu moins (visez environ (cible)h par nuit)",
    },
    "temps_exercice": {
        "ideal": (1, 2), "echelle": 2,
        "plus": "faire plus d'exercice (visez environ (cible)h par jour)",
    },
    "taux_presence": {
        "ideal": (95, 100), "echelle": 50,
        "plus": "assister à plus de cours (visez environ (cible)% de présence)",
    },
    "taux_travail": {
        "ideal": (95, 100), "echelle": 50,
        "plus": "remettre plus de travaux (visez environ (cible)% des travaux)",
    },
    "caffeine": {
        "ideal": (0, 2), "echelle": 6,
        "moins": "réduire votre consommation de café (visez environ (cible) tasse(s) par jour)",
    },
    "motivation": {
        "ideal": (8, 10), "echelle": 8,
        "plus": "travailler votre motivation (visez un niveau d'environ (cible) sur 10)",
    },}

@pytest.fixture(scope="module")
def jeu_test():
    fichier = Path(__file__).parents[1] / "donnees" / "donnees_propres.csv"
    donnees = Modele.charger_donnees(str(fichier))
    _, x_val, _, y_val, _ = Modele.separer_donnees(donnees)
    return x_val, y_val

@pytest.fixture(scope="module")
def modele():
    return TestModele.charger_modele("modele1_entrainé.joblib")

@pytest.fixture
def reponses_ideales():
    return {
        "genre": "female",
        "sante_mentale": "good",
        "education_parents": "phd",
        "internet": "good",
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

class MauvaisModele:
    def __init__(self, valeur):
        self.valeur = valeur
    def predict(self, X):
        return [self.valeur]

def test_prediction_plausibles(reponses_ideales):
    assert prediction(MauvaisModele(125.3), reponses_ideales) == 100
    assert prediction(MauvaisModele(-5), reponses_ideales) == 0


def test_profil_ideal_donne_une_note_satisfaisante(modele, reponses_ideales):
    note = prediction(modele, reponses_ideales)
    assert 0 <= note <= 100
    assert note >= 80  

def test_profil_ideal_ne_suggere_pas_d_amelioration(modele, reponses_ideales): #enlevé CAS_IDEAL
    assert amélioration(CAS_IDEAL, reponses_ideales, modele) is None