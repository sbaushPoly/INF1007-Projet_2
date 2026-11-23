import tkinter
from tkinter import ttk
from abc import ABC, abstractmethod
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import sys
sys.path.insert(0, 'src')
from donnees import charger_donnees
from main import main, conversion_langue, confirmation_reponse

def page_suivante(actuelle:tkinter.ttk.Frame, prochaine:tkinter.ttk.Frame, coordonnee:str, direction:int=1, animation:bool = True)->None:
    '''
    Cache les éléments de la page actuellement visible et fait apparaitre les éléments de la prochaine page.
    Entrées:
        actuelle (tkinter.ttk.Frame): Le frame de la page à cacher
        prochaine (tkinter.ttk.Frame): Le frame de la page à faire apparaître
        coordonnee (str): Les valeurs possibles sont 'x' et 'y'. Indiquent l'axe sur lequel le déplacement est fait.
        direction (int): valeur de 1 ou -1, indique la direction de la transition (1 pour aller vers la droite ou le haut, -1 pour aller vers la gauche ou le bas)
        animation (bool): Indique si une animation jouera lors de la transition entre les pages
    Aucune sortie
    '''

    if animation == False:
        actuelle.place_forget()
        prochaine.place(x=0, y=0, width=1600, height=900)
        return

    if direction != 1 and direction != -1:
        raise ValueError('La valeur de la direction est invalide')
    
    match coordonnee:
        case 'x':
            prochaine.place(x=1600*direction, y=0, width=1600, height=900)
            root.update_idletasks()
            animation_x([actuelle, prochaine], [-1600*direction, 0], -20*direction)
        case 'y':
                #code par IA modifié
            prochaine.place(x=0, y=900*direction, width=1600, height=900)
            root.update_idletasks()
                #code par IA
            animation_y([actuelle, prochaine], [-900*direction, 0], -20*direction)
        case _:
            raise ValueError('La coordonnée du déplacement est invalide')

    #code par IA
    actuelle.place_forget()
    #code par IA
    return

def animation_x(frames:list, position_finales:list, deplacement:int=10)->None:
    '''
    Permet de déplacer progressivement selon l'axe des x les objets Tkinter Frame vers leur position finale respective.
    Entrées:
        frames (list): liste d'objets Tkinter Frame (tkinter.ttk.Frame) à déplacer
        positions_finales (list): liste des positions finales (int) respectives à chaque élément de frames
        deplacement (int): Nombre de pixels de déplacement effectué à tous les 6 ms. Valeur par défaut de 10.
    Aucune sortie
    '''
    if frames[0].winfo_x() != position_finales[0]:
        for frame in frames:
            frame.place(x=frame.winfo_x()+deplacement, y=frame.winfo_y())
        frames[0].after(6, lambda:animation_x(frames, position_finales, deplacement))
    else:
        root.update_idletasks()

def animation_y(frames, position_finales, deplacement=10)->None:
    '''
    Permet de déplacer progressivement selon l'axe des y les objets Tkinter Frame vers leur position finale respective.
    Entrées:
        frames (list): liste d'objets Tkinter Frame (tkinter.ttk.Frame) à déplacer
        positions_finales (list): liste des positions finales (int) respectives à chaque élément de frames
        deplacement (int): Nombre de pixels de déplacement effectué à tous les 6 ms. Valeur par défaut de 10.
    Aucune sortie
    '''
    if frames[0].winfo_y() != position_finales[0]:
        for frame in frames:
            frame.place(x=frame.winfo_x(), y=frame.winfo_y()+deplacement, width=1600, height=900)
        frames[0].after(6, lambda:animation_y(frames, position_finales, deplacement))
    else:
        root.update_idletasks()

