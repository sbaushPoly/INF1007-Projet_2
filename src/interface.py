import tkinter
from tkinter import ttk
from tkinter import font
from abc import ABC, abstractmethod

def page_suivante(actuelle:tkinter.ttk.Frame, prochaine:tkinter.ttk.Frame, coordonnee:str, direction:int=1, animation = True)->None:
    '''
    Cache les éléments de la page actuellement visible et fait apparaitre les éléments de la prochaine page.
    Entrées:
        actuelle: Tkinter Frame qui contient tous les éléments de la page à cacher
        prochaine: Tkinter Frame qui contient tous les éléments de la page à faire apparaître
        coordonnee: Les valeurs possibles sont 'x' et 'y'. Indiquent l'axe sur lequel le déplacement est fait.
        direction: valeur de 1 ou -1, indique la direction de la transition(1 pour aller vers la droite ou le haut, -1 pour aller vers la gauche ou le bas)
    Aucune sortie
    '''
    #(directement mettre prochaine à x=0, y=0)
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
    Permet de déplacer selon l'axe des x les objets Tkinter Frame vers leur position finale respective.
    Entrées:
        frames: liste d'objets Tkinter Frame à déplacer
        positions_finales: liste des positions finales respectives à chaque élément de frames
        deplacement: Nombre de pixels de déplacement effectué à tous les 3 ms. Valeur par défaut de 10.
    Aucune sortie
    '''
    if frames[0].winfo_x() != position_finales[0]:
        for frame in frames:
            frame.place(x=frame.winfo_x()+deplacement, y=frame.winfo_y()) #,width=1600, height=900
        frames[0].after(6, lambda:animation_x(frames, position_finales, deplacement))
    else:
        root.update_idletasks()
        return

def animation_y(frames, position_finales, deplacement=10):
    '''
    Permet de déplacer selon l'axe des y les objets Tkinter Frame vers leur position finale respective.
    Entrées:
        frames: liste d'objets Tkinter Frame à déplacer
        positions_finales: liste des positions finales respectives à chaque élément de frames
        deplacement: Nombre de pixels de déplacement effectué à tous les 3 ms. Valeur par défaut de 10.
    Aucune sortie
    '''
    if frames[1].winfo_y() != position_finales[1]:
        for frame in frames:
            frame.place(x=frame.winfo_x(), y=frame.winfo_y()+deplacement, width=1600, height=900)
        frames[0].after(6, lambda:animation_y(frames, position_finales, deplacement))
    else:
        root.update_idletasks()
        return



def confirmation_reponse(reponse_recue, intervalle):
    '''
    Vérifie si la réponse écrite reçue se trouve dans l'intervalle de réponses possibles.
    '''
    if reponse_recue == '':
        return 'Vous devez écrire une réponse.'
    try: reponse_recue = float(reponse_recue)
    except ValueError: return "La réponse doit être un nombre."
    if reponse_recue >= intervalle[0] and reponse_recue <= intervalle[1]:
        return None
    else:
        return "La réponse ne se trouve pas dans l'intervalle permise."

#Initialisation de l'interface utilisateur
root = tkinter.Tk()
root.geometry('1600x900')

#Initialisation des images utilisés
image_arriere_plan = tkinter.PhotoImage(file='assets/papier_background.png')
image_fleche = tkinter.PhotoImage(file='assets/fleche.png') 

#liste des noms des polices de texte, décommenter pour la consulter
#print(sorted(list(font.families()))) 
class Page(ABC):
    def __init__(self):
        self.page = ttk.Frame(master=root)
        tkinter.Label(self.page, image=image_arriere_plan).place(x=0,y=0,relwidth=1,relheight=1)
    
    def frame_page(self):
        '''
        Retourne la page sous forme de Tkinter Frame
        '''
        return self.page

    @abstractmethod
    def configuration_bouton(self):
        '''
        Fait la configuration du bouton permettant de soumettre sa réponse et passer à la prochaine page
        '''
        pass

class PagePrincipale(Page):
    def __init__(self):
        super().__init__()
        #self.page.place(width=1600, height=900)
        ttk.Label(master=self.page, text='Que sera votre note selon vos habitudes de vie?', font=('Ink Free', 40), background='white').place(anchor = 'n', relx=0.5, rely = 0.2)
        self.bouton1 = tkinter.Button(master=self.page, text='Commencer', font=('Ink Free', 30), bg = 'khaki1')
        self.bouton2 = tkinter.Button(master=self.page, text='À propos', font=('Ink Free', 30), bg = 'aquamarine1')
        self.bouton3 = tkinter.Button(master=self.page, text='Quitter', font=('Ink Free', 30), bg = 'light sky blue', command=root.quit)
        self.bouton1.place(anchor = 'n', relx=0.5, rely = 0.4, relwidth=0.4, relheight=0.12)
        self.bouton2.place(anchor = 'n', relx=0.5, rely = 0.55, relwidth=0.4, relheight=0.12)
        self.bouton3.place(anchor = 'n', relx=0.5, rely = 0.7, relwidth=0.4, relheight=0.12)

    def configuration_bouton(self):
        self.bouton1.configure(command=lambda: page_suivante(self.page, page_q1, 'x', 1))
            #code par IA modifié
        self.bouton2.configure(command=lambda: page_suivante(self.page, page_a_propos, 'y'))
            #code par IA modifié

class PageAPropos(Page):
    def __init__(self):
        super().__init__()
        ttk.Label(self.page, text='À propos', font=('Ink Free', 40), background='white').place(anchor = 'n', relx=0.5, rely = 0.1)
        ttk.Label(self.page, text='test', font=('Ink Free', 20), background='white', wraplength=1500).place(anchor = 'n', relx=0.5, rely = 0.3)
        self.bouton_retour = tkinter.Button(self.page, text='Retour', font=('Ink Free', 30), bg = 'aquamarine1') 
        self.bouton_retour.place(anchor = 'n', relx=0.5, rely = 0.8)

    def configuration_bouton(self):
        self.bouton_retour.configure(command=lambda: page_suivante(self.page, page_principale, 'y', -1))

class PageQuestion(Page):
    reponses_obtenues = []
    def __init__(self, type: str, question: str, prochaine_page:ttk.Frame, options: list=None):
        '''
        Initialise la page de la question et des variables.
        Entrées:
        type: 'écrit' ou 'choix', détermine le mode de réponse.
        Question: La question qui sera affichée sur l'écran.
        Options: Pour une question écrite, définit la valeur minimale et maximale des réponses possibles. 
                 Pour une question à choix de réponses, définit les options de réponses.
        '''
        #Initialisation des variables
        self.type_question = type
        self.intervalle = options
        self.prochaine_page = prochaine_page
        super().__init__()
        ttk.Label(self.page, text=question, font=('Ink Free', 40), background='white', wraplength=1280).place(anchor = 'n', relx=0.5, rely = 0.25)
        if type == 'ecrit':
            self.reponse = tkinter.StringVar()
            self.entree_reponse = ttk.Entry(self.page, textvariable=self.reponse, font=('Ink Free', 20)).place(anchor = 'n', relx=0.5, rely = 0.5, relwidth=0.2)
            self.message_erreur = tkinter.Label(self.page, text='', font=('Ink Free', 20), background='white', foreground='red')
            if options == None:
                options = [0, 24]
        elif type == 'choix':
            if options == None:
                options = [] # la liste des choix possibles est vide
            self.entree_reponse = ttk.Combobox(
                self.page, 
                textvariable=self.reponse, 
                values=options, 
                state="readonly",  # Empêche l'utilisateur d'écrire un texte personnalisé au clavier
                font=('Ink Free', 20)
            )
            self.reponse = tkinter.StringVar
            self.entree_reponse = ttk.Menubutton(self.page).place(anchor = 'n', relx=0.5, rely = 0.5, relwidth=0.2)
        else:
            raise ValueError(f'Le type de question choisi est invalide')
        self.bouton_suite = tkinter.Button(self.page, image=image_fleche, bg = 'gray80')
        self.bouton_suite.place(anchor = 'nw', height = 40, width=40, relx=0.6, rely = 0.5)

    def configuration_bouton(self):
        self.bouton_suite.configure(command=lambda: self.recuperer_reponse())

    def recuperer_reponse(self):
        '''
        Sauvegarde la réponse et fait la transition vers la prochaine page si la réponse est valide.
        Si la réponse est invalide, affiche un message d'erreur sur l'interface.
        '''
        reponse_recue = self.reponse.get()
        if self.type_question == 'ecrit':
            if len(self.intervalle) == 2 and type(self.intervalle[0]) == int and type(self.intervalle[1]) == int:
                raison_erreur = confirmation_reponse(reponse_recue, self.intervalle)
            else:
                raise ValueError("L'intervalle de réponse est invalide")
        else:
            raison_erreur = None
        if raison_erreur == None:
            self.reponses_obtenues.append(reponse_recue)
            page_suivante(self.page, self.prochaine_page, 'x', 1)
        else:
            self.message_erreur.configure(text = raison_erreur)
            self.message_erreur.place(anchor = 'n', relx=0.5, rely = 0.43)

    @classmethod
    def retourner_reponses(cls):
        return cls.reponses_obtenues

class IndicateurPlacement:
    def __init__(self, page:ttk.Frame, sujet:str, colonne:str, position_y:int, couleur:str, position_bloc = 'bas'):
        self.bloc = tkinter.Frame(page, bg=couleur)
        if position_bloc == 'bas':
            self.bloc.place(x=1600, y=position_y, width=600, height=300)
        elif position_bloc == 'haut':
            self.bloc.place(x=1600, y=position_y-240, width=600, height=300)
        self.entree_utilisateur = ttk.Label(self.bloc, text="Vous:", font=('Ink Free', 15), background=couleur).place(anchor = 'nw', relx=0.02, rely = 0.0)
        self.entree_moyenne = ttk.Label(self.bloc, text="En moyenne:", font=('Ink Free', 15), background=couleur).place(anchor = 'nw', relx=0.02, rely = 0.1)
        #graphique

        self.bouton = tkinter.Button(page, width=45, text=sujet, bg = couleur, font=('Ink Free', 20), justify='left')
        self.bouton.place(x=920, y=position_y)
        self.bouton.configure(command = lambda: self.animation_bloc())
        self.mouvement_vers_ext = False
    
    def animation_bloc(self):
        if self.mouvement_vers_ext == False:
            animation_x([self.bloc, self.bouton], [950, 950], -10)
            self.mouvement_vers_ext = True
            return
        else:
            animation_x([self.bloc, self.bouton], [1600, 1600], 10)
            self.mouvement_vers_ext = False
            return

class PageResultat1(Page):
    def __init__(self):
        super().__init__()
        ttk.Label(self.page, text='Résultats:', font=('Ink Free', 60), background='white').place(anchor = 'nw', relx=0.1, rely = 0.1)
        ttk.Label(self.page, text='Selon vos habitudes, il est probable que vous obteniez une note de', font=('Ink Free', 40), background='white', wraplength=700, justify='center').place(anchor = 'nw', relx=0.1, rely = 0.3)
        self.affichage_resultat = ttk.Label(self.page, text='N/A', font=('Ink Free', 60), background='white').place(anchor = 'nw', relx=0.25, rely = 0.6)
        ttk.Label(self.page, text="Quelle note avez-vous comme objectif d'atteindre?", font=('Ink Free', 25), background='pink').place(anchor = 'nw', relx=0.03, rely = 0.87)
        self.reponse = tkinter.StringVar()
        self.entree_reponse = ttk.Entry(self.page, textvariable=self.reponse, font=('Ink Free', 25)).place(anchor = 'nw', relx=0.48, rely = 0.87, relwidth=0.2)
        self.message_erreur = tkinter.Label(self.page, text='', font=('Ink Free', 20), background='white', foreground='red')
        self.bouton_retour = tkinter.Button(self.page, text='Retour au menu principal', font=('Ink Free', 18), bg = 'aquamarine1')
        self.bouton_retour.place(anchor = 'nw', relx=0.75, rely = 0.87)
        ttk.Label(self.page, text="Comparez vos habitudes avec la moyenne!", font=('Ink Free', 25), background='white').place(anchor = 'nw', relx=0.55, rely = 0.1)

        bloc_heures_etude = IndicateurPlacement(self.page, "Heures d'étude", 'study_hours_per_day', 150, 'light blue')

        self.page.place(width=1600, height=900)

    def configuration_bouton(self):
        self.bouton_retour.configure(command=lambda: page_suivante(self.page, page_principale, 'y', 1))

    def recuperer_reponse(self):
        reponse_recue = self.reponse.get()
        raison_erreur = confirmation_reponse(reponse_recue, [0,100])
        if raison_erreur == None:
            page_suivante(self.page, page_principale, 'x', 1) # -- Remplacer page finale --
            return reponse_recue
        else:
            self.message_erreur.configure(text = raison_erreur)
            self.message_erreur.place(anchor = 'nw', relx=0.6, rely = 0.75)

class PageResultat2(Page):
    def __init__(self):
        super().__init__()
        ttk.Label(self.page, text='Pour atteindre une note de 90.00%, vous pourriez...', font=('Ink Free', 40), background='white').place(anchor = 'n', relx=0.5, rely = 0.1)
        self.bouton_retour = tkinter.Button(self.page, text='Retour au menu principal', font=('Ink Free', 18), bg = 'aquamarine1')
        self.bouton_retour.place(anchor = 'n', relx=0.5, rely = 0.8)
        #classe pour propositions?

    def configuration_bouton(self):
        self.bouton_retour.configure(command=lambda: page_suivante(self.page, page_principale, 'x', 1))

#Page résultat 2

#Initialisation pages
page_principale_classe = PagePrincipale()
page_principale = page_principale_classe.frame_page()
page_a_propos_classe = PageAPropos()
page_a_propos = page_a_propos_classe.frame_page()
page_resultats1_classe = PageResultat1()
page_resultats1 = page_resultats1_classe.frame_page()
#Initialisation pages question
page_q2_classe = PageQuestion('ecrit', "2. Combien d'heures passez-vous par jour sur votre téléphone cellulaire?", page_principale, [0, 24])
page_q2 = page_q2_classe.frame_page()
page_q1_classe = PageQuestion('ecrit', "1. Combien d'heures passez-vous à étudier chaque jour?", page_q2, [0, 24])
page_q1 = page_q1_classe.frame_page()


#Configuration des boutons de transition de pages
page_principale_classe.configuration_bouton()
page_a_propos_classe.configuration_bouton()
page_q1_classe.configuration_bouton()
page_q2_classe.configuration_bouton()

#Initialisation de l'avertissement du haut de la page
avertissement = ttk.Label(root, text='*Cet outil est un exercice pédagogique utilisant des données synthétiques et ne devrait pas être utilisé comme aide à la décision'
                          , font=('Arial', 16), background='gray80')
avertissement.place(relwidth=1.0)

root.mainloop()