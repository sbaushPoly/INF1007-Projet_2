import pytest
import sys
sys.path.insert(0, 'src')
import donnees
from modele import TestModele
from exeptions import DonneeInvalideError
from main import prediction, amélioration

def test_implementation_test_initial():
    assert donnees.implementation_test_initial() == True

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

@pytest.fixture
def reponses():
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



# ---------- Cas usuels ----------
def test_prediction_rep_choix(reponses):
    reponses.update(genre="Homme", sante_mentale="Bonne",
                    education_parents="Doctorat", internet="Mauvaise")
    model = TestModele.charger_modele("modele1_entrainé.joblib")
    ligne = prediction(model, reponses) #prediction retourne seulement la note finale
    assert ligne["gender_Male"] == 1
    assert ligne["mental_health_status_Good"] == 1
    assert ligne["mental_health_status_Poor"] == 0
    assert ligne["parent_education_level_PhD"] == 1
    assert ligne["parent_education_level_Masters"] == 0
    assert ligne["internet_quality_Poor"] == 1

@pytest.mark.parametrize( #Placer juste avant le test qui l'utilise afin de ne pas causer d'erreur?
    ("cle", "valeur"),
    [
        ("age", 18),
        ("sommeil", 8),
        ("motivation", 10),
    ],
)

# ---------- Cas limites ----------
def test_valeurs_aux_bornes_acceptees(reponses, cle, valeur):
    reponses[cle] = valeur
    model = TestModele.charger_modele("modele1_entrainé.joblib")
    assert isinstance(prediction(model, reponses), float)

def test_suggestion_none_aux_bords_de_la_zone_ideale(reponses, cle, valeur):
    reponses[cle] = valeur
    model = TestModele.charger_modele("modele1_entrainé.joblib")
    assert amélioration(CAS_IDEAL, reponses, model) is None

# ---------- Cas d'erreur ----------
def test_valeurs_aux_bornes_acceptees(reponses, cle, valeur):
    reponses[cle] = valeur
    model = TestModele.charger_modele("modele1_entrainé.joblib")
    assert isinstance(prediction(model, reponses), float)

def test_valeur_non_numerique_leve_erreur(reponses, valeur):
    reponses["sommeil"] = valeur
    model = TestModele.charger_modele("modele1_entrainé.joblib")
    with pytest.raises(DonneeInvalideError):
        prediction(model, reponses)

def test_reponse_manquante_leve_erreur(reponses):
    del reponses["caffeine"]
    model = TestModele.charger_modele("modele1_entrainé.joblib")
    with pytest.raises(DonneeInvalideError, match="caffeine"):
        prediction(model, reponses)

def test_categorie_inconnue_leve_erreur(reponses):
    reponses["genre"] = "Martien"
    model = TestModele.charger_modele("modele1_entrainé.joblib")
    with pytest.raises(DonneeInvalideError):
        prediction(model, reponses)