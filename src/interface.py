import tkinter
from tkinter import ttk
from tkinter import font

def page_suivante(actuelle, prochaine, coordonnee, direction=1):
    '''
    Cache les éléments de la page actuellement visible et fait apparaitre les éléments de la prochaine page.
    Entrées:
        actuelle: ttk.Frame() qui contient tous les éléments de la page à cacher
        prochaine: ttk.Frame() qui contient tous les éléments de la page à faire apparaître
        coordonnee: valeurs possibles de 'x' et 'y'. Indiquent l'axe sur lequel le déplacement est fait.
        direction: valeur de 1 ou -1, indique la direction de la transition(1 pour aller vers la droite ou le haut, -1 pour aller vers la gauche ou le bas)
    Aucune sortie
    '''
    match coordonnee:
        case 'x':
            prochaine.place(x=1600*direction, y=0, width=1600, height=900)
            root.update_idletasks()
            animation_x([actuelle, prochaine], [-1600*direction, 0], -10)
        case 'y':
            #code par IA modifié
            prochaine.place(x=0, y=900*direction, width=1600, height=900)
            root.update_idletasks()
            #code par IA
            animation_y([actuelle, prochaine], [-900*direction, 0], -10*direction)

    #code par IA
    actuelle.place_forget()
    #code par IA
    return

def animation_x(frames, position_finales, deplacement=10):
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
            frame.place(x=frame.winfo_x()+deplacement, y=frame.winfo_y(), width=1600, height=900)
        #frames[1].place(x=frames[1].winfo_x()+deplacement, y=frames[1].winfo_y(), width=1600, height=900)
        frames[0].after(3, lambda:animation_x(frames, position_finales, deplacement))
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
        #frames[1].place(x=frames[1].winfo_x(), y=frames[1].winfo_y()+deplacement, width=1600, height=900)
        frames[0].after(3, lambda:animation_y(frames, position_finales, deplacement))
    else:
        root.update_idletasks()
        return
                    

#Initialisation de l'interface utilisateur
root = tkinter.Tk()
root.geometry('1600x900')

image_arriere_plan = tkinter.PhotoImage(file='assets/papier_background.png')
image_fleche = tkinter.PhotoImage(file='assets/fleche.png') 

#print(sorted(list(font.families()))) #noms des polices de texte

#page principale
page_principale = ttk.Frame(master=root)
arriere_plan_1 = tkinter.Label(page_principale, image=image_arriere_plan)
titre_p1 = ttk.Label(master=page_principale, text='Que sera votre note selon vos habitudes de vie?', font=('Ink Free', 40), background='white')
bouton1 = tkinter.Button(master=page_principale, text='Commencer', font=('Ink Free', 30), bg = 'khaki1')
bouton2 = tkinter.Button(master=page_principale, text='À propos', font=('Ink Free', 30), bg = 'aquamarine1')
bouton3 = tkinter.Button(master=page_principale, text='Quitter', font=('Ink Free', 30), bg = 'light sky blue', command=root.quit)

#Faire apparaitre la page principale
page_principale.place(width=1600, height=900)
arriere_plan_1.place(x=0,y=0, relwidth=1, relheight=1)
titre_p1.place(anchor = 'n', relx=0.5, rely = 0.2)
bouton1.place(anchor = 'n', relx=0.5, rely = 0.4, relwidth=0.4, relheight=0.12)
bouton2.place(anchor = 'n', relx=0.5, rely = 0.55, relwidth=0.4, relheight=0.12)
bouton3.place(anchor = 'n', relx=0.5, rely = 0.7, relwidth=0.4, relheight=0.12)

#page à propos
page_a_propos = ttk.Frame(master=root)
#image_arriere_plan = tkinter.PhotoImage(file='assets/papier_background.png')
arriere_plan_2 = tkinter.Label(page_a_propos, image=image_arriere_plan).place(x=0,y=0,relwidth=1,relheight=1)
titre = ttk.Label(page_a_propos, text='À propos', font=('Ink Free', 40), background='white').place(anchor = 'n', relx=0.5, rely = 0.1)
description = ttk.Label(page_a_propos, text='test', font=('Ink Free', 20), background='white').place(anchor = 'n', relx=0.5, rely = 0.3)
bouton_retour = tkinter.Button(page_a_propos, text='Retour', font=('Ink Free', 30), bg = 'aquamarine1')
bouton_retour.place(anchor = 'n', relx=0.5, rely = 0.8)

#page question 1
class PageQuestion:
    def __init__(self, type, question):
        self.page = ttk.Frame(master=root)
        arriere_plan = tkinter.Label(self.page, image=image_arriere_plan).place(x=0,y=0,relwidth=1,relheight=1)
        titre = ttk.Label(self.page, text=question, font=('Ink Free', 40), background='white').place(anchor = 'n', relx=0.5, rely = 0.25)
        if type == 'ecrit':
            reponse = tkinter.StringVar()
            entree_reponse = ttk.Entry(self.page, textvariable=reponse, font=('Ink Free', 20)).place(anchor = 'n', relx=0.5, rely = 0.5, relwidth=0.2)
        # elif type == 'choix':
        #     self.entree_reponse = ttk.Menubutton(page).place(anchor = 'n', relx=0.5, rely = 0.5, relwidth=0.2)
        else:
            raise ValueError(f'Le type de question choisi est invalide')
        bouton_suite = tkinter.Button(self.page, image=image_fleche, bg = 'gray80')
        bouton_suite.place(anchor = 'nw', height = 40, width=40, relx=0.6, rely = 0.5)

    def frame_page(self):
        return self.page
    #reponse1 = reponse.get()

page_q1_classe = PageQuestion('ecrit', 'Test question')
page_q1 = page_q1_classe.frame_page()

# -- Configuration des boutons de transition de pages
#code par IA
bouton2.configure(command=lambda: page_suivante(page_principale, page_a_propos, 'y'))
#code par IA

bouton_retour.configure(command=lambda: page_suivante(page_a_propos, page_principale, 'y', -1))
bouton1.configure(command=lambda: page_suivante(page_principale, page_q1, 'x', 1))

avertissement = ttk.Label(root, text='*Cet outil est un exercice pédagogique utilisant des données synthétiques et ne devrait pas être utilisé comme aide à la décision'
                          , font=('Arial', 16), background='gray80')
avertissement.place(relwidth=1.0)

root.mainloop()