class Page(ABC):
    def __init__(self)->None:
        '''
        Initialise les éléments de base de chaque page, étant le ttk.Frame et l'arrière_plan.
        Entrée:
            self(Page): une instance de la classe Page
        Aucune sortie
        '''
        self.page = ttk.Frame(master=root)
        tkinter.Label(self.page, image=image_arriere_plan).place(x=0,y=0,relwidth=1,relheight=1)
    
    def frame_page(self)->None:
        '''
        Retourne la page sous forme de Tkinter Frame
        Entrée:
            self(Page): une instance de la classe Page
        Sortie:
            page (tkinter.ttk.Frame): Le frame de la page actuelle
        '''
        return self.page

    @abstractmethod
    def configuration_bouton(self):
        '''
        Permet de configurer les fonctions exécutées par les boutons lorsque tous leurs éléments seront définies.
        '''
        pass

class PagePrincipale(Page):
    def __init__(self)->None:
        '''
        Initialise les éléments de la page principale.
        Entrée:
            self(PagePrincipale): une instance de la classe PagePrincipale
        Aucune sortie
        '''
        super().__init__()
        self.page.place(width=1600, height=900)
        ttk.Label(master=self.page, text='Que sera votre note selon vos habitudes de vie?', font=('Ink Free', 40), background='white').place(anchor = 'n', relx=0.5, rely = 0.2)
        self.bouton1 = tkinter.Button(master=self.page, text='Commencer', font=('Ink Free', 30), bg = 'khaki1')
        self.bouton2 = tkinter.Button(master=self.page, text='À propos', font=('Ink Free', 30), bg = 'aquamarine1')
        self.bouton3 = tkinter.Button(master=self.page, text='Quitter', font=('Ink Free', 30), bg = 'light sky blue')
        self.bouton1.place(anchor = 'n', relx=0.5, rely = 0.4, relwidth=0.4, relheight=0.12)
        self.bouton2.place(anchor = 'n', relx=0.5, rely = 0.55, relwidth=0.4, relheight=0.12)
        self.bouton3.place(anchor = 'n', relx=0.5, rely = 0.7, relwidth=0.4, relheight=0.12)

    def configuration_bouton(self)->None:
        self.bouton1.configure(command=lambda: page_suivante(self.page, page_q1, 'x', 1))
            #code par IA modifié
        self.bouton2.configure(command=lambda: page_suivante(self.page, page_a_propos, 'y'))
            #code par IA modifié
        self.bouton3.configure(command= lambda: root.quit())

class PageAPropos(Page): 
    def __init__(self)->None:
        '''
        Initialise les éléments de la page à propos.
        Entrée:
            self(PageAPropos): une instance de la classe PagePrincipale
        Aucune sortie
        '''
        texte_a_propos = "Ceci est une application qui a été crée dans le cadre du projet 2 du cours INF1007. " \
        "À partir d'un ensemble de données disponible en ligne, nous avons entrainé un modèle permettant de prédire la note qu'aurait un étudiant de l'âge de 17 à 25 ans selon ses habitudes et d'autres caractéristiques de sa vie." \
        "\n\nCe modèle ayant été entrainé sur des données synthétiques, la prédiction donnée par cette application pourrait ne pas concorder avec les notes réelles obtenues." \
        "\n\nSource de l'image de l'arrière plan : College Ruled Paper par BlazingFireBug sur DeviantArt (https://www.deviantart.com/blazingfirebug/art/College-Ruled-Paper-438389060)" \
        "\n\nDéveloppé par Saya Beauchemin et Ashley Buteau"
        super().__init__()
        ttk.Label(self.page, text='À propos', font=('Ink Free', 40), background='white').place(anchor = 'n', relx=0.5, rely = 0.1)
        ttk.Label(self.page, text=texte_a_propos, font=('Ink Free', 20), background='white', wraplength=1400, justify='center').place(anchor = 'n', relx=0.5, rely = 0.3)
        self.bouton_retour = tkinter.Button(self.page, text='Retour', font=('Ink Free', 30), bg = 'aquamarine1') 
        self.bouton_retour.place(anchor = 'n', relx=0.5, rely = 0.8)

    def configuration_bouton(self)->None:
        self.bouton_retour.configure(command=lambda: page_suivante(self.page, page_principale, 'y', -1))

