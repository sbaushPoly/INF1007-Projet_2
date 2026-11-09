import tkinter
from tkinter import ttk
from tkinter import font

def page_suivante(actuelle, prochaine):
    pass

root = tkinter.Tk()
root.geometry('1600x900')

#print(sorted(list(font.families())))

# ttk.Menubutton(root).pack(side = tkinter.LEFT)
# ttk.Entry(root).pack(side = tkinter.LEFT)

avertissement = ttk.Label(root, text='*Cet outil est un exercice pédagogique utilisant des données synthétiques et ne devrait pas être utilisé comme aide à la décision'
                          , font=('Arial', 16), background='gray')
avertissement.pack(side=tkinter.TOP, fill = tkinter.X)

#page principale
page_principale = ttk.Frame(root, padding=10)
titre_p1 = ttk.Label(page_principale, text='Que sera votre note selon vos habitudes de vie?', font=('Ink Free', 40))
boutons = ttk.Frame(page_principale, padding=10)
bouton1 = tkinter.Button(boutons, text='Commencer', font=('Ink Free', 30), bg = 'khaki1', command = page_suivante(page_principale))
bouton2 = tkinter.Button(boutons, text='À propos', font=('Ink Free', 30), bg = 'aquamarine1')
bouton3 = tkinter.Button(boutons, text='Quitter', font=('Ink Free', 30), bg = 'light sky blue', command=root.quit)

page_principale.pack()
titre_p1.pack(side = tkinter.TOP, expand=True)
boutons.pack(expand=True)
bouton1.pack(side = tkinter.TOP, ipadx=100, pady = 10)
bouton2.pack(side = tkinter.TOP, ipadx=120, pady = 10)
bouton3.pack(side = tkinter.TOP, ipadx=130, pady = 10)

root.mainloop()