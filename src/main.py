import pandas as pd
from modele import TestModele

CAS_IDEAL = {
    "heures_etude": {
        "ideal": (5, 8), "echelle": 8,
        "plus": "étudier davantage (visez environ {cible:g} h par jour)",
        "moins": "étudier un peu moins (visez environ {cible:g} h par jour)",
    },
    "temps_telephone": {
        "ideal": (0, 2), "echelle": 10,
        "moins": "réduire votre temps sur le cellulaire (visez environ {cible:g} h par jour)",
    },
    "temps_reseaux_sociaux": {
        "ideal": (0, 1), "echelle": 6,
        "moins": "réduire votre temps sur les réseaux sociaux (visez environ {cible:g} h par jour)",
    },
    "temps_jeux": {
        "ideal": (0, 1), "echelle": 6,
        "moins": "réduire vos heures de jeux vidéo (visez environ {cible:g} h par jour)",
    },
    "temps_tele": {
        "ideal": (0, 1), "echelle": 6,
        "moins": "réduire votre temps devant la télé ou le streaming (visez environ {cible:g} h par jour)",
    },
    "sommeil": {
        "ideal": (7, 9), "echelle": 5,
        "plus": "dormir davantage (visez environ {cible:g} h par nuit)",
        "moins": "dormir un peu moins (visez environ {cible:g} h par nuit)",
    },
    "temps_exercice": {
        "ideal": (1, 2), "echelle": 2,
        "plus": "faire plus d'exercice (visez environ {cible:g} h par jour)",
    },
    "taux_presence": {
        "ideal": (95, 100), "echelle": 50,
        "plus": "assister à plus de cours (visez environ {cible:g} % de présence)",
    },
    "taux_travail": {
        "ideal": (95, 100), "echelle": 50,
        "plus": "remettre plus de travaux (visez environ {cible:g} % des travaux)",
    },
    "caffeine": {
        "ideal": (0, 2), "echelle": 6,
        "moins": "réduire votre consommation de café (visez environ {cible:g} tasse(s) par jour)",
    },
    "motivation": {
        "ideal": (8, 10), "echelle": 8,
        "plus": "travailler votre motivation (visez un niveau d'environ {cible:g} sur 10)",
    },}



def prediction(model, reponse : dict) -> float:
    """
    Fait la prédiction de la note à partir des réponses données.

    Args:
        reponse (dict): Un dictionnaire avec les réponses provenant d'un utilisateur.

    Returns:
        note_predite (float): La note prédite par le modèle.
    """
    # Options pour questions aux choix
    GENRES = {"Femme": "Female", "Homme": "Male"}
    SANTE_MENTALE = {"Moyenne": "Average", "Bonne": "Good", "Mauvaise": "Poor"}
    EDUCATION_PARENTS = {"Baccalauréat": "Bachelors", "Secondaire": "HighSchool",
                     "Maîtrise": "Masters", "Doctorat": "PhD"}
    QUALITE_INTERNET = {"Moyenne": "Average", "Bonne": "Good", "Mauvaise": "Poor"}

    # Placer les données dans un nouveau Dictionnaire
    genre = GENRES[reponse["genre"]]
    sante = SANTE_MENTALE[reponse["sante_mentale"]]
    educ = EDUCATION_PARENTS[reponse["education_parents"]]
    internet = QUALITE_INTERNET[reponse["internet"]]

    donnees_utilisateur = {
        "age": reponse["age"],
        "study_hours_per_day": reponse["heures_etude"],
        "smartphone_usage_hours": reponse["temps_telephone"],
        "social_media_hours": reponse["temps_reseaux_sociaux"],
        "gaming_hours": reponse["temps_jeux"],
        "streaming_hours": reponse["temps_tele"],
        "sleep_hours": reponse["sommeil"],
        "exercise_hours": reponse["temps_exercice"],
        "class_attendance_percent": reponse["taux_presence"],
        "assignment_completion_percent": reponse["taux_travail"],
        "caffeine_intake_cups": reponse["caffeine"],
        "motivation_level": reponse["motivation"],
        # 1 si la catégorie correspond, 0 sinon
        "gender_Male": int(genre == "Male"),
        "mental_health_status_Good": int(sante == "Good"),
        "mental_health_status_Poor": int(sante == "Poor"),
        "parent_education_level_HighSchool": int(educ == "HighSchool"),
        "parent_education_level_Masters": int(educ == "Masters"),
        "parent_education_level_PhD": int(educ == "PhD"),
        "internet_quality_Good": int(internet == "Good"),
        "internet_quality_Poor": int(internet == "Poor"),
    }

    df = pd.DataFrame([donnees_utilisateur])

    #verification des noms des colonnes et realignement
    colonnes = getattr(model, "feature_names_in_", None)
    if colonnes is not None:
        df = df.reindex(columns=colonnes, fill_value=0)

    # 3. Faire la prédiction
    prediction = model.predict(df)

    # 4. Afficher le résultat
    # prediction est un tableau (ex: [85.4]), on prend le premier élément avec [0]
    note_predite = float(prediction[0])
    print(f"La note prédite pour cet étudiant est de : {note_predite:.2f}")
    return note_predite



def amélioration(model, CAS_IDEAL, reponse: dict):
    """
    Compare les réponses de l'utilisateur au cas idéal et suggère d'améliorer
    l'habitude dont l'écart (normalisé) est le plus grand.

    Retourne un dictionnaire :
        {"cle", "message", "ecart", "gain", "note_actuelle", "note_apres"}
    ou None si l'utilisateur est déjà dans la zone idéale partout.
    """
    candidats = []   # (écart normalisé, clé, sens, valeur cible)

    for cle, c in CAS_IDEAL.items():
        ideal_min, ideal_max = c["ideal"]
        valeur = reponse[cle]

        if valeur < ideal_min:
            sens, cible = "plus", ideal_min
        elif valeur > ideal_max:
            sens, cible = "moins", ideal_max
        else:
            continue            # déjà dans la zone idéale

        if sens not in c:       # ce sens n'est jamais suggéré pour cette variable
            continue

        ecart = abs(valeur - cible) / c["echelle"]
        candidats.append((ecart, cle, sens, cible))

    if not candidats:
        return None

    # L'habitude la plus éloignée du cas idéal
    ecart, cle, sens, cible = max(candidats)

    # Estimation (informative) de la note si cette seule habitude atteignait la cible
    rep_modifiee = dict(reponse)
    rep_modifiee[cle] = cible
    note_ameliorer = prediction(model, rep_modifiee)
        

    return {
        "cle": cle,
        "ecart": ecart,
        "note_ameliorer": note_ameliorer,
    }



def main():
    model = TestModele.charger_modele("modele1_entrainé.joblib")
    reponse = None            #faire le lien avec l'interface

    note_predite = prediction(model, reponse)

    amelioration = amélioration(model, CAS_IDEAL, reponse)

    bilan = {
        "caracteristique": amelioration["cle"],
        "ecart": amelioration["ecart"],
        "gain": amelioration["note_ameliorer"] - note_predite,
        "note_actuelle": note_predite,
        "note_apres": amelioration["note_ameliorer"]
        }

    # print()