class PageQuestion(Page): 
    _reponses_obtenues = [] #données pour test: [19.0, 'female', 4.0, 3.0, 2.0, 0.0, 0.0, 7.0, 0.47, 100.0, 95.0, 0.0, 'poor', 'highschool', 'good', 8.0]
    
    def __init__(self, type: str, question: str, prochaine_page:ttk.Frame, options: list)->None:
        '''
        Initialise la page de la question et des variables utilisés.
        Entrées:
            self (PageQuestion): une instance de la classe PageQuestion
            type (str): valeurs possibles de 'écrit' ou 'choix', détermine le mode de réponse.
            question (str): La question qui sera affichée sur l'écran.
            prochaine_page (tkinter.ttk.Frame): La page qui suivra la page actuelle.
            options (list): Pour une question écrite, définit la valeur minimale et maximale des réponses possibles. 
                 Pour une question à choix de réponses, définit les options de réponses.
        Aucune sortie
        '''
        #Initialisation des variables
        self.type_question = type
        self.intervalle = options
        self.prochaine_page = prochaine_page
        #Initialisation des éléments de la page
        super().__init__()
        ttk.Label(self.page, text=question, font=('Ink Free', 40), background='white', wraplength=1280).place(anchor = 'n', relx=0.5, rely = 0.25)
        self.message_erreur = tkinter.Label(self.page, text='', font=('Ink Free', 20), background='white', foreground='red')
        self.texte_chargement = tkinter.Label(self.page, text='Chargement des résultats en cours...', font=('Ink Free', 20), background='white')
        #Initialisation de l'entrée de la réponse
        if type == 'ecrit':
            self.reponse = tkinter.StringVar()
            self.entree_reponse = ttk.Entry(self.page, textvariable=self.reponse, font=('Ink Free', 20)).place(anchor = 'n', relx=0.5, rely = 0.5, relwidth=0.2)
        elif type == 'choix':
            self.reponse = tkinter.StringVar()
            self.entree_reponse = ttk.Combobox(
                self.page, 
                textvariable=self.reponse, 
                values=options, 
                state="readonly",  # Empêche l'utilisateur d'écrire un texte personnalisé au clavier
                font=('Ink Free', 20)
            )
            self.entree_reponse.place(anchor = 'n', relx=0.5, rely = 0.5, relwidth=0.2)
        else:
            raise ValueError(f'Le type de question choisi est invalide')
        #Initialisation du bouton de changement de page
        self.bouton_suite = tkinter.Button(self.page, image=image_fleche, bg = 'gray80')
        self.bouton_suite.place(anchor = 'nw', height = 40, width=40, relx=0.6, rely = 0.5)

    def configuration_bouton(self)->None:
        if self.prochaine_page == page_resultats1:
            self.bouton_suite.configure(command=lambda: self.derniere_page())
        else:
            self.bouton_suite.configure(command=lambda: self.recuperer_reponse())

    def recuperer_reponse(self)->None:
        '''
        Sauvegarde la réponse et fait la transition vers la prochaine page si la réponse est valide.
        Si la réponse est invalide, affiche un message d'erreur sur l'interface.
        Entrée:
            self (PageQuestion): une instance de la classe PageQuestion
        Aucune sortie
        '''
        reponse_recue = self.reponse.get()
        if self.type_question == 'ecrit':
            if len(self.intervalle) == 2 and type(self.intervalle[0]) == int and type(self.intervalle[1]) == int:
                raison_erreur = confirmation_reponse(reponse_recue, self.intervalle)
                if raison_erreur == None:
                    reponse_recue = float(reponse_recue)
            else:
                raise ValueError('Intervalle invalide')
        else: #Si question à choix de réponse
            if reponse_recue == '': #Pour aucune réponse
                raison_erreur = 'Veuillez entrer une réponse'
            else: #Pour réponse attendue
                reponse_recue = conversion_langue(reponse_recue, 'Français')
                raison_erreur = None 
        if raison_erreur == None:#Si il n'y a pas d'erreur
            self._reponses_obtenues.append(reponse_recue)
            page_suivante(self.page, self.prochaine_page, 'x', 1)
        else:
            self.message_erreur.configure(text = raison_erreur)
            self.message_erreur.place(anchor = 'n', relx=0.5, rely = 0.43)

    def derniere_page(self)->None:
        '''
        Lorsque la dernière question a été répondue, ajoute la dernière réponse à la liste des réponses, 
        acquiert le bilan des résultats selon les réponses reçues et initialise les éléments dépendants 
        de la réponse dans la page de résultats.
        Entrée:
            self (PageQuestion): une instance de la classe PageQuestion
        Aucune sortie
        '''
        self.texte_chargement.place(anchor = 'n', relx=0.5, rely = 0.6)
        self.recuperer_reponse()

        page_resultats1_classe.bilan = main(PageQuestion._reponses_obtenues)
        page_resultats1_classe.initialisation_indicateurs()
        page_resultats1_classe.affichage_resultat.configure(text=str(round(page_resultats1_classe.bilan['note_actuelle'], 2))+'%')

    @classmethod
    def retourner_reponses(cls)->list:
        '''
        Retourne la liste des réponses obtenues.
        Entrée:
            cls : la classe PageQuestion
        Sortie:
            cls.reponses_obtenues (list): La liste des réponses de l'utilisateur dans l'ordre des questions
        '''
        return cls._reponses_obtenues

