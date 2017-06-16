from tkinter import *
from os import system
from math import sqrt

def distance(x1, y1, x2, y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)

def switchColor(event):
    global blockchecker, mode
    found = False
    plyrspotted = False
    for i in blockchecker:
        for j in i:
            if j.color == '#27ADF9' and mode == '#27ADF9':
                plyrspotted = True
            if j.color == '#27ADF9' and plyrspotted:
                j.switch('white')
            elif distance(event.x, 0, j.x, 0) < 10 and distance(event.y, 0, j.y, 0) < 10:
                j.switch(mode)

def switchMode(c):
    global mode
    mode = c

def createmap():
    global blockchecker
    f = open('terrain.data', 'w')
    for i in blockchecker:
        for j in i:
            if j.color == 'black':
                f.write('#')
            elif j.color == 'white':
                f.write(' ')
            elif j.color == 'yellow':
                f.write('C')
            else:
                f.write('P')
        f.write('\n')
    f.close()
    root.destroy()
    system('python3 minigame.py')

class blockcheck:
    def __init__(self, x, y, color = 'white'):
        self.color = color
        self.x, self.y = x+10, y+10
        self.body = c.create_rectangle(x, y, x+20, y+20, fill = color, outline = '#168BCE')

    def switch(self, color):
        self.color = color
        c.itemconfig(self.body, fill = color)

root = Tk()
root.title('Createur de map')
root.configure(bg = '#168BCE')

mode = 'black'

c = Canvas(root, width = 600, height = 400)
c.bind('<Button-1>', switchColor)
c.bind('<B1-Motion>', switchColor)

blockchecker = []
for i in range(20):
    temp = []
    for j in range(30):
        temp.append(blockcheck(j*20, i*20))
    blockchecker.append(temp)

c.pack(side = LEFT, padx = 20, pady = 20)
Label(root, text = 'Créez votre niveau et jouez-y:\nIl faut un seul personnage, des murs et au moins une pièce.', bg = '#168BCE', fg = 'white').pack(padx = 20, pady = 20)
Button(root, text = 'ajouter des murs', command = lambda: switchMode('black'), fg = 'white', bg = '#168BCE', activebackground = '#269BDE', activeforeground = 'white', relief = FLAT).pack(padx = 20, pady = 20)
Button(root, text = 'supprimer les elements', command = lambda: switchMode('white'), fg = 'white', bg = '#168BCE', activebackground = '#269BDE', activeforeground = 'white', relief = FLAT).pack(padx = 20, pady = 20)
Button(root, text = 'ajouter des pieces', command = lambda: switchMode('yellow'), fg = 'white', bg = '#168BCE', activebackground = '#269BDE', activeforeground = 'white', relief = FLAT).pack(padx = 20, pady = 20)
Button(root, text = 'ajouter le personnage', command = lambda: switchMode('#27ADF9'), fg = 'white', bg = '#168BCE', activebackground = '#00BBFF', activeforeground = 'white', relief = FLAT).pack(padx = 20, pady = 20)
Button(root, text='Creer la carte', command = createmap, fg = 'white', bg = '#168BCE', activebackground = '#269BDE', activeforeground = 'white', relief = FLAT).pack(padx = 20, pady = 20)
root.mainloop()
