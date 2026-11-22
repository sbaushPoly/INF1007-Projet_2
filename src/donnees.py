import os
import pandas as pd
import matplotlib.pyplot as plt

def implementation_test_initial():
    return True

def charger_donnees(fichier: str) -> pd.DataFrame:
    """
    Charge les données à partir d'un fichier CSV.

    Args:
        fichier (str): Le chemin vers le fichier CSV. 

    Returns:
        pd.DataFrame: Un DataFrame contenant les données chargées.
    """
    if not os.path.exists(fichier):
        raise FileNotFoundError(f"Le fichier {fichier} n'existe pas.")
    try:
        donnees = pd.read_csv(fichier) 
        return donnees
    except FileNotFoundError as e:
        print(f"Erreur lors du chargement des données : {e}")


def afficher_graphiques(donnees: pd.DataFrame, colonnes: list, titre: str, type_graphique: str, sauvegarder: bool=False):
    """
    Affiche des graphiques pour l'exploration des données.

    Args:
        donnees (pd.DataFrame): Le DataFrame contenant les données à visualiser.
        colonnes (list): nom des colonnes à visualiser.
        titre (str): Le titre du graphique.
    """
    plt.figure(figsize=(10, 6))
    if type_graphique == 'boxplot':
        plt.boxplot(donnees[colonnes])
    elif type_graphique == 'hist':
        plt.hist(x=donnees[colonnes], bins=12)
    else:
        raise ValueError('Le type de graphique est invalide')
    plt.title(titre)
    if sauvegarder:
        chemin = os.path.join('graphiques', colonnes+'.png')
        plt.savefig(chemin)
    else:
        plt.show()


def controle_habitudes_quotidiennes(donnees: pd.DataFrame) -> pd.DataFrame:
    """
    Vérifie que la somme des heures pour les habitudes quotidiennes ne dépasse pas 24 heures.

    Args:
        donnees (pd.DataFrame): Le DataFrame contenant les données à vérifier.

    Returns:
        pd.DataFrame: Un DataFrame filtré ne contenant que les lignes respectant la contrainte.
    """
    # Note: "social_media_hours" est considéré comme déjà inclus dans "smartphone_usage_hours" pour éviter le double comptage.
    habitudes_quotidiennes = ["study_hours_per_day", "social_media_hours", 
                              "gaming_hours", "streaming_hours", "sleep_hours", "exercise_hours"]
    donnees["habitudes_heures"] = donnees[habitudes_quotidiennes].sum(axis=1)
    donnees_filtrees = donnees[donnees["habitudes_heures"] <= 24].copy()
    donnees_filtrees.drop(columns=["habitudes_heures"], inplace=True)
    
    print("Nombre de lignes > 24h :", (donnees["habitudes_heures"] > 24).sum())
    
    return donnees_filtrees


def nettoyer_string(colonne: str):
    """
    Supprime les espaces et mets le texte en minuscules.

    Args:
        colonne (str): Le nom de la colonne à nettoyer.
    """
    donnees[colonne] = donnees[colonne].str.strip()
    donnees[colonne] = donnees[colonne].str.lower()
    return()

def range_respect(donnees: pd.DataFrame, colonne: str, minimum: float, maximum: float):
    """
    Conserve uniquement les valeurs dans la plage spécifiée pour une colonne donnée.
    
    Args:
        donnees (pd.DataFrame): Le DataFrame à filtrer.
        colonne (str): Le nom de la colonne à vérifier.
        minimum (float): La valeur minimale acceptable.
        maximum (float): La valeur maximale acceptable.
    """
    donnees = donnees[(donnees[colonne] >= minimum) & (donnees[colonne] <= maximum)]
    return()