association_questions = {
    1:{'sujet':"Âge", 'colonne': 'age', 'position_y': 150, 'couleur':'aquamarine1', 'unite':'ans'},
    2:{'sujet':"Genre", 'colonne': 'gender', 'position_y': 190, 'couleur':'light pink', 'unite':''},
    3:{'sujet':"Heures d'étude", 'colonne': 'study_hours_per_day', 'position_y': 230, 'couleur':'light blue', 'unite':'h'},
    4:{'sujet':"Heures sur téléphone cellulaire", 'colonne': 'smartphone_usage_hours', 'position_y': 270, 'couleur':'khaki1', 'unite':'h'},
    5:{'sujet':"Heures sur réseaux sociaux", 'colonne': 'social_media_hours', 'position_y': 310, 'couleur':'aquamarine1', 'unite':'h'},
    6:{'sujet':"Heures sur les jeux vidéos", 'colonne': 'gaming_hours', 'position_y': 350, 'couleur':'light pink', 'unite':'h'},
    7:{'sujet':"Heures sur services de diffusion", 'colonne': 'streaming_hours', 'position_y': 390, 'couleur':'light blue', 'unite':'h'},
    8:{'sujet':"Heures de sommeil", 'colonne': 'sleep_hours', 'position_y': 430, 'couleur':'khaki1', 'unite':'h'},
    9:{'sujet':"Heures d'activité physique", 'colonne': 'exercise_hours', 'position_y': 470, 'couleur':'aquamarine1', 'unite':'h'},
    10:{'sujet':"Pourcentage de cours présents", 'colonne': 'class_attendance_percent', 'position_y': 510, 'couleur':'light pink', 'unite':'%'},
    11:{'sujet':"Pourcentage de travaux complétés", 'colonne': 'assignment_completion_percent', 'position_y': 550, 'couleur':'light blue', 'unite':'%'},
    12:{'sujet':"Tasses de café consommés", 'colonne': 'caffeine_intake_cups', 'position_y': 590, 'couleur':'khaki1', 'unite':'tasse(s)'},
    13:{'sujet':"État de santé mentale", 'colonne': 'mental_health_status', 'position_y': 630, 'couleur':'aquamarine1', 'unite':''},
    14:{'sujet':"Niveau d'éducation des parents", 'colonne': 'parent_education_level', 'position_y': 670, 'couleur':'light pink', 'unite':''},
    15:{'sujet':"Qualité de la connexion Internet", 'colonne': 'internet_quality', 'position_y': 710, 'couleur':'light blue', 'unite':''},
    16:{'sujet':"Niveau de motivation", 'colonne': 'motivation_level', 'position_y': 750, 'couleur':'khaki1', 'unite':'/10'}
}

