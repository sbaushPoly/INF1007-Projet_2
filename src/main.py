import pandas as pd
import os
import sys
sys.path.insert(0, 'src')
from modele import TestModele
from donnees import prediction, amélioration
import interface

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

def confirmation_reponse(reponse_recue:str, intervalle:list):
    '''
    Vérifie si la réponse écrite reçue est valide et se trouve dans l'intervalle de réponses possibles.
    Entrées:
        reponse_recue: La réponse qui a été écrite par l'utilisateur.
        intervalle: Une liste à deux éléments indiquant le début et la fin de l'intervalle inclusive de réponses possibles.
    Retourne un string avec le message d'erreur correspondant ou None s'il n'y a pas d'erreur dans la réponse recue.
    '''
    if reponse_recue == '':
        return 'Vous devez écrire une réponse.'
    if ',' in reponse_recue:
        return "Écrivez les nombres décimales avec un point plutôt qu'une virgule."
    try: 
        reponse_recue = float(reponse_recue)
    except ValueError: 
        return "La réponse doit être un nombre."
    if reponse_recue >= intervalle[0] and reponse_recue <= intervalle[1]:
        return None
    else:
        return "La réponse ne se trouve pas dans l'intervalle permise."

def conversion_langue(mot:str, langue_initiale:str)->str:
    '''
    Convertit les mots vers leur valeur indiquée en anglais tel que dans le fichier csv, ou l'inverse.
    Entrées:
        mot (str): le mot à traduire
        langue_initiale (str): Valeurs possibles de 'Français' et 'Anglais'. 
        Indique la langue à partir de laquelle le mot est traduit.
    Sortie:
        mot_traduit (str): le mot traduit
    '''
    if langue_initiale == 'Français':
        match mot: 
            case 'Homme':
                mot_traduit = 'male'
            case 'Femme':
                mot_traduit = 'female'
            case 'Faible':
                mot_traduit = 'poor' 
            case 'Moyen' | 'Moyenne':
                mot_traduit = 'average'
            case 'Bon' | 'Bonne':
                mot_traduit = 'good'
            case 'Secondaire':
                mot_traduit = 'highschool'
            case 'Baccalauréat':
                mot_traduit = 'bachelors'
            case 'Maitrise':
                mot_traduit = 'masters'
            case 'Doctorat':
                mot_traduit = 'phd'
            case _:
                raise ValueError('Entrée de choix invalide')
    elif langue_initiale == 'Anglais':
        match mot: 
            case 'male':
                mot_traduit = 'Homme'
            case 'female':
                mot_traduit = 'Femme'
            case 'poor':
                mot_traduit = 'Faible' 
            case 'average':
                mot_traduit = 'Moyen'
            case 'good':
                mot_traduit = 'Bon'
            case 'highschool':
                mot_traduit = 'Secondaire'
            case 'bachelors':
                mot_traduit = 'Baccalauréat'
            case 'masters':
                mot_traduit = 'Maitrise'
            case 'phd':
                mot_traduit = 'Doctorat'
            case _:
                raise ValueError('Entrée de choix invalide')
    else:
        return ValueError('Langue_initiale invalide')
    return mot_traduit

def conversion_liste(reponse:list)->dict:
    '''
    Convertit les réponses obtenues de interface.py dans un format utilisable par prediction
    Entrée: 
        reponse (list): tous les réponses entrées par l'utilisateur
    Sortie:
        (dict): tous les réponses associées à un nom les représantant
    '''
    return {
        "age" : reponse[0],
        "genre" : reponse[1],
        "heures_etude" : reponse[2],
        "temps_telephone" : reponse[3],
        "temps_reseaux_sociaux" : reponse[4],
        "temps_jeux" : reponse[5],
        "temps_tele" : reponse[6],
        "sommeil" : reponse[7],
        "temps_exercice" : reponse[8],
        "taux_presence" : reponse[9],
        "taux_travail" : reponse[10],
        "caffeine" : reponse[11],
        "sante_mentale" : reponse[12],
        "education_parents" : reponse[13],
        "internet" : reponse[14],
        "motivation" : reponse[15]
    }


def main():
    model = TestModele.charger_modele("modele1_entrainé.joblib")
    reponse = interface.PageQuestion.retourner_reponses()

    reponse = conversion_liste(reponse)
    note_predite = prediction(model, reponse)

    amelioration = amélioration(CAS_IDEAL, reponse, model)

    if amelioration == None:
        bilan = {
        "caracteristique": 'Aucune',
        "ecart": 0,
        "gain": 0,
        "note_actuelle": note_predite,
        "note_apres": note_predite,
        'caracteristique_affiche': 'Aucune habitude à changer',
        'message_affiche': 'Tous vos habitudes se trouvent dans les intervalles idéales. Bravo!'
        }
    else:
        message = amelioration['message']
        message = 'Vous pourriez' + message.replace('(cible)', str(amelioration['cible']))

        match amelioration['cle']:
            case "heures_etude":
                caracteristique_affiche = "Votre nombre d'heures d'étude"
            case "temps_telephone":
                caracteristique_affiche = "Votre temps passé sur votre téléphone cellulaire"
            case "temps_reseaux_sociaux":
                caracteristique_affiche = "Votre temps passé sur les réseaux sociaux"
            case "temps_jeux":
                caracteristique_affiche = "Votre temps passé à jouer à des jeux vidéos"
            case "temps_tele":
                caracteristique_affiche = "Votre temps passé sur des services de diffusion continue"
            case "sommeil":
                caracteristique_affiche = "Votre nombre d'heures de sommeil"
            case "temps_exercice":
                caracteristique_affiche = "Votre nombre d'heures d'activité physique"
            case "taux_presence":
                caracteristique_affiche = "Votre taux de présence à vos cours"
            case "taux_travail":
                caracteristique_affiche = "Votre taux de travaux complétés"
            case "caffeine":
                caracteristique_affiche = "Votre consommation de caféine"
            case "motivation":
                caracteristique_affiche = "Votre motivation envers vos études"
       
        bilan = {
            "caracteristique": amelioration["cle"],
            "ecart": amelioration["ecart"],
            "gain": amelioration["note_ameliorer"] - note_predite,
            "note_actuelle": note_predite,
            "note_apres": amelioration["note_ameliorer"],
            'caracteristique_affiche': caracteristique_affiche,
            'message_affiche': message
            }

    #print(bilan)
    return bilan
#main()