def nettoyer_donnees(donnees: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie le DataFrame en supprimant les valeurs aberrantes et en filtrant les données.

    Args:
        donnees (pd.DataFrame): Le DataFrame à nettoyer.

    Returns:
        pd.DataFrame: Un DataFrame nettoyé.
    """
    # Supprime les lignes avec des valeurs manquantes
    donnees = donnees.dropna() 

    # Nettoyage des colonnes de type string
    colonnes_string = ["gender", "mental_health_status", "parent_education_level", "internet_quality"]
    for colonne in colonnes_string:
        nettoyer_string(colonne)

    # Nettoyage des colonnes numériques avec des plages spécifiques
    range_respect(donnees, "class_attendance_percent", 0, 100)
    range_respect(donnees, "assignment_completion_percent", 0, 100)
    range_respect(donnees, "motivation_level", 0, 10)
    range_respect(donnees, "final_exam_score", 0, 100)

    # Nettoyage pour vérifier la cohérence des habitudes quotidiennes
    donnees = controle_habitudes_quotidiennes(donnees)
    return donnees

def prediction(model, reponse : dict) -> float:
    """
    Fait la prédiction de la note à partir des réponses données.

    Args:
        reponse (dict): Un dictionnaire avec les réponses provenant d'un utilisateur.

    Returns:
        note_predite (float): La note prédite par le modèle.
    """

    # Placer les données dans un nouveau Dictionnaire
    genre = [reponse["genre"]]
    sante = [reponse["sante_mentale"]]
    educ = [reponse["education_parents"]]
    internet = [reponse["internet"]]

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
        "gender_Male": int(genre == "male"),
        "mental_health_status_Good": int(sante == "good"),
        "mental_health_status_Poor": int(sante == "poor"),
        "parent_education_level_HighSchool": int(educ == "highschool"),
        "parent_education_level_Masters": int(educ == "masters"),
        "parent_education_level_PhD": int(educ == "phd"),
        "internet_quality_Good": int(internet == "good"),
        "internet_quality_Poor": int(internet == "poor"),
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



def amélioration(CAS_IDEAL, reponse: dict, model):
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
        message = c[sens]
        candidats.append((ecart, cle, sens, cible, message))

    if not candidats:
        return None

    # L'habitude la plus éloignée du cas idéal
    ecart, cle, sens, cible, message = max(candidats)

    # Estimation (informative) de la note si cette seule habitude atteignait la cible
    rep_modifiee = dict(reponse)
    rep_modifiee[cle] = cible
    note_ameliorer = prediction(model, rep_modifiee)
        

    return {
        "cle": cle,
        "ecart": ecart,
        "note_ameliorer": note_ameliorer,
        'message': message,
        'cible' : cible
    }

if __name__ == '__main__':
    #----------------------------
    # Chargement des données
    #----------------------------
    dossier_actuel = os.path.dirname(os.path.abspath(__file__))[:-4] #[:-4] pour enlever '.src'
    chemin = os.path.join("archive", "student_digital_life.csv")
    donnees = charger_donnees(chemin)

    #----------------------------
    # Exploration des données
    #----------------------------
    # print(donnees.dtypes)
    # print(donnees.describe()) 
    afficher_graphiques(donnees, "age", "Distribution de l'âge des étudiants", 'boxplot')
    afficher_graphiques(donnees, "caffeine_intake_cups", "Distribution de la consommation de caféine", 'boxplot')
    afficher_graphiques(donnees, 'study_hours_per_day', "Distribution du temps d'étude en heures", 'boxplot')
    afficher_graphiques(donnees, 'smartphone_usage_hours', "Distribution du temps d'utilisation du cellulaire", 'boxplot')
    afficher_graphiques(donnees, 'social_media_hours', "Distribution du temps d'utilisation de résaux sociaux", 'boxplot')
    afficher_graphiques(donnees, 'gaming_hours', "Distribution du temps consacré aux jeux vidéo", 'boxplot')
    afficher_graphiques(donnees, 'streaming_hours', "Distribution du temps consacré aux services de diffusion continu", 'boxplot')
    afficher_graphiques(donnees, 'sleep_hours', "Distribution du temps de sommeil", 'boxplot')
    afficher_graphiques(donnees, 'exercise_hours', "Distribution du temps d'acivité physique", 'boxplot')

    # Conclusion :
    # Aucune valeur aberrante significative observée
    # donc aucune suppression effectuée.

    # ----------------------------
    # Nettoyage
    # ----------------------------
    donnees = nettoyer_donnees(donnees)
    print("Nombre de données après nettoyage :")
    print(len(donnees))

    # Sauvegarde
    # donnees.to_csv('donnees_propres.csv', index=False)
    # print("Nettoyage terminé. Le nouveau fichier 'donnees_propres.csv' a été créé !")