class IndicateurPlacement:
    def __init__(self, page:ttk.Frame, index_question: int, position_bloc:str = 'bas')->None:
        '''
        Initialise les éléments de l'indicateur de placement de la réponse de l'utilisateur.
        Entrées:
            self (IndicateurPlacement): Une instance de la classe IndicateurPlacement.
            page (tkinter.ttk.Frame): La page dans laquelle l'indicateur apparait.
            index_question (int): Le numéro correspondant à la question actuelle telle que définie dans le 
                dictionnaire association_questions, d'une valeur de 1 à 15.
            position_bloc (str): Valeurs possibles de 'bas' et 'haut'. Indique où le bloc contenant l'information 
                devrait être orientée sans que son contenu soit caché par le bas de la fenêtre.
        Aucune sortie
        '''
        #Initialisation des variables
        self.index_question = index_question
        sujet = association_questions[index_question]['sujet']
        self.colonne = association_questions[index_question]['colonne']
        self.position_y = association_questions[index_question]['position_y']
        couleur = association_questions[index_question]['couleur']
        self.unite = association_questions[index_question]['unite']
        self.position_bloc = position_bloc

        #Initialisation du bloc
        self.bloc = tkinter.Frame(page, bg=couleur)
        if self.position_bloc == 'bas':
            self.bloc.place(x=1600, y=self.position_y, width=600, height=300)
        else:
            self.bloc.place(x=1600, y=self.position_y-255, width=600, height=300)
        self.entree_utilisateur = ttk.Label(self.bloc, text="Vous:", font=('Ink Free', 15), background=couleur)
        self.entree_utilisateur.place(anchor = 'nw', relx=0.02, rely = 0.0)
        self.entree_moyenne = ttk.Label(self.bloc, text="En moyenne:", font=('Ink Free', 15), background=couleur)
        self.entree_moyenne.place(anchor = 'nw', relx=0.02, rely = 0.1)
        
        #graphique
        fig = Figure(figsize=(4, 2), dpi=100)
        ax = fig.add_subplot()
        #dossier_actuel = os.path.dirname(os.path.abspath(__file__))
        chemin = os.path.join('donnees', "donnees_propres.csv")
        self.df = charger_donnees(chemin)
        ax.hist(self.df[self.colonne], bins=10)
        canvas = FigureCanvasTkAgg(fig, master=self.bloc)
        canvas.draw()
        canvas.get_tk_widget().place(relx = 0.07, rely=0.3)

        #Bouton déplacement
        self.bouton = tkinter.Button(page, width=45, text=sujet, bg = couleur, font=('Ink Free', 15), justify='left')
        self.bouton.place(x=1100, y=self.position_y)
        self.bouton.configure(command = lambda: self.animation_bloc())
        self.mouvement_vers_ext = False

    def placer_bloc(self)->None:
        '''
        Permet de placer le bloc par dessus les boutons des autres indicateurs afin que ceux-ci ne
        cachent pas l'information contenue dans le bloc.
        Entrée:
            self (IndicateurPlacement): Une instance de la classe IndicateurPlacement.
        Aucune sortie
        '''
        self.bloc.tkraise()

    def mise_a_jour_texte(self)->None:
        '''
        Ajoute la réponse de l'utilisateur et la moyenne ou la valeur la plus fréquente dans le texte affichant ces informations.
        Entrée:
            self (IndicateurPlacement): Une instance de la classe IndicateurPlacement.
        Aucune sortie
        '''
        if type(PageQuestion._reponses_obtenues[self.index_question-1]) == float:
            self.entree_utilisateur.configure(text = 'Vous:'+ str(PageQuestion._reponses_obtenues[self.index_question-1])+self.unite)
            self.entree_moyenne.configure(text = 'En moyenne:'+ str(round(self.df[self.colonne].mean(), 2))+self.unite)
        else:
            self.entree_utilisateur.configure(text = 'Vous:'+ conversion_langue(PageQuestion._reponses_obtenues[self.index_question-1], 'Anglais'))
            reponse_frequente = str(self.df.value_counts(self.colonne).idxmax())
            reponse_frequente = conversion_langue(reponse_frequente.lower(), 'Anglais')
            self.entree_moyenne.configure(text = 'Valeur plus fréquente:'+ reponse_frequente)

    def animation_bloc(self)->None:
        '''
        Gère la direction et distance de l'animation de déplacement des blocs.
        Entrée:
            self (IndicateurPlacement): Une instance de la classe IndicateurPlacement.
        Aucune sortie
        '''
        if self.mouvement_vers_ext == False:
            animation_x([self.bloc, self.bouton], [950, 950], -10)
            self.mouvement_vers_ext = True
        else:
            animation_x([self.bloc, self.bouton], [1600, 1600], 10)
            self.mouvement_vers_ext = False

