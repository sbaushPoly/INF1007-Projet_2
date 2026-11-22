import pytest
import sys
sys.path.insert(0, 'src')
import donnees
from exeptions import DonneeInvalideError


def test_implementation_test_initial():
    assert donnees.implementation_test_initial() == True

# ---------- Cas usuels ----------
def test_prediction_rep_choix(reponses):
    reponses.update(genre="Homme", sante_mentale="Bonne",
                    education_parents="Doctorat", internet="Mauvaise")
    ligne = donnees.prediction(reponses)
    assert ligne["gender_Male"] == 1
    assert ligne["mental_health_status_Good"] == 1
    assert ligne["mental_health_status_Poor"] == 0
    assert ligne["parent_education_level_PhD"] == 1
    assert ligne["parent_education_level_Masters"] == 0
    assert ligne["internet_quality_Poor"] == 1


# ---------- Cas limites ----------
def test_valeurs_aux_bornes_acceptees(reponses, cle, valeur):
    reponses[cle] = valeur
    assert isinstance(donnees.prediction(reponses), float)

def test_suggestion_none_aux_bords_de_la_zone_ideale(reponses, cle, valeur):
    reponses[cle] = valeur
    assert donnees.amélioration(reponses) is None

# ---------- Cas d'erreur ----------
def test_valeurs_aux_bornes_acceptees(reponses, cle, valeur):
    reponses[cle] = valeur
    assert isinstance(donnees.prediction(reponses), float)

def test_valeur_non_numerique_leve_erreur(reponses, valeur):
    reponses["sommeil"] = valeur
    with pytest.raises(DonneeInvalideError):
        donnees.prediction(reponses)

def test_reponse_manquante_leve_erreur(reponses):
    del reponses["caffeine"]
    with pytest.raises(DonneeInvalideError, match="caffeine"):
        donnees.prediction(reponses)

def test_categorie_inconnue_leve_erreur(reponses):
    reponses["genre"] = "Martien"
    with pytest.raises(DonneeInvalideError):
        donnees.prediction(reponses)