class PageResultat1(Page):
    def __init__(self)->None:
        '''
        Initialise les éléments de la page 1 des résultats et les variables associées.
        Entrée:
            self (PageResultat1): Une instance de la classe PageResultat1.
        Aucune sortie
        '''
        self.liste_indicateurs = []
        self.bilan = None
        #Initialisation de l'indication du résultat
        super().__init__()
        ttk.Label(self.page, text='Résultats:', font=('Ink Free', 60), background='white').place(anchor = 'nw', relx=0.1, rely = 0.1)
        ttk.Label(self.page, text='Selon vos habitudes, il est probable que vous obteniez une note de', font=('Ink Free', 40), background='white', wraplength=700, justify='center').place(anchor = 'nw', relx=0.1, rely = 0.3)
        self.affichage_resultat = ttk.Label(self.page, text='N/A', font=('Ink Free', 60), background='white')
        self.affichage_resultat.place(anchor = 'nw', relx=0.2, rely = 0.6)
        ttk.Label(self.page, text="Comparez vos habitudes avec la moyenne!", font=('Ink Free', 25), background='white').place(anchor = 'nw', relx=0.55, rely = 0.1)
        #Initialisation du bouton de la suite
        self.bouton_suite = tkinter.Button(self.page, text='Suivant', bg = 'light pink', font=('Ink Free', 30), justify='left')
        self.bouton_suite.place(anchor = 'nw', relx=0.15, rely = 0.87, width = 400)
    
    def initialisation_indicateurs(self)->None:
        '''
        Initialise les indicateurs de placement et le résultat lorsque les réponses seront reçues.
        Entrée:
            self (PageResultat1): Une instance de la classe PageResultat1.
        Aucune sortie
        '''
        for i in range(1, len(association_questions)+1):
            if i < 8:
                self.liste_indicateurs.append(IndicateurPlacement(self.page, i))
            else:
                self.liste_indicateurs.append(IndicateurPlacement(self.page, i, 'haut'))
        for indicateur in self.liste_indicateurs:
            indicateur.placer_bloc()
            indicateur.mise_a_jour_texte()    

    def configuration_bouton(self)->None:
        self.bouton_suite.configure(command = lambda: self.vers_resultat2())

    def vers_resultat2(self)->None:
        '''
        Initialise le texte et fait la transition vers la prochaine page de résultats.
        Entrée:
            self (PageResultat1): Une instance de la classe PageResultat1.
        Aucune sortie
        '''
        page_resultats2_classe.mise_a_jour_texte()
        page_suivante(self.page, page_resultats2, 'x', 1)
      
class PageResultat2(Page):
    def __init__(self)->None:
        '''
        Initialise les éléments de la page des résultats et les variables associées.
        Entrée:
            self (PageResultat2): Une instance de la classe PageResultat2.
        Aucune sortie
        '''
        super().__init__()
        self.texte = ttk.Label(self.page, text = '', font=('Ink Free', 40), background='white', wraplength=1400)
        self.texte.place(anchor = 'n', relx=0.5, rely = 0.1)
        self.bouton_retour = tkinter.Button(self.page, text='Retour au menu principal', font=('Ink Free', 18), bg = 'aquamarine1')
        self.bouton_retour.place(anchor = 'n', relx=0.5, rely = 0.8)

        #Proposition
        self.texte_caracteristique = ttk.Label(self.page, text='Caracteristique', font=('Ink Free', 40), background='light coral', wraplength=600)
        self.texte_changement = ttk.Label(self.page, text='Changement', font=('Ink Free', 30), background='light pink', wraplength=600)
        self.texte_caracteristique.place(anchor='n', relx=0.5, rely = 0.4)
        self.texte_changement.place(anchor='n', relx=0.5, rely = 0.55)

    def mise_a_jour_texte(self)->None:
        '''
        Met à jour le texte sur cette page selon le bilan des résultats obtenus.
        Entrée:
            self (PageResultat2): Une instance de la classe PageResultat2.
        Aucune sortie
        '''
        self.texte.configure(text=f'Pour obtenir une note de {round(page_resultats1_classe.bilan['note_apres'], 2)}% (hausse de {round(page_resultats1_classe.bilan['gain'], 2)}%), une habitude que vous pourriez changer serait:')
        self.texte_caracteristique.configure(text=page_resultats1_classe.bilan['caracteristique_affiche'])
        self.texte_changement.configure(text=page_resultats1_classe.bilan['message_affiche'])

    def configuration_bouton(self)->None:
        self.bouton_retour.configure(command=lambda: self.retour_page_principale())

    def retour_page_principale(self)->None:
        '''
        Fait la transition vers la page principale et réinitialise les réponses de l'utilisateur
        Entrée:
            self (PageResultat2): Une instance de la classe PageResultat2.
        Aucune sortie
        '''
        page_suivante(self.page, page_principale, 'y', 1)
        PageQuestion._reponses_obtenues = []
        page_q16_classe.texte_chargement.place_forget()

def initialisation_interface():
    #Initialisation de l'interface utilisateur
    global root
    root = tkinter.Tk()
    root.geometry('1600x900')
    #Initialisation des images utilisés
    chemin_arriere_plan = os.path.join('assets', 'papier_background.png')
    global image_arriere_plan
    image_arriere_plan = tkinter.PhotoImage(file=chemin_arriere_plan)
    chemin_fleche = os.path.join('assets', 'fleche.png')
    global image_fleche
    image_fleche = tkinter.PhotoImage(file=chemin_fleche) 
    #Initialisation pages
    page_principale_classe = PagePrincipale()
    global page_principale
    page_principale = page_principale_classe.frame_page()
    page_a_propos_classe = PageAPropos()
    global page_a_propos
    page_a_propos = page_a_propos_classe.frame_page()
    global page_resultats1_classe
    page_resultats1_classe = PageResultat1()
    global page_resultats1
    page_resultats1 = page_resultats1_classe.frame_page()
    global page_resultats2_classe
    page_resultats2_classe = PageResultat2()
    global page_resultats2
    page_resultats2 = page_resultats2_classe.frame_page()
    #Initialisation pages question
    global page_q16_classe
    page_q16_classe = PageQuestion('ecrit', "16. Sur 10, quel est votre niveau de motivation face à vos études?", page_resultats1, [0, 10])
    page_q16 = page_q16_classe.frame_page()
    page_q15_classe = PageQuestion('choix', "15. Comment décririez-vous la qualité de votre connexion Internet?", page_q16, ['Faible', 'Moyenne', 'Bonne'])
    page_q15 = page_q15_classe.frame_page()
    page_q14_classe = PageQuestion('choix', "14. Quel est le niveau d'éducation de vos parents?", page_q15, ['Secondaire', 'Baccalauréat', 'Maitrise', 'Doctorat'])
    page_q14 = page_q14_classe.frame_page()
    page_q13_classe = PageQuestion('choix', "13. Comment décririez-vous votre état de santé mentale?", page_q14, ['Faible', 'Moyen', 'Bon'])
    page_q13 = page_q13_classe.frame_page()
    page_q12_classe = PageQuestion('ecrit', "12. Combien de tasses de café consommez-vous par jour?", page_q13, [0, 10])
    page_q12 = page_q12_classe.frame_page()
    page_q11_classe = PageQuestion('ecrit', "11. En pourcentage, quelle est la proportion des travaux scolaires que vous avez complétés?", page_q12, [0, 100])
    page_q11 = page_q11_classe.frame_page()
    page_q10_classe = PageQuestion('ecrit', "10. En pourcentage, quelle est la proportion des cours auquels vous vous êtes présentés?", page_q11, [0, 100])
    page_q10 = page_q10_classe.frame_page()
    page_q9_classe = PageQuestion('ecrit', "9. Combien d'heures par jour consacrez-vous aux activités physiques?", page_q10, [0, 24])
    page_q9 = page_q9_classe.frame_page()
    page_q8_classe = PageQuestion('ecrit', "8. Pendant combien d'heures dormez-vous chaque nuit?", page_q9, [0, 24])
    page_q8 = page_q8_classe.frame_page()
    page_q7_classe = PageQuestion('ecrit', "7. Combien d'heures passez-vous par jour à utiliser des services de diffusion en continu?", page_q8, [0, 24])
    page_q7 = page_q7_classe.frame_page()
    page_q6_classe = PageQuestion('ecrit', "6. Combien d'heures passez-vous par jour à jouer à des jeux vidéo?", page_q7, [0, 24])
    page_q6 = page_q6_classe.frame_page()
    page_q5_classe = PageQuestion('ecrit', "5. Combien d'heures passez-vous par jour sur les médias sociaux?", page_q6, [0, 24])
    page_q5 = page_q5_classe.frame_page()
    page_q4_classe = PageQuestion('ecrit', "4. Combien d'heures passez-vous par jour sur votre téléphone cellulaire?", page_q5, [0, 24])
    page_q4 = page_q4_classe.frame_page()
    page_q3_classe = PageQuestion('ecrit', "3. Combien d'heures passez-vous à étudier chaque jour?", page_q4, [0, 24])
    page_q3 = page_q3_classe.frame_page()
    page_q2_classe = PageQuestion('choix', "2. Quel est votre genre?", page_q3, ['Homme', 'Femme'])
    page_q2 = page_q2_classe.frame_page()
    page_q1_classe = PageQuestion('ecrit', "1. Quel est votre âge?", page_q2, [17, 25])
    global page_q1
    page_q1 = page_q1_classe.frame_page()

    #Configuration des boutons de transition de pages
    page_principale_classe.configuration_bouton()
    page_a_propos_classe.configuration_bouton()
    page_q1_classe.configuration_bouton()
    page_q2_classe.configuration_bouton()
    page_q3_classe.configuration_bouton()
    page_q4_classe.configuration_bouton()
    page_q5_classe.configuration_bouton()
    page_q6_classe.configuration_bouton()
    page_q7_classe.configuration_bouton()
    page_q8_classe.configuration_bouton()
    page_q9_classe.configuration_bouton()
    page_q10_classe.configuration_bouton()
    page_q11_classe.configuration_bouton()
    page_q12_classe.configuration_bouton()
    page_q13_classe.configuration_bouton()
    page_q14_classe.configuration_bouton()
    page_q15_classe.configuration_bouton()
    page_q16_classe.configuration_bouton()
    page_resultats1_classe.configuration_bouton()
    page_resultats2_classe.configuration_bouton()

    #Initialisation de l'avertissement du haut de la page
    avertissement = ttk.Label(root, text='*Cet outil est un exercice pédagogique utilisant des données synthétiques et ne devrait pas être utilisé comme aide à la décision'
                            , font=('Arial', 16), background='gray80')
    avertissement.place(relwidth=1.0)

    root.mainloop()

if __name__ == '__main__':
    initialisation